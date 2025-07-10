from functions import *

print(eventOptionMenu())
event_dict = eventOptionMenu()

#print(event_id)

for event_id, event_info in event_dict.items():
    name = event_info["name"]
    date = event_info["date"]
    venue = event_info["venue"]
    print(f"\n{'Event ID':<12}: [ {event_id} ]\n{'Event Title':<12}: {name}\n{'Date':<12}: {date}\n{'Venue':<12}: {venue}\n")
    print("-"*33)
    
#duplicate_id.append(event_id) # append shown event_id to duplicate_id list

