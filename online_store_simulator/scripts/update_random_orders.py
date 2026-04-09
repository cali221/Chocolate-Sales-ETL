import requests
import random

def update_random_orders_status(host):
    # get uncompleted orders (limit 100)
    orders = requests.get(f"http://{host}:8000/uncompleted_orders").json()

    if not orders:
        print("Uncompleted order not found")
    else:
        print("\nUpdating status of random orders...")
        # get all statuses as json
        all_statuses = requests.get(f"http://{host}:8000/status").json()

        # status id mapping
        status_id_mapping = {status["name"]: status["id"] for status in all_statuses}

        # status transition mapping
        status_transition_mapping = {
            "Pending": "Processing",
            "Processing": "In Transit",
            "In Transit": "Arrived",
            "Arrived": "Completed",
            "Completed": None
        }

        # get the number of orders to update
        number_of_orders_to_update = random.randint(1, len(orders))
        print(f"NUMBER OF ORDERS TO UPDATE: {number_of_orders_to_update }")

        # get a sample of unique orders of size number_of_orders_to_update
        selected_orders = random.sample(orders, number_of_orders_to_update)
        print(f"SELECTED ORDER IDs: {[order['id'] for order in selected_orders]}")

        for order in selected_orders:
            # get the order's current status name
            current_status = order["current_status_name"]

            # get the order's next status name
            next_status = status_transition_mapping[current_status]

            # print some data
            print(f"\nORDER ID: {order["id"]} | CURRENT STATUS: {current_status} | NEXT STATUS: {next_status} | NEXT STATUS ID: {status_id_mapping[next_status]}")
            
            # if next status is not None (not completed)
            if next_status is not None:
                # update the order so it has the next status
                update_response = requests.patch(f"http://{host}:8000/orders/{order['id']}", json={"current_status_id": status_id_mapping[next_status]})
                
                # print the updated status result
                print(f"Updated order status: {update_response.json()['current_status_name']} (status ID: {update_response.json()['current_status_id']})\n")
            else:
                print("Order has been completed, skipping update...")

        print("\nFinished updating status of random orders...\n")
