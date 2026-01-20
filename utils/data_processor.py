def clean_and_process_data(raw_records):
    total = 0
    invalid = 0
    valid_records = []

    for record in raw_records:
        total += 1
        fields = record.split("|")

        if len(fields) != 8:
            invalid += 1
            continue

        txn_id, date, pid, pname, qty, price, cid, region = fields

        if not txn_id.startswith("T"):
            invalid += 1
            continue

        if not cid or not region:
            invalid += 1
            continue

        try:
            qty = int(qty.replace(",", ""))
            price = float(price.replace(",", ""))
        except ValueError:
            invalid += 1
            continue

        if qty <= 0 or price <= 0:
            invalid += 1
            continue

        valid_records.append({
            "TransactionID": txn_id,
            "Date": date,
            "ProductID": pid,
            "ProductName": pname,
            "Quantity": qty,
            "UnitPrice": price,
            "CustomerID": cid,
            "Region": region
        })

    print(f"Total records parsed: {total}")
    print(f"Invalid records removed: {invalid}")
    print(f"Valid records after cleaning: {len(valid_records)}")

    return valid_records

