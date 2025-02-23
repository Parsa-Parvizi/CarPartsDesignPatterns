from locust import HttpUser, task, between


class CarPartsUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def add_part(self):
        """Simulate adding a new car part."""
        response = self.client.post("/add_part", json={
            "part_type": "engines",
            "part_name": "V8",
            "price": 500
        })
        print("Add Part Response:", response.text)

    @task
    def get_price(self):
        """Simulate retrieving the price of a car part."""
        response = self.client.get("/get_price?part_name=V8")
        print("Get Price Response:", response.text)

    @task
    def edit_part(self):
        """Simulate editing a car part's price."""
        response = self.client.put("/edit_part", json={
            "part_name": "V8",
            "new_price": 600
        })
        print("Edit Part Response:", response.text)

    @task
    def delete_part(self):
        """Simulate deleting a car part."""
        response = self.client.delete("/delete_part?part_name=V8")
        print("Delete Part Response:", response.text)

    @task
    def generate_report(self):
        """Simulate generating a report."""
        response = self.client.get("/generate_report")
        print("Generate Report Response:", response.text)

# Run with: locust -f locustfile.py --host=http://localhost:8000
