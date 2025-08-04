import argparse
from datetime import datetime
from typing import Optional
import os 

class CLI:
    def __init__(self):
        self.parser = self._create_parser()
        
    def _create_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            description="Analyze log files to extract and report structured event data",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
    python main.py --log-dir /logs --events-file events.txt
    python main.py --log-dir /logs --events-file events.txt --from 2025-06-01T14:00:00
    python main.py --log-dir /logs --events-file events.txt --from 2025-06-01T14:00:00 --to 2025-06-01T16:00:00
        """
        )
        
        parser.add_argument(
            '--log-dir',
            required=True,
            help='Path to a folder containing log files'
        )
        
        parser.add_argument(
            '--events-file',
            required=True,
            help='Path to a config file that defines how to filter log events'
        )
        
        # Optional args
        parser.add_argument(
            '--from',
            dest='from_time',
            help='Start time filter (YYYY-MM-DDTHH:MM:SS format)'
        ) 
        
        parser.add_argument(
            '--to',
            dest='to_time',
            help='End time filter (YYYY-MM-DDTHH:MM:SS format)'
        )
        
        return parser
    
    def parse_args(self, args=None):
        parsed_args = self.parser.parse_args(args)
        
        # Validate log directory exists
        if not os.path.exists(parsed_args.log_dir):
            self.parser.error(f"Log directory does not exist: '{parsed_args.log_dir}'")
        
        if not os.path.isdir(parsed_args.log_dir):
            self.parser.error(f"Log directory path is not a directory: '{parsed_args.log_dir}'")
        
        # Validate events file exists
        if not os.path.exists(parsed_args.events_file):
            self.parser.error(f"Events file does not exist: '{parsed_args.events_file}'")
        
        if not os.path.isfile(parsed_args.events_file):
            self.parser.error(f"Events file path is not a file: '{parsed_args.events_file}'")
            
        if parsed_args.from_time:
            try:
                parsed_args.from_time = self._parse_datetime(parsed_args.from_time)
            except ValueError as e:
                self.parser.error(f"Invalid --from datetime format: {e}")
        
        if parsed_args.to_time:
            try:
                parsed_args.to_time = self._parse_datetime(parsed_args.to_time)
            except ValueError as e:
                self.parser.error(f"Invalid --to datetime format: {e}")

        if (parsed_args.from_time and parsed_args.to_time and 
            parsed_args.from_time >= parsed_args.to_time):
            self.parser.error("Error: --from time must be earlier than --to time")
        
        return parsed_args
        
    def _parse_datetime(self, datetime_str: str) -> datetime:
        try:
            return datetime.fromisoformat(datetime_str)
        except ValueError:
            if 'T' not in datetime_str:
                raise ValueError(f"Missing 'T' separator. Expected format: YYYY-MM-DDTHH:MM:SS, got: {datetime_str}")
            
            raise ValueError(f"Expected format: YYYY-MM-DDTHH:MM:SS, got: {datetime_str}") 