# event.py
class Event:
    def __init__(self, event_id, name, date, venue):
        self.event_id = event_id
        self.name = name
        self.date = date
        self.venue = venue
        self.ticket_types = {}

    def add_ticket_type(self, ticket_type, price, quota):
        self.ticket_types[ticket_type] = {
            "price": float(price),
            "quota": int(quota)
        }

    def display_ticket_types(self, remaining):
        print(f"Ticket Types for {self.name} ({self.event_id}):")
        for ttype, info in self.ticket_types.items():
            left = remaining.get(ttype, info['quota'])
            print(f"- {ttype} - RM{info['price']} (Remaining: {left})")