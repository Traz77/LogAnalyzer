from dataclasses import dataclass
from typing import Optional
import re

@dataclass(frozen=True)
class EventFilter:
    event_type: str                         # Required
    count: bool = False                     # Optional: --count flag
    level: Optional[str] = None             # Optional: --level INFO/WARNING/ERROR
    pattern: Optional[re.Pattern] = None    # Optional: --pattern regex
    
    # Parse an events configuration line into an EventFilter
    @classmethod
    def from_line(cls, line: str) -> Optional['EventFilter']:
        line = line.strip()
        
        if not line or line.startswith('#'):
            return None
        
        parts = line.split()
        if len(parts) < 1:
            return None
        
        event_type = parts[0]
        count = False
        level = None
        pattern = None
        
        i = 1
        while i < len(parts):
            if parts[i] == '--count':
                count = True
                i += 1
            elif parts[i] == '--level' and i + 1 < len(parts):
                level = parts[i + 1]
                i += 2
            elif parts[i] == '--pattern' and i + 1 < len(parts):
                # Find the end of the pattern (before next -- flag or end of line)
                pattern_parts = []
                i += 1
                while i < len(parts) and not parts[i].startswith('--'):
                    pattern_parts.append(parts[i])
                    i += 1
                
                if pattern_parts:
                    pattern_str = ' '.join(pattern_parts)
                    try:
                        pattern = re.compile(pattern_str)
                    except re.error as e:
                        print(f"Warning: Invalid regex pattern '{pattern_str}': {e}")
                        return None
            else:
                i += 1
        
        # Atleast 1 filter
        if not count and level is None and pattern is None:
            print(f"Warning: Filter for {event_type} has no criteria, ignoring")
            return None
        
        return cls(event_type, count, level, pattern)
     
    # Check if a LogEntry matches this filter
    def matches(self, log_entry) -> bool:
        
        if log_entry.event_type != self.event_type:
            return False
        
        if self.level is not None:
            if log_entry.level != self.level:
                return False
        
        if self.pattern is not None:
            if not self.pattern.search(log_entry.message):
                return False
        
        return True
