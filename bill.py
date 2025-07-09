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
        print("\n" + "=" * 52)
        print(f"INTI EVENT TICKETING SYSTEM")
        print(f"Booking Invoice - {self.booking_id}")
        print("=" * 52)
        print(f"{'Customer Name':<20}: {buyer_name}")
        print(f"{'IC/Passport No.':<20}: {ic_passport}")
        print(f"{'Event:':<20}: {event_name}")
        print(f"{'Date':<20}: {event_date}")
        print(f"{'Venue':<20}: {event_venue}")
        print(f"{'Ticket Type':<20}: {ticket_type}")
        print(f"{'Price per Ticket':<20}: RM{price:.2f}")
        print(f"{'Quantity':<20}: {quantity}")
        print("\n" + "-" * 52)
        print(f"{'Subtotal':<20}: RM{self.subtotal:.2f}")
        print(f"{'SST (6%)':<20}: RM{charges['sst']:.2f}")
        print(f"{'Processing Fee':<20}: RM{charges['processing']:.2f}")
        print(f"{'Admin Fee (Flat)':<20}: RM{charges['admin']:.2f}")
        print("-" * 52)
        print(f"{'Total Amount Due':<20}: RM{self.total_charge():.2f}")
        print("\nTicket IDs:")
        for ticket_id in self.ticket_info:
            print(f"    {ticket_id}")
        print(f"\n{'Status':<20}: Booked")
        print("=" * 52)
        print("Please keep this invoice for entry and verification.")
        print("=" * 52)


