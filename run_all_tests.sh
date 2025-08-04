#!/bin/bash
echo "Running tests..."

# Create output directory
mkdir -p tests_output

# Main functionality test
echo "Testing main functionality..."
python3 main.py --log-dir . --events-file events_sample.txt > tests_output/sample_output.txt

# Time filtering test
echo "Testing time filtering..."
python3 main.py --log-dir . --events-file events_sample.txt --from 2025-06-01T14:00:00 --to 2025-06-01T15:00:00 > tests_output/time_filtered_output.txt

# Bonus features test
echo "Testing bonus features..."
python3 main.py --log-dir test_bonus --events-file test_bonus/test_events.txt > tests_output/bonus_output.txt

# Unique compressed test
echo "Testing unique compressed patterns..."
python3 main.py --log-dir test_bonus --events-file test_bonus/unique_test_events.txt > tests_output/unique_compressed_output.txt

# Unit tests
echo "Running unit tests..."
python3 -m unittest discover tests -v 2>&1 | tee tests_output/unit_tests_output.txt

# Integration tests specifically
echo "Running integration tests..."
python3 -m unittest tests.test_integration -v > tests_output/integration_tests_output.txt 2>&1

# Help output
echo "Generating help output..."
python3 main.py --help > tests_output/help_output.txt

# Compressed file verification test
echo "Testing compressed file processing verification..."
python3 main.py --log-dir test_bonus --events-file test_bonus/unique_test_events.txt > tests_output/compressed_verification_output.txt

# Test error handling
echo "Testing error cases..."
python3 main.py --log-dir nonexistent --events-file events_sample.txt > tests_output/error_handling_output.txt 2>&1

# Test --from only filtering
echo "Testing --from only filtering..."
python3 main.py --log-dir . --events-file events_sample.txt --from 2025-06-01T14:30:00 > tests_output/from_only_filtering_output.txt

# Test --to only filtering
echo "Testing --to only filtering..."
python3 main.py --log-dir . --events-file events_sample.txt --to 2025-06-01T15:00:00 > tests_output/to_only_filtering_output.txt

echo "All tests completed! Check the output directory."
echo "Files generated:"
ls -la tests_output/