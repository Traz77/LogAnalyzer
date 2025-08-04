import unittest
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.log_entry import LogEntry
from models.event_filter import EventFilter

class TestLogEntry(unittest.TestCase):
    
    def test_valid_log_line_parsing(self):
        line = "2025-06-01T14:03:05 INFO TELEMETRY Iteration time: 1.2 sec"
        entry = LogEntry.from_line(line)
        
        self.assertIsNotNone(entry)
        self.assertEqual(entry.level, "INFO")
        self.assertEqual(entry.event_type, "TELEMETRY")
        self.assertEqual(entry.message, "Iteration time: 1.2 sec")
        self.assertEqual(entry.timestamp, datetime(2025, 6, 1, 14, 3, 5))
    
    def test_invalid_log_line_parsing(self):
        # Too few parts
        entry = LogEntry.from_line("2025-06-01 14:03:05 INFO")
        self.assertIsNone(entry)
        
        # Invalid timestamp
        entry = LogEntry.from_line("invalid-date 14:03:05 INFO TELEMETRY message")
        self.assertIsNone(entry)
        
        # Empty line
        entry = LogEntry.from_line("")
        self.assertIsNone(entry)

class TestEventFilter(unittest.TestCase):
    
    def test_count_filter_parsing(self):
        line = "TELEMETRY --count --pattern ^Iteration time:\\s\\d+\\.\\d+\\ssec$"
        filter_obj = EventFilter.from_line(line)
        
        self.assertIsNotNone(filter_obj)
        self.assertEqual(filter_obj.event_type, "TELEMETRY")
        self.assertTrue(filter_obj.count)
        self.assertIsNotNone(filter_obj.pattern)
    
    def test_level_filter_parsing(self):
        line = "DEVICE --level WARNING"
        filter_obj = EventFilter.from_line(line)
        
        self.assertIsNotNone(filter_obj)
        self.assertEqual(filter_obj.event_type, "DEVICE")
        self.assertEqual(filter_obj.level, "WARNING")
        self.assertFalse(filter_obj.count)
    
    def test_pattern_matching(self):
        entry = LogEntry(
            timestamp=datetime(2025, 6, 1, 14, 3, 5),
            level="INFO",
            event_type="TELEMETRY",
            message="Iteration time: 1.2 sec"
        )
        
        # Test matching pattern
        filter_obj = EventFilter.from_line("TELEMETRY --pattern ^Iteration time:")
        self.assertTrue(filter_obj.matches(entry))
        
        # Test non-matching event type
        filter_obj = EventFilter.from_line("DEVICE --pattern ^Iteration time:")
        self.assertFalse(filter_obj.matches(entry))
        
        # Test non-matching level
        filter_obj = EventFilter.from_line("TELEMETRY --level ERROR")
        self.assertFalse(filter_obj.matches(entry))

if __name__ == '__main__':
    unittest.main()