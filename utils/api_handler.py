def fetch_product_details(product_id):
    return {
        "product_id": product_id,
        "category": "Electronics",
        "rating": 4.3
    }

def fetch_all_products():
    """
    Fetches all products from DummyJSON API
    """
    url = "https://dummyjson.com/products?limit=100"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        products = data.get("products", [])

        print("API fetch successful")
        return products

    except Exception as e:
        print("API fetch failed:", e)
        return []
        
def create_product_mapping(api_products):
    """
    Creates a mapping of product IDs to product info
    """
    product_mapping = {}

    for product in api_products:
        try:
            product_id = product.get("id")
            if product_id is None:
                continue

            product_mapping[product_id] = {
                "title": product.get("title"),
                "category": product.get("category"),
                "brand": product.get("brand"),
                "rating": product.get("rating")
            }
        except Exception:
            continue

    return product_mapping
    def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transaction data with API product information
    """
    enriched_transactions = []

    for txn in transactions:
        enriched_txn = txn.copy()

        try:
            # Extract numeric product ID (P101 → 101)
            product_id_str = txn.get("ProductID", "")
            numeric_id = int(product_id_str[1:])

            if numeric_id in product_mapping:
                api_product = product_mapping[numeric_id]

                enriched_txn["API_Category"] = api_product.get("category")
                enriched_txn["API_Brand"] = api_product.get("brand")
                enriched_txn["API_Rating"] = api_product.get("rating")
                enriched_txn["API_Match"] = True
            else:
                enriched_txn["API_Category"] = None
                enriched_txn["API_Brand"] = None
                enriched_txn["API_Rating"] = None
                enriched_txn["API_Match"] = False

        except Exception:
            enriched_txn["API_Category"] = None
            enriched_txn["API_Brand"] = None
            enriched_txn["API_Rating"] = None
            enriched_txn["API_Match"] = False

        enriched_transactions.append(enriched_txn)

    # Save to file
    save_enriched_data(enriched_transactions)

    return enriched_transactions

def save_enriched_data(enriched_transactions, filename="data/enriched_sales_data.txt"):
    """
    Saves enriched transactions back to file
    """
    header = [
        "TransactionID", "Date", "ProductID", "ProductName",
        "Quantity", "UnitPrice", "CustomerID", "Region",
        "API_Category", "API_Brand", "API_Rating", "API_Match"
    ]

    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write("|".join(header) + "\n")

            for txn in enriched_transactions:
                row = [
                    str(txn.get("TransactionID", "")),
                    str(txn.get("Date", "")),
                    str(txn.get("ProductID", "")),
                    str(txn.get("ProductName", "")),
                    str(txn.get("Quantity", "")),
                    str(txn.get("UnitPrice", "")),
                    str(txn.get("CustomerID", "")),
                    str(txn.get("Region", "")),
                    str(txn.get("API_Category", "")),
                    str(txn.get("API_Brand", "")),
                    str(txn.get("API_Rating", "")),
                    str(txn.get("API_Match", ""))
                ]

                file.write("|".join(row) + "\n")

        print("Enriched data saved successfully")

    except Exception as e:
        print("Failed to save enriched data:", e)
