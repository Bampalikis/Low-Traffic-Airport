import queue
import random
import time

# Constants
ACTIONS = {
    "TAKEOFF": "takeoff",
    "LANDING": "landing",
    "EMERGENCY_LANDING": "emergency"
}

class Airport:
    def __init__(self):
        self.planes_waiting_to_takeoff = queue.Queue()   # Queue for planes waiting to take off
        self.planes_waiting_to_land = queue.PriorityQueue() # Priority queue for planes waiting to land

    def queue_for_takeoff(self, plane_id):
        self.planes_waiting_to_takeoff.put(plane_id)
        print(f"{plane_id} requests takeoff.")

    def queue_for_landing(self, plane_id, emergency=False):
        if emergency:
            print(f"{plane_id} requests emergency landing.")
            # Plane with higher priority for emergency landing
            self.planes_waiting_to_land.put((0, plane_id))
        else:
            print(f"{plane_id} requests landing.")
            self.planes_waiting_to_land.put((1, plane_id))

    def process_takeoffs(self):
        while not self.planes_waiting_to_takeoff.empty():
            plane_id = self.planes_waiting_to_takeoff.get()
            print(f"CONTROL: {plane_id} takeoff.")
            time.sleep(1)  # Simulate takeoff time

    def process_landings(self):
        while not self.planes_waiting_to_land.empty():
            _, plane_id = self.planes_waiting_to_land.get()
            print(f"CONTROL: {plane_id} land.")
            time.sleep(1)  # Simulate landing time

    def allow_landing(self, plane_id, emergency=False):
        if emergency:
            print(f"{plane_id} requests emergency landing.")
            self.queue_for_landing(plane_id, emergency=True)
        elif self.planes_waiting_to_land.empty():
            print(f"CONTROL: {plane_id} land.")
            self.queue_for_landing(plane_id)
        else:
            # Check if there are any planes waiting for landing with lower priority
            lower_priority_landing = any(priority > 0 for priority, _ in self.planes_waiting_to_land.queue)
            if not lower_priority_landing:
                print(f"CONTROL: {plane_id} land.")
                self.queue_for_landing(plane_id)
            else:
                print(f"{plane_id} will have to wait for landing.")
                self.queue_for_takeoff(plane_id)

# Function to simulate airport activity
def simulate_airport(airport, num_requests):
    for _ in range(num_requests):
        action = random.choice([ACTIONS["TAKEOFF"], ACTIONS["LANDING"], ACTIONS["EMERGENCY_LANDING"]])
        plane_id = f"Flight {random.randint(100, 999)}"
        if action == ACTIONS["TAKEOFF"]:
            airport.queue_for_takeoff(plane_id)
        elif action == ACTIONS["LANDING"]:
            airport.allow_landing(plane_id)
        else:  # Emergency landing
            airport.allow_landing(plane_id, emergency=True)

    # Process takeoffs and landings after all requests
    airport.process_takeoffs()
    airport.process_landings()

# Example usage:
if __name__ == "__main__":
    airport = Airport()
    num_requests = 10  # Number of random requests to simulate

    simulate_airport(airport, num_requests)
