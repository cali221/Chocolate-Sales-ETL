import requests

order_data = {
  "customer_id": 1,
  "items": [
    {
      "quantity": 2,
      "product_id": 2
    },
    {
      "quantity": 2,
      "product_id": 1
    }
  ],
  "tax_amount": 3,
  "discount_amount": 3,
  "shipping_costs_amount": 3
}

r = requests.post('http://localhost:8000/orders', json=order_data)

print(r.json())