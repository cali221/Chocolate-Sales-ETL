import requests
import random
import json

def create_random_order(host, port):
  print("\nCreating a new random order....")
  # get product IDs (limit 100)
  products = requests.get(f"http://{host}:{port}/products/available_online/").json()
  product_ids_and_prices = [{"product_id": product['id'], 
                             "product_price": product['current_price_online']} for product in products]

  # get customer IDs (limit 100)
  customers = requests.get(f"http://{host}:{port}/customers").json()
  customer_ids = [customer['id'] for customer in customers]

  # get a random number of distinct products to order
  # should be <= the number of product IDs
  number_of_items = random.randint(1, len(product_ids_and_prices))

  print(f"Number of distinct products to order: {number_of_items}")

  # get number_of_items unique product IDs 
  selected_product_ids_and_prices = random.sample(product_ids_and_prices, number_of_items)
  
  print("Selected products to order:")
  for item in selected_product_ids_and_prices:
    print(f"Product ID: {item['product_id']} | Product Price: {item['product_price']}")

  # get a list of the items to order with their quantities
  order_items = [ {"quantity": random.randint(1, 500), 
                   "product_id": item['product_id'],
                   "discount_per_unit_amount":  round(random.uniform(0, item['product_price']), 3)} 
                  for item in selected_product_ids_and_prices]

  # set up the order data
  order_data = {
    "customer_id": random.choice(customer_ids),
    "items": order_items,
    "tax_amount": round(random.uniform(1, 15), 3),
    "discount_off_order_amount": round(random.uniform(1, 10), 3),
    "shipping_costs_amount": round(random.uniform(1, 15), 3)
  }

  # create an order
  order_created = requests.post(f"http://{host}:{port}/orders", json=order_data)

  # print the json results of the endpoint
  print(f"Inserted order:\n{json.dumps(order_created.json(), indent=2)}")
  print("Finished creating a new random order....\n")