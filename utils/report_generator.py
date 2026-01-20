from datetime import datetime
from collections import defaultdict
def generate_sales_report(transactions, enriched_transactions, output_file="output/sales_report.txt"):
    """
    Generates a comprehensive formatted text report
    """

    # ---------- BASIC METRICS ----------
    total_transactions = len(transactions)
    total_revenue = sum(t["Quantity"] * t["UnitPrice"] for t in transactions)
    avg_order_value = total_revenue / total_transactions if total_transactions else 0

    dates = sorted(t["Date"] for t in transactions)
    start_date, end_date = dates[0], dates[-1]

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ---------- REGION-WISE PERFORMANCE ----------
    region_data = defaultdict(lambda: {"sales": 0, "count": 0})

    for t in transactions:
        revenue = t["Quantity"] * t["UnitPrice"]
        region_data[t["Region"]]["sales"] += revenue
        region_data[t["Region"]]["count"] += 1

    region_rows = []
    for region, data in region_data.items():
        percent = (data["sales"] / total_revenue) * 100
        region_rows.append((region, data["sales"], percent, data["count"]))

    region_rows.sort(key=lambda x: x[1], reverse=True)

    # ---------- TOP 5 PRODUCTS ----------
    product_data = defaultdict(lambda: {"qty": 0, "revenue": 0})

    for t in transactions:
        product_data[t["ProductName"]]["qty"] += t["Quantity"]
        product_data[t["ProductName"]]["revenue"] += t["Quantity"] * t["UnitPrice"]

    top_products = sorted(
        product_data.items(),
        key=lambda x: x[1]["qty"],
        reverse=True
    )[:5]

    # ---------- TOP 5 CUSTOMERS ----------
    customer_data = defaultdict(lambda: {"spent": 0, "count": 0})

    for t in transactions:
        amount = t["Quantity"] * t["UnitPrice"]
        customer_data[t["CustomerID"]]["spent"] += amount
        customer_data[t["CustomerID"]]["count"] += 1

    top_customers = sorted(
        customer_data.items(),
        key=lambda x: x[1]["spent"],
        reverse=True
    )[:5]

    # ---------- DAILY SALES TREND ----------
    daily_data = defaultdict(lambda: {"revenue": 0, "count": 0, "customers": set()})

    for t in transactions:
        date = t["Date"]
        daily_data[date]["revenue"] += t["Quantity"] * t["UnitPrice"]
        daily_data[date]["count"] += 1
        daily_data[date]["customers"].add(t["CustomerID"])

    daily_rows = sorted(daily_data.items())

    # ---------- PRODUCT PERFORMANCE ----------
    best_day = max(daily_rows, key=lambda x: x[1]["revenue"])

    low_products = [
        (p, d["qty"], d["revenue"])
        for p, d in product_data.items()
        if d["qty"] < 10
    ]

    region_avg_txn = {
        r: region_data[r]["sales"] / region_data[r]["count"]
        for r in region_data
    }

    # ---------- API ENRICHMENT SUMMARY ----------
    enriched_count = sum(1 for t in enriched_transactions if t.get("API_Match"))
    success_rate = (enriched_count / len(enriched_transactions)) * 100 if enriched_transactions else 0

    failed_products = sorted({
        t["ProductID"]
        for t in enriched_transactions
        if not t.get("API_Match")
    })

    # ---------- WRITE REPORT ----------
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("=" * 50 + "\n")
        f.write("        SALES ANALYTICS REPORT\n")
        f.write(f"      Generated: {now}\n")
        f.write(f"      Records Processed: {total_transactions}\n")
        f.write("=" * 50 + "\n\n")

        f.write("OVERALL SUMMARY\n")
        f.write("-" * 50 + "\n")
        f.write(f"Total Revenue:        ₹{total_revenue:,.2f}\n")
        f.write(f"Total Transactions:   {total_transactions}\n")
        f.write(f"Average Order Value:  ₹{avg_order_value:,.2f}\n")
        f.write(f"Date Range:           {start_date} to {end_date}\n\n")

        f.write("REGION-WISE PERFORMANCE\n")
        f.write("-" * 50 + "\n")
        f.write(f"{'Region':<10}{'Sales':<15}{'% of Total':<12}{'Transactions'}\n")
        for r, sales, pct, cnt in region_rows:
            f.write(f"{r:<10}₹{sales:,.0f}     {pct:>6.2f}%      {cnt}\n")
        f.write("\n")

        f.write("TOP 5 PRODUCTS\n")
        f.write("-" * 50 + "\n")
        f.write("Rank  Product        Quantity  Revenue\n")
        for i, (p, d) in enumerate(top_products, 1):
            f.write(f"{i:<5} {p:<14}{d['qty']:<10}₹{d['revenue']:,.2f}\n")
        f.write("\n")

        f.write("TOP 5 CUSTOMERS\n")
        f.write("-" * 50 + "\n")
        f.write("Rank  CustomerID   Total Spent   Orders\n")
        for i, (c, d) in enumerate(top_customers, 1):
            f.write(f"{i:<5} {c:<12}₹{d['spent']:,.2f}   {d['count']}\n")
        f.write("\n")

        f.write("DAILY SALES TREND\n")
        f.write("-" * 50 + "\n")
        f.write("Date        Revenue       Transactions  Unique Customers\n")
        for date, d in daily_rows:
            f.write(
                f"{date}  ₹{d['revenue']:,.2f}      {d['count']:<13} {len(d['customers'])}\n"
            )
        f.write("\n")

        f.write("PRODUCT PERFORMANCE ANALYSIS\n")
        f.write("-" * 50 + "\n")
        f.write(f"Best Selling Day: {best_day[0]} (₹{best_day[1]['revenue']:,.2f})\n")

        if low_products:
            f.write("Low Performing Products:\n")
            for p, q, r in low_products:
                f.write(f"- {p} (Qty: {q}, Revenue: ₹{r:,.2f})\n")
        else:
            f.write("Low Performing Products: None\n")

        f.write("\nAverage Transaction Value per Region:\n")
        for r, v in region_avg_txn.items():
            f.write(f"- {r}: ₹{v:,.2f}\n")
        f.write("\n")

        f.write("API ENRICHMENT SUMMARY\n")
        f.write("-" * 50 + "\n")
        f.write(f"Total Products Enriched: {enriched_count}\n")
        f.write(f"Success Rate: {success_rate:.2f}%\n")

        if failed_products:
            f.write("Products Not Enriched: " + ", ".join(failed_products) + "\n")
        else:
            f.write("Products Not Enriched: None\n")
