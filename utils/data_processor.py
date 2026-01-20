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
