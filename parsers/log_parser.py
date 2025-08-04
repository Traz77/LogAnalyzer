from typing import List, Optional, Generator
from datetime import datetime
import os
import gzip
from models.log_entry import LogEntry

class LogParser:
    def __init__(self, log_dir: str):
        self.log_dir = log_dir

    # Parse all log files in the directory and yield LogEntry objects
    def parse_all_logs(self, from_time: Optional[datetime] = None,
                      to_time: Optional[datetime] = None) -> Generator[LogEntry, None, None]:
        log_files = self._get_log_files()
        
        for file_path in log_files:
            for entry in self._parse_single_file(file_path):
                if self._should_include_entry(entry, from_time, to_time):
                    yield entry
                    
    # Get all log files in the directory
    def _get_log_files(self) -> List[str]:
        if not os.path.exists(self.log_dir):
            print(f"Warning: Directory '{self.log_dir}' does not exist\n")
            return [] 
    
        if not os.path.isdir(self.log_dir):
            print(f"Warning: '{self.log_dir}' is not a directory\n")
            return []
        
        LOG_EXTENSIONS = {'.log', '.log.gz', '.txt'}

        log_files = [] 
        for filename in os.listdir(self.log_dir):
            if any(filename.endswith(ext) for ext in LOG_EXTENSIONS):
                file_path = os.path.join(self.log_dir, filename) 
                log_files.append(file_path)
                
        return sorted(log_files)
                
    # Parse a single log file
    def _parse_single_file(self, file_path: str) -> Generator[LogEntry, None, None]:
        try:
            if file_path.endswith('.gz'):
                file_handle = gzip.open(file_path, 'rt', encoding='utf-8')
            else:
                file_handle = open(file_path, 'r', encoding='utf-8')
            
            with file_handle:
                for line in file_handle:
                    entry = LogEntry.from_line(line)
                    if entry:
                        yield entry
        except (IOError, OSError) as e:
            print(f"Warning: Could not read file {file_path}: {e}")
            return
    
    # Check if log entry falls within time range
    def _should_include_entry(self, log_entry: LogEntry, from_time: Optional[datetime],
                              to_time: Optional[datetime]) -> bool:
        # If no time filters specified, include all entries
        if from_time is None and to_time is None:
            return True
        
        # Check from_time (inclusive)
        if from_time is not None and log_entry.timestamp < from_time:
            return False
        
        # Check to_time (inclusive)
        if to_time is not None and log_entry.timestamp > to_time:
            return False
        
        return True