# ticket.py
class Ticket:
    def __init__(self, ticket_id, booking_id, event_id, ticket_type, buyer_name, ic_number, status='Active'):
        self.ticket_id = ticket_id
        self.booking_id = booking_id
        self.event_id = event_id
        self.ticket_type = ticket_type
        self.buyer_name = buyer_name
        self.ic_number = ic_number
        self.status = status

    def __str__(self):
        return f"{self.ticket_id},{self.booking_id},{self.event_id},{self.ticket_type},{self.buyer_name},{self.ic_number},{self.status}\n"