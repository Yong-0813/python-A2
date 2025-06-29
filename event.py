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

    def __str__(self):
        lines = []
        for ticket_type, info in self.ticket_types.items():
            line = f"{self.event_id},{self.name},{self.date},{self.venue},{ticket_type},{info['price']},{info['quota']}"
            lines.append(line)
        return "\n".join(lines)
