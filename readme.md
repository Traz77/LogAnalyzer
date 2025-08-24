# Log Analyzer - Solution Description
the solution follows a modular architecture with an emphasis on separation of concerns. 
The design prioritizes maintainability, testability and extensibility. 

# Flow: 
1. CLI Input
-  ↓
2. Parse Arguments (--log-dir, --events-file, --from, --to)
-  ↓
3. Read Events Configuration File
-  ↓
4. Parse Each Event Line → Create EventFilter Objects
-  ↓
5. Read All Log Files in Directory
-  ↓
6. Parse Each Log Line → Create LogEntry Objects
-  ↓
7. Apply Time Filtering (--from, --to) → Reduce Workload on Event Filter (stream only valid entries)
-  ↓
8. For Each EventFilter:
   - Find Matching LogEntry Objects
   - Either Count or Collect Matches
-  ↓
9. Format and Display Results

# Design Decisions
- Models: LogEntry and EventFilter as data classes for immutability and built in validation

- Parsers: Dedicated classes for parsing different file types 

- CLI: Isolated cli interface with proper UX 

- Each component is testable and allowed for easy extension.

# Design Patterns 
- Factory methods - LogEntry.from_line and EventFilter.from_line use factory methods for object creation 

- Strategy - matches() method in EventFilter applies different matching strategies based on config(level, pattern etc.)

- Generator - LogParser.parse_all_logs() yields entries on-demand for memory efficiency

# Performance Consideration 
- Use of generator for log processing - avoid loading everything into memory simultaneously.

- Each event filter operated independently, matching against the same log stream. Multiple filters can match the same log entry.

- Pre-compiling regex patterns during config parsing, instead of compiling them for every log line match

- Hash based result tracking, ensures unique identification of filters for result.

- Min use of I/O 

# Usage 
### Get help 
```bash
python3 main.py -h
python3 main.py --help 
```

### Basic usage
```bash
# Run with sample data 
python3 main.py --log-dir . --events-file events_sample.txt
```

### Run all tests - output will be in tests_output folder
```bash
chmod +x run_all_tests.sh
./run_all_tests.sh
```

### Time filtering
```bash
# Filter logs from 2:00 PM to 3:00 PM
python3 main.py --log-dir . --events-file events_sample.txt --from 2025-06-01T14:00:00 --to 2025-06-01T15:00:00

# Filter logs from 2:30 PM onwards
python3 main.py --log-dir . --events-file events_sample.txt --from 2025-06-01T14:30:00

# Filter logs up to 3:00 PM
python3 main.py --log-dir . --events-file events_sample.txt --to 2025-06-01T15:00:00
```

### Compressed test
```bash
# Test compressed logs support
python3 main.py --log-dir test_bonus --events-file test_bonus/test_events.txt

# Test compressed patterns
python3 main.py --log-dir test_bonus --events-file test_bonus/unique_test_events.txt
```
