from woocommerce import API
import time
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("WOO_CONSUMER_KEY")  
api_secret = os.getenv("WOO_SECRET_KEY")
api_lightspeed = os.getenv("LIGTSPEED_KEY")

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

response = requests.get(url, headers=headers)
input_json = response.json()
print(input_json)
input_json = input_json["data"]

#     return woocommerce_json
def convert_to_woocommerce_json(data):

    woocommerce_json = []
    if "categories" in data:
        # Get categories
        categories_list = data["categories"]
        for category in categories_list:
            if "name" in category:
                woocommerce_category = {
                    "name": category["name"]
                }
                print(woocommerce_category)
                wcapi.post("products/categories", woocommerce_category).json()
            else:
                print("Category doesn't have a name:", category)
    else:
        print("No categories found in the input data.")

    return woocommerce_json


#  convert_to_woocommerce_json(input_json["data"])

product_data = {
    "category": "3WD",
    "title": "Premium Quality"
}

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
product = wcapi.get("products", params={"title": product_data["title"]}).json()
if not product:
    new_product_data = {
        'name': product_data['title'],
        'categories': [{'id': category_id}]
    }
    created_product = wcapi.post("products", new_product_data).json()
    print("Product created:", created_product)
else:
    product_id = product[0]['id']
    # Update existing product's category
    product_update_data = {
        'categories': [{'id': category_id}]
    }
    updated_product = wcapi.put(f"products/{product_id}", product_update_data).json()
    print("Product updated:", updated_product)