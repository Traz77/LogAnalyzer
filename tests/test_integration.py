import unittest
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parsers.log_parser import LogParser
from parsers.events_parser import EventsParser
from main import process_entries

class TestIntegration(unittest.TestCase):
    
    def setUp(self):
        self.project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.sample_log_path = os.path.join(self.project_root, 'sample.log')
        self.events_file_path = os.path.join(self.project_root, 'events_sample.txt')
        self.test_compressed_dir = os.path.join(self.project_root, 'test_compressed')  # Updated directory
    
    def test_sample_files_exist(self):
        self.assertTrue(os.path.exists(self.sample_log_path), "sample.log should exist")
        self.assertTrue(os.path.exists(self.events_file_path), "events_sample.txt should exist")
    
    def test_sample_data_processing(self):
        # Test parsing events
        events_parser = EventsParser(self.events_file_path)
        filters = events_parser.parse_events()
        self.assertEqual(len(filters), 23, "Should load 23 event filters from events_sample.txt")
        
        # Test parsing logs
        log_parser = LogParser(self.project_root)
        entries = list(log_parser.parse_all_logs())
        self.assertGreater(len(entries), 0, "Should parse some log entries from sample.log")
        
        # Test that we get expected filter types
        filter_types = [f.event_type for f in filters]
        self.assertIn('TELEMETRY', filter_types)
        self.assertIn('DEVICE', filter_types)
        self.assertIn('GNMI', filter_types)
        
        # Test that we have count and non-count filters
        count_filters = [f for f in filters if f.count]
        display_filters = [f for f in filters if not f.count]
        self.assertGreater(len(count_filters), 0, "Should have some count filters")
        self.assertGreater(len(display_filters), 0, "Should have some display filters")
    
    def test_compressed_features_directory(self):  
        if not os.path.exists(self.test_compressed_dir):
            self.skipTest("test_compressed directory not found - skipping compressed feature tests")
        
        compressed_files = os.listdir(self.test_compressed_dir)
        log_files = [f for f in compressed_files if f.endswith('.log') or f.endswith('.log.gz')]
        self.assertGreater(len(log_files), 0, "Should have log files in test_compressed directory")
        
        # Test compressed log support
        gz_files = [f for f in compressed_files if f.endswith('.log.gz')]
        if gz_files:
            # Test parsing compressed logs
            log_parser = LogParser(self.test_compressed_dir)
            entries = list(log_parser.parse_all_logs())
            self.assertGreater(len(entries), 0, "Should parse entries from compressed logs")
    
    def test_expected_results_with_sample_data(self):
        # Load filters and logs
        events_parser = EventsParser(self.events_file_path)
        filters = events_parser.parse_events()
        
        log_parser = LogParser(self.project_root)
        entries = list(log_parser.parse_all_logs())
        
        # Process entries and count matches
        results = {}
        for entry in entries:
            for filter_obj in filters:
                if filter_obj.matches(entry):
                    filter_key = id(filter_obj)
                    if filter_key not in results:
                        results[filter_key] = {'filter': filter_obj, 'matches': [], 'count': 0}
                    results[filter_key]['matches'].append(entry)
                    results[filter_key]['count'] += 1
        
        # Verify we get some matches
        self.assertGreater(len(results), 0, "Should find some matching entries")
        
        # Verify specific expected patterns work
        telemetry_count_found = False
        device_warning_found = False
        gnmi_error_found = False
        
        for result in results.values():
            filter_obj = result['filter']
            if (filter_obj.event_type == 'TELEMETRY' and 
                filter_obj.count and 
                filter_obj.pattern):
                telemetry_count_found = True
                self.assertGreater(result['count'], 0, "Should find TELEMETRY iteration matches")
            
            if (filter_obj.event_type == 'DEVICE' and 
                filter_obj.level == 'WARNING' and 
                filter_obj.count):
                device_warning_found = True
                self.assertGreater(result['count'], 0, "Should find DEVICE WARNING matches")
            
            if (filter_obj.event_type == 'GNMI' and 
                filter_obj.level == 'ERROR' and 
                not filter_obj.count):
                gnmi_error_found = True
                self.assertGreater(result['count'], 0, "Should find GNMI ERROR matches")
        
        self.assertTrue(telemetry_count_found, "Should find TELEMETRY count filter results")
        self.assertTrue(device_warning_found, "Should find DEVICE WARNING count filter results")
        self.assertTrue(gnmi_error_found, "Should find GNMI ERROR display filter results")
    
    def test_time_filtering_functionality(self):
        # Load sample data
        log_parser = LogParser(self.project_root)
        
        # Test without time filtering
        all_entries = list(log_parser.parse_all_logs())
        
        # Test with time filtering
        from_time = datetime(2025, 6, 1, 14, 30, 0)
        to_time = datetime(2025, 6, 1, 15, 0, 0)
        filtered_entries = list(log_parser.parse_all_logs(from_time, to_time))
        
        # All filtered entries should be within time range
        for entry in filtered_entries:
            self.assertGreaterEqual(entry.timestamp, from_time, 
                                  "Filtered entry should be after from_time")
            self.assertLessEqual(entry.timestamp, to_time, 
                               "Filtered entry should be before to_time")

if __name__ == '__main__':
    unittest.main()