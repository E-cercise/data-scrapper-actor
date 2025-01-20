import time
import json
from apify_client import ApifyClient
from dotenv import dotenv_values

config = config = dotenv_values(".env")

apify_token = config.get("APIFY_TOKEN", "")


if apify_token == "":
    raise KeyError("no apify token, please set it in environment variable")

print(apify_token)

# Initialize Apify Client
client = ApifyClient(apify_token)

def run_actor_1():
    # Step 1: Run the ASIN Scraper Actor (Actor 1)
    print("Running ASIN Scraper Actor...")
    run = client.actor("junglee/Amazon-crawler").call(
        run_input={
    
    "categoryOrProductUrls": [


        {
            "url": "https://www.amazon.com/s?k=Pull-Up+Bar",
            "method": "GET"
        },
        # {
        #     "url": "https://www.amazon.com/s?k=Assisted+Pull-Up+Machine",
        #     "method": "GET"
        # },
                # {
        #     "url": "https://www.amazon.com/s?k=Chest+Press+Machine",
        #     "method": "GET"
        # }
    ],
    "maxItemsPerStartUrl": 100,
    "maxOffers": 0,
    "proxyCountry": "AUTO_SELECT_PROXY_COUNTRY",
    "scrapeProductDetails": True,
    "scrapeProductVariantPrices": True,
    "scrapeSellers": False,
    "useCaptchaSolver": False
    }
    )

    # Wait for Actor 1 to finish
    print("Waiting for ASIN Scraper Actor to finish...")
    while True:
        status = client.run(run['id']).get()['status']
        if status == "SUCCEEDED":
            print("ASIN Scraper Actor finished.")
            break
        time.sleep(5)

    # Retrieve ASINs from the dataset
    dataset_id = run['defaultDatasetId']
    dataset_items = client.dataset(dataset_id).list_items()
    print(dataset_items)
    asin_list = [item['asin'] for item in dataset_items.items]
    print(f"Found {len(asin_list)} ASINs: {asin_list}")
    return asin_list

def run_actor_2(asin_list):
    # Step 2: Run the Product Detail Scraper Actor (Actor 2)
    print("Running Product Detail Scraper Actor...")
    run = client.actor("junglee/amazon-asins-scraper").call(
        run_input={
    "amazonDomain": "amazon.com",
    "asins": asin_list,
    "proxyCountry": "AUTO_SELECT_PROXY_COUNTRY",
    "useCaptchaSolver": False
    }
    )

    # Wait for Actor 2 to finish
    print("Waiting for Product Detail Scraper Actor to finish...")
    while True:
        status = client.run(run['id']).get()['status']
        if status == "SUCCEEDED":
            print("Product Detail Scraper Actor finished.")
            break
        time.sleep(5)

    # Retrieve product details from the dataset
    dataset_id = run['defaultDatasetId']
    product_details = client.dataset(dataset_id).list_items()
    print(f"Retrieved {len(product_details.items)} product details.")
    return product_details.items

def dump_to_json(data, filename='data/pull_up_bar.json'):
    # Dump the product details to a JSON file
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    print(f"Product details have been saved to {filename}")

def main():
    # try:
    # Run Actor 1 and fetch ASINs
    asin_list = run_actor_1()

    if not asin_list:
        print("No ASINs found. Exiting...")
        return

    # Run Actor 2 and fetch product details
    product_details = run_actor_2(asin_list)

    # Output the results
    for product in product_details:
        # print(f"Product: {product['title']}, Price: {product['price']}, ASIN: {product['asin']}")
        print(f"got products: {product}")

    # Dump the product details to a JSON file
    dump_to_json(product_details)

    # except Exception as e:
    #     print(f"Error occurred: {e}")

if __name__ == "__main__":
    main()
