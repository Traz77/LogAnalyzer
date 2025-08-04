import unittest
import tempfile
import os
from cli import CLI

class TestCLI(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.temp_events_file = os.path.join(self.temp_dir, 'test_events.txt')
        
        # Create a real events file for testing
        with open(self.temp_events_file, 'w') as f:
            f.write('TELEMETRY --level INFO\n')
            f.write('DEVICE --pattern "temperature"\n')
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_basic_argument_parsing(self):
        cli = CLI()
        args = cli.parse_args(['--log-dir', self.temp_dir, '--events-file', self.temp_events_file])
        
        self.assertEqual(args.log_dir, self.temp_dir)
        self.assertEqual(args.events_file, self.temp_events_file)
        self.assertIsNone(args.from_time)
        self.assertIsNone(args.to_time)
    
    def test_time_filtering_arguments(self):
        cli = CLI()
        args = cli.parse_args([
            '--log-dir', self.temp_dir,
            '--events-file', self.temp_events_file,
            '--from', '2025-06-01T14:00:00',
            '--to', '2025-06-01T15:00:00'
        ])
        
        self.assertEqual(args.log_dir, self.temp_dir)
        self.assertEqual(args.events_file, self.temp_events_file)
        self.assertIsNotNone(args.from_time)
        self.assertIsNotNone(args.to_time)
    
    def test_invalid_datetime_format(self):
        cli = CLI()
        with self.assertRaises(SystemExit):
            cli.parse_args([
                '--log-dir', self.temp_dir,
                '--events-file', self.temp_events_file,
                '--from', 'invalid-date'
            ])
    
    def test_nonexistent_directory(self):
        cli = CLI()
        with self.assertRaises(SystemExit):
            cli.parse_args([
                '--log-dir', '/nonexistent/directory',
                '--events-file', self.temp_events_file
            ])
    
    def test_nonexistent_events_file(self):
        cli = CLI()
        with self.assertRaises(SystemExit):
            cli.parse_args([
                '--log-dir', self.temp_dir,
                '--events-file', '/nonexistent/events.txt'
            ])

if __name__ == '__main__':
    unittest.main()