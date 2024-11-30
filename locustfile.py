from locust import HttpUser, task, between


class CarPartsUser (HttpUser):
    wait_time = between(1, 3)

    @task
    def add_part(self):
        """Simulate adding a new car part."""
        response = self.client.post("/add_part", json={
            "part_type": "Tire",
            "part_name": "All-Season Tire",
            "price": 150
        })
        # Print response for debugging
        print("Add Part Response:", response.text)

    @task
    def get_price(self):
        """Simulate retrieving the price of a car part."""
        response = self.client.get("/get_price?part_name=All-Season Tire")
        # Print response for debugging
        print("Get Price Response:", response.text)

    @task
    def edit_part(self):
        """Simulate editing a car part's price."""
        response = self.client.put("/edit_part", json={
            "part_name": "All-Season Tire",
            "new_price": 160
        })
        # Print response for debugging
        print("Edit Part Response:", response.text)

    @task
    def delete_part(self):
        """Simulate deleting a car part."""
        response = self.client.delete("/delete_part?part_name=All-Season Tire")
        # Print response for debugging
        print("Delete Part Response:", response.text)

    @task
    def generate_report(self):
        """Simulate generating a report."""
        response = self.client.get("/generate_report")
        # Print response for debugging
        print("Generate Report Response:", response.text)

# locust -f locustfile.py --host=http://localhost:8000
