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
