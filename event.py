# event.py
# Event Info
class Event:

    _event_counter = 1 
    _file_path = "events.txt"  # Path to the file

    @classmethod
    def _initialize_counter_from_file(cls):
        file = open(cls._file_path, "r")
        lines = file.readlines()
        file.close()
        
        # Auto generate and increment for Event ID
        # variable to store latest Event ID
        max_id = 0
        for line in lines:
            parts = line.strip().split(",")
            if parts and parts[0].startswith("E"):
                id_num = int(parts[0][1:])  
                if id_num > max_id:
                    max_id = id_num
        cls._event_counter = max_id + 1

    def __init__(self, name, date, venue):

        if Event._event_counter == 1:
            Event._initialize_counter_from_file()

        self.event_id = f"E{Event._event_counter:03d}"
        Event._event_counter += 1
        self.name = name
        self.date = f"{date[:4]}-{date[4:6]}-{date[6:]}"
        self.venue = venue
        self.ticket_types = {}

    def add_ticket_type(self, ticket_type, price, quota):
        self.ticket_types[ticket_type] = {
            "price": float(price),
            "quota": int(quota)
        }

    def __str__(self):
        lines = []
        for ticket_type, info in self.ticket_types.items():
            line = f"{self.event_id},{self.name},{self.date},{self.venue},{ticket_type},{info['price']},{info['quota']}"
            lines.append(line)
        return "\n".join(lines)


