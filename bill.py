# bill.py
import datetime

class Bill:
    def __init__(self, booking_id, buyer_name, ic_number, event, ticket_type, quantity, price):
        self.booking_id = booking_id
        self.date = datetime.date.today().strftime("%Y-%m-%d")
        self.buyer_name = buyer_name
        self.ic_number = ic_number
        self.event = event
        self.ticket_type = ticket_type
        self.quantity = quantity
        self.price = price
        self.subtotal = price * quantity
        self.tickets = []

    def add_ticket(self, ticket):
        self.tickets.append(ticket)

    def calculate_charges(self):
        return {
            "sst": self.subtotal * 0.06,
            "processing": self.subtotal * 0.02,
            "admin": 5.0
        }

    def total_charge(self):
        ch = self.calculate_charges()
        return self.subtotal + ch['sst'] + ch['processing'] + ch['admin']

    def print_invoice(self):
        charges = self.calculate_charges()
        print("===========================")
        print(f"Booking Invoice - {self.booking_id}")
        print("===========================")
        print(f"Customer Name : {self.buyer_name}")
        print(f"IC/Passport No.: {self.ic_number}")
        print(f"Event : {self.event.name}")
        print(f"Date : {self.event.date}")
        print(f"Venue : {self.event.venue}")
        print(f"Ticket Type : {self.ticket_type}")
        print(f"Price per Ticket : RM{self.price:.2f}")
        print(f"Quantity : {self.quantity}")
        print("---------------------------")
        print(f"Subtotal : RM{self.subtotal:.2f}")
        print(f"SST (6%) : RM{charges['sst']:.2f}")
        print(f"Processing Fee : RM{charges['processing']:.2f}")
        print(f"Admin Fee : RM{charges['admin']:.2f}")
        print("---------------------------")
        print(f"Total Amount Due : RM{self.total_charge():.2f}")
        print("\nTicket IDs:")
        for t in self.tickets:
            print(f" {t.ticket_id}")
        print("\nStatus : Booked")
        print("===========================")