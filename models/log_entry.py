from dataclasses import dataclass
from datetime import datetime 
from typing import Optional

@dataclass(frozen=True)
class LogEntry:
    timestamp: datetime
    level: str
    event_type: str 
    message: str
    
    @classmethod
    def from_line(cls, line: str) -> Optional['LogEntry']:
        # Parse log line into LogEntry object 
        line = line.strip()
        
        if not line:
            return None
        
        # Split the line into 4 parts max - last one is the message
        parts = line.split(' ', 3)
        
        if len(parts) < 4:
            return None # Invalid line format 
        try:
            timestamp_str = parts[0]
            timestamp = datetime.fromisoformat(timestamp_str)
            
            level = parts[1]
            event_type = parts[2]
            message = parts[3]
        
            return cls(timestamp, level, event_type, message)
        except(ValueError, IndexError):
            return None
    