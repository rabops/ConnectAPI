from flask import Flask, request
from woocommerce import API
import time
import requests
import json
import os
from dotenv import load_dotenv




# Load environment variables from .env file
load_dotenv()

api_key = os.environ.get("WOO_CONSUMER_KEY")
api_secret = os.environ.get("WOO_SECRET_KEY")
api_lightspeed = os.environ.get("LIGHTSPEED_KEY")

# Initialize the WooCommerce API client
wcapi = API(
    url="https://steelos.pwd.net.au",  # Replace with your site URL
    consumer_key=api_key,
    consumer_secret=api_secret,
    wp_api=True,
    version="wc/v3"
)

url = "https://steelos.retail.lightspeed.app/api/2.0/product_categories"
headers = {
    "accept": "application/json",
    "authorization": f"Bearer {api_lightspeed}"
}

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def hook():
    # Get data from form
   data = request.form.to_dict()

    # Print data received

   payload_data = json.loads(data["payload"])
 #  print("Received shaishel ssss:", payload_data)
    # Extract title, ID, and category
   title = payload_data["name"]
 #  product_id = payload_data["id"]
   category = payload_data["product_type"]["name"]


   product_data = {
        'title': title,
        'category': category
   }

   print('title is ',product_data)


    # Check if category exists, if not create one
   category = wcapi.get("products/categories", params={"slug": product_data["category"]}).json()
   if not category:
        new_category_data = {
            'name': product_data['category'],
            'slug': product_data['category'].lower()  # Slug is required
        }
        created_category = wcapi.post("products/categories", new_category_data).json()
        category_id = created_category['id']
   else:
        category_id = category[0]['id']

    # Check if product exists, if not create one
   product = wcapi.get("products", params={"search": product_data["title"]}).json()

    #product = wcapi.get("products/41117").json()
   print('checking...........product\n',product)
   if product:
        product_id = product[0]['id']
        # Update existing product's category
        product_update_data = {
            'categories': [{'id': category_id}]
        }
        updated_product = wcapi.put(f"products/{product_id}", product_update_data).json()

   return product_data


if __name__ == "__main__":
    app.run()
