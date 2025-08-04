import unittest
import tempfile
import os
import gzip
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parsers.log_parser import LogParser
from parsers.events_parser import EventsParser

class TestLogParser(unittest.TestCase):
    
    def test_regular_log_file_parsing(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.log', delete=False) as f:
            f.write("2025-06-01T14:03:05 INFO TELEMETRY Test message 1\n")
            f.write("2025-06-01T14:04:05 ERROR DEVICE Test message 2\n")
            temp_log_path = f.name
        
        try:
            # Test parsing
            log_parser = LogParser(os.path.dirname(temp_log_path))
            entries = list(log_parser.parse_all_logs())
            
            self.assertEqual(len(entries), 2)
            self.assertEqual(entries[0].message, "Test message 1")
            self.assertEqual(entries[0].event_type, "TELEMETRY")
            self.assertEqual(entries[1].message, "Test message 2")
            self.assertEqual(entries[1].event_type, "DEVICE")
        finally:
            os.unlink(temp_log_path)

    def test_compressed_log_file_parsing(self):
        # Create temporary compressed log file
        with tempfile.NamedTemporaryFile(suffix='.log.gz', delete=False) as f:
            temp_gz_path = f.name
        
        log_data = "2025-06-01T14:03:05 INFO TELEMETRY Compressed test message\n"
        with gzip.open(temp_gz_path, 'wt') as f:
            f.write(log_data)
        
        try:
            # Test parsing compressed file
            log_parser = LogParser(os.path.dirname(temp_gz_path))
            entries = list(log_parser.parse_all_logs())
            
            self.assertEqual(len(entries), 1)
            self.assertEqual(entries[0].message, "Compressed test message")
            self.assertEqual(entries[0].event_type, "TELEMETRY")
        finally:
            os.unlink(temp_gz_path)

class TestEventsParser(unittest.TestCase):
    def test_events_file_parsing(self):
        # Create temporary events file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("TELEMETRY --count --pattern ^Iteration time:\n")
            f.write("DEVICE --level WARNING\n")
            f.write("# This is a comment\n")
            f.write("GNMI --level ERROR\n")
            temp_events_path = f.name
        
        try:
            # Test parsing
            events_parser = EventsParser(temp_events_path)
            filters = events_parser.parse_events()
            
            self.assertEqual(len(filters), 3)  # Should skip comment line
            self.assertEqual(filters[0].event_type, "TELEMETRY")
            self.assertTrue(filters[0].count)
            self.assertEqual(filters[1].event_type, "DEVICE")
            self.assertEqual(filters[1].level, "WARNING")
        finally:
            os.unlink(temp_events_path)

if __name__ == '__main__':
    unittest.main()