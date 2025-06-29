# bill.py
import datetime

class Bill:
    def __init__(self, booking_id):
        self.booking_id = booking_id
        self.booking_date = datetime.date.today().strftime("%Y-%m-%d")
        self.subtotal = 0
        self.ticket_info = []

    def add_ticket(self, ticket):
        self.ticket_info.append(ticket)

    def calculate_charges(self):
        return {
            "sst": self.subtotal * 0.06,
            "processing": self.subtotal * 0.02,
            "admin": 5.0
        }

    def total_charge(self):
        charges = self.calculate_charges()
        return self.subtotal + charges['sst'] + charges['processing'] + charges['admin']

    def print_invoice(self, buyer_name, ic_passport, event_name, event_date, event_venue, price, quantity, ticket_id, ticket_type):
        charges = self.calculate_charges()
        print("\n" + "=" * 30)
        print(f"Booking Invoice - {self.booking_id}")
        print("=" * 30)
        print(f"Customer Name : {buyer_name}")
        print(f"IC/Passport No. : {ic_passport}")
        print(f"Event : {event_name}")
        print(f"Date : {event_date}")
        print(f"Venue : {event_venue}")
        print(f"Ticket Type : {ticket_type}")
        print(f"Price per Ticket : RM{price:.2f}")
        print(f"Quantity : {quantity}")
        print("\n" + "=" * 30)
        print(f"Subtotal : RM{self.subtotal:.2f}")
        print(f"SST (6%) : RM{charges['sst']:.2f}")
        print(f"Processing Fee : RM{charges['processing']:.2f}")
        print(f"Admin Fee : RM{charges['admin']:.2f}")
        print("=" * 30)
        print(f"Total Amount Due : RM{self.total_charge():.2f}")
        print("\nTicket IDs:")
        for ticket_id in self.ticket_info:
            print(f"{ticket_id}")
        print("\nStatus : Booked")
        print("=" * 30)