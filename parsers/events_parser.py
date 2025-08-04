from typing import List
from models.event_filter import EventFilter

class EventsParser:
    def __init__(self, events_file: str):
        self.events_file = events_file
    
    # Parse events configuration file and return list of EventFilter objects
    def parse_events(self) -> List[EventFilter]:
        filters = []
        
        try: 
            with open(self.events_file, 'r', encoding='utf-8') as file:
                for line in file:
                    event_filter = EventFilter.from_line(line) 
                    if event_filter:
                        filters.append(event_filter)
        except (IOError, OSError) as e:
            print(f"Error reading events file {self.events_file}: {e}")
            return []
        
        return filters
    
    
    