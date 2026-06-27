import csv
from pathlib import Path


class PassengerDetails:

    def __init__(
        self,
        passenger_number,
        passenger_name,
        flight_number,
        departure_time,
        arrival_time,
        origin,
        destination,
    ):
        self.passenger_number = passenger_number
        self.passenger_name = passenger_name
        self.flight_number = flight_number
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.origin = origin
        self.destination = destination
        self.flight = []
        self.total = 0
        self.vat = 0
        self.grand_total = 0

    def receptionist_service(self):
        while True:
            try:
                flight_type = input(
                    "Enter flight type (Economy, Business, First Class) or 'exit' to finish: "
                )
                if flight_type.lower() == "exit":
                  
                  break
            except ValueError:
                print("Invalid input. Please enter a valid flight type.")
                continue
            
            try:
                cost = float(input(f"Enter cost for {flight_type} flight: "))
            except ValueError:
                print("Invalid cost. Please enter a number for flight cost.")
                continue
            self.flight.append((flight_type, cost))

    def calculate_totals(self):
        self.total = sum(cost for _, cost in self.flight)
        self.vat = self.total * 0.15  # Assuming VAT is 15%
        self.grand_total = self.total + self.vat
        
    def save_to_csv(self,):
        if not self.flight:
            print("No flight details to save.")
            return
          
        file_path = Path(__file__).parent / f"passenger_{self.passenger_number}.csv"
        with file_path.open(mode="w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                ["Passenger Number", "Passenger Name", "Flight Number", "Departure Time", "Arrival Time", "Origin", "Destination", "Flight Type", "Total Cost", "VAT", "Grand Total"])
            
            writer.writerow(
                [
                    self.passenger_number,
                    self.passenger_name,
                    self.flight_number,
                    self.departure_time,
                    self.arrival_time,
                    self.origin,
                    self.destination,
                    # Flight Type and Cost
                    "; ".join(f"{ftype}: {cost}" for ftype, cost in self.flight),
                    
                    self.total,
                    self.vat,
                    self.grand_total
                ]
            )
            print(f"Flight details saved to {file_path}")        

 
def main():
    passenger_one = PassengerDetails(
        passenger_number="1",
        passenger_name="Eunice",
        flight_number="AB123",
        departure_time="2024-06-01 10:00",
        arrival_time="2024-06-01 14:00",
        origin="UK",
        destination="Canada",
    )
    passenger_one.receptionist_service()
    passenger_one.calculate_totals()
    
    print(
        f"Flight created for passenger {passenger_one.passenger_number}-{passenger_one.passenger_name} on flight {passenger_one.flight_number} from {passenger_one.origin} to {passenger_one.destination}."
    )
    print(f"Flight details: {passenger_one.flight}")
    print(f"Total cost: {passenger_one.total}, VAT: {passenger_one.vat}, Grand Total: {passenger_one.grand_total}")
    
    passenger_one.save_to_csv()


if __name__ == "__main__":

    main()
