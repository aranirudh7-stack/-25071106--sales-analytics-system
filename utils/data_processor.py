def parse_transactions(raw_lines):
    """
    Parses raw lines into clean list of dictionaries
    """

    transactions = []

    for line in raw_lines:
        parts = line.split("|")

        if len(parts) != 8:
            continue

        txn_id, date, pid, pname, qty, price, cid, region = parts

        # Clean product name (keep text, remove commas)
        pname = pname.replace(",", " ")

        try:
            qty = int(qty.replace(",", ""))
            price = float(price.replace(",", ""))
        except ValueError:
            continue

        transactions.append({
            "TransactionID": txn_id,
            "Date": date,
            "ProductID": pid,
            "ProductName": pname,
            "Quantity": qty,
            "UnitPrice": price,
            "CustomerID": cid,
            "Region": region
        })

    return transactions
def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    valid_transactions = []
    invalid_count = 0

    regions = set()
    amounts = []

    for txn in transactions:
        try:
            if (
                not txn["TransactionID"].startswith("T")
                or not txn["ProductID"].startswith("P")
                or not txn["CustomerID"].startswith("C")
                or txn["Quantity"] <= 0
                or txn["UnitPrice"] <= 0
            ):
                invalid_count += 1
                continue

            amount = txn["Quantity"] * txn["UnitPrice"]
            regions.add(txn["Region"])
            amounts.append(amount)

            valid_transactions.append(txn)

        except KeyError:
            invalid_count += 1

    print("Available regions:", sorted(regions))
    if amounts:
        print("Transaction amount range:", min(amounts), "-", max(amounts))

    # Apply filters
    filtered = valid_transactions

    if region:
        filtered = [t for t in filtered if t["Region"] == region]
        print(f"After region filter ({region}):", len(filtered))

    if min_amount is not None:
        filtered = [
            t for t in filtered if t["Quantity"] * t["UnitPrice"] >= min_amount
        ]
        print("After min amount filter:", len(filtered))

    if max_amount is not None:
        filtered = [
            t for t in filtered if t["Quantity"] * t["UnitPrice"] <= max_amount
        ]
        print("After max amount filter:", len(filtered))

    summary = {
        "total_input": len(transactions),
        "invalid": invalid_count,
        "final_count": len(filtered)
    }

    return filtered, invalid_count, summary
    
def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions
    """
    total_revenue = 0.0
    for txn in transactions:
        total_revenue += txn["Quantity"] * txn["UnitPrice"]
    return round(total_revenue, 2)
    
def region_wise_sales(transactions):
    region_data = {}
    total_sales = 0.0

    for txn in transactions:
        region = txn["Region"]
        revenue = txn["Quantity"] * txn["UnitPrice"]

        if region not in region_data:
            region_data[region] = {
                "total_sales": 0.0,
                "transaction_count": 0
            }

        region_data[region]["total_sales"] += revenue
        region_data[region]["transaction_count"] += 1
        total_sales += revenue

    for region in region_data:
        percentage = (region_data[region]["total_sales"] / total_sales) * 100
        region_data[region]["percentage"] = round(percentage, 2)

    # Sort by total_sales descending
    sorted_regions = dict(
        sorted(
            region_data.items(),
            key=lambda x: x[1]["total_sales"],
            reverse=True
        )
    )

    return sorted_regions
def top_selling_products(transactions, n=5):
    product_data = {}

    for txn in transactions:
        product = txn["ProductName"]
        qty = txn["Quantity"]
        revenue = qty * txn["UnitPrice"]

        if product not in product_data:
            product_data[product] = {
                "quantity": 0,
                "revenue": 0.0
            }

        product_data[product]["quantity"] += qty
        product_data[product]["revenue"] += revenue

    result = [
        (product, data["quantity"], round(data["revenue"], 2))
        for product, data in product_data.items()
    ]

    result.sort(key=lambda x: x[1], reverse=True)

    return result[:n]
def customer_analysis(transactions):
    customer_data = {}

    for txn in transactions:
        cid = txn["CustomerID"]
        amount = txn["Quantity"] * txn["UnitPrice"]
        product = txn["ProductName"]

        if cid not in customer_data:
            customer_data[cid] = {
                "total_spent": 0.0,
                "purchase_count": 0,
                "products_bought": set()
            }

        customer_data[cid]["total_spent"] += amount
        customer_data[cid]["purchase_count"] += 1
        customer_data[cid]["products_bought"].add(product)

    # Final formatting
    final_data = {}
    for cid, data in customer_data.items():
        avg_order_value = data["total_spent"] / data["purchase_count"]

        final_data[cid] = {
            "total_spent": round(data["total_spent"], 2),
            "purchase_count": data["purchase_count"],
            "avg_order_value": round(avg_order_value, 2),
            "products_bought": list(data["products_bought"])
        }

    # Sort by total_spent descending
    sorted_customers = dict(
        sorted(
            final_data.items(),
            key=lambda x: x[1]["total_spent"],
            reverse=True
        )
    )

    return sorted_customers
def daily_sales_trend(transactions):
    daily_data = {}

    for txn in transactions:
        date = txn["Date"]
        revenue = txn["Quantity"] * txn["UnitPrice"]
        customer = txn["CustomerID"]

        if date not in daily_data:
            daily_data[date] = {
                "revenue": 0.0,
                "transaction_count": 0,
                "customers": set()
            }

        daily_data[date]["revenue"] += revenue
        daily_data[date]["transaction_count"] += 1
        daily_data[date]["customers"].add(customer)

    # Format result
    result = {}
    for date in sorted(daily_data.keys()):
        result[date] = {
            "revenue": round(daily_data[date]["revenue"], 2),
            "transaction_count": daily_data[date]["transaction_count"],
            "unique_customers": len(daily_data[date]["customers"])
        }

    return result
def find_peak_sales_day(transactions):
    daily = daily_sales_trend(transactions)

    peak_date = None
    max_revenue = 0
    txn_count = 0

    for date, data in daily.items():
        if data["revenue"] > max_revenue:
            max_revenue = data["revenue"]
            txn_count = data["transaction_count"]
            peak_date = date

    return (peak_date, max_revenue, txn_count)
def low_performing_products(transactions, threshold=10):
    product_data = {}

    for txn in transactions:
        product = txn["ProductName"]
        qty = txn["Quantity"]
        revenue = qty * txn["UnitPrice"]

        if product not in product_data:
            product_data[product] = {
                "quantity": 0,
                "revenue": 0.0
            }

        product_data[product]["quantity"] += qty
        product_data[product]["revenue"] += revenue

    low_products = [
        (product, data["quantity"], round(data["revenue"], 2))
        for product, data in product_data.items()
        if data["quantity"] < threshold
    ]

    low_products.sort(key=lambda x: x[1])

    return low_products


