from cli import CLI
from parsers.events_parser import EventsParser
from parsers.log_parser import LogParser

def main():
    # Parse cli args
    cli = CLI()
    args = cli.parse_args()
    
    # Load event filters from config files
    print(f"Loading event filters from: {args.events_file}")
    events_parser = EventsParser(args.events_file)
    filters = events_parser.parse_events()
    
    if not filters:
        print("No valid event filters found")
        return
    
    print(f"Loaded {len(filters)} event filters")
    
    print(f"Parsing log files from: {args.log_dir}\n")
    log_parser = LogParser(args.log_dir)
    log_entries = log_parser.parse_all_logs(args.from_time, args.to_time)
    
    process_entries(log_entries, filters)
    
def process_entries(log_entries, filters):
    # Results per filter 
    results = {}
    
    for filter_obj in filters:
        filter_key = f"{filter_obj.event_type}_{hash(str(filter_obj))}"
        results[filter_key] = {
            'filter': filter_obj,
            'matches': [],
            'count': 0
        } 
    
    total_entries = 0 
    for entry in log_entries:
        total_entries += 1
        
        for filter_obj in filters:
            if filter_obj.matches(entry):
                filter_key = f"{filter_obj.event_type}_{hash(str(filter_obj))}"
                results[filter_key]['matches'].append(entry)
                results[filter_key]['count'] += 1
                
    display_results(results, total_entries)
    
def display_results(results, total_entries):
    """Display the matching results according to specification"""
    
    for filter_key, result in results.items():
        filter_obj = result['filter']
        matches = result['matches']
        count = result['count']
        
        # Build filter description
        filter_desc = f"Event: {filter_obj.event_type}"
        
        if filter_obj.level:
            filter_desc += f" level [{filter_obj.level}]"
        
        if filter_obj.pattern:
            filter_desc += f" pattern [{filter_obj.pattern.pattern}]"
        
        if filter_obj.count:
            filter_desc += f" count — matches: {count} entries"
            print(filter_desc)
        else:
            filter_desc += " — matching log lines:"
            print(filter_desc)
            for match in matches:
                timestamp_str = match.timestamp.strftime('%Y-%m-%dT%H:%M:%S')
                print(f"{timestamp_str} {match.level} {match.event_type} {match.message}")
        
        print()  # Empty line between results
        
if __name__ == "__main__":
    main()