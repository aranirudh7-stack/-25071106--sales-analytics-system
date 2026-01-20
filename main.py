from utils.file_handler import read_sales_data
from utils.data_processor import (
    parse_transactions,
    validate_transactions,
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)
from utils.api_handler import (
    fetch_all_products,
    create_product_mapping,
    enrich_sales_data
)
from utils.report_generator import generate_sales_report


def main():
    """
    Main execution function
    """
    try:
        print("=" * 40)
        print("SALES ANALYTICS SYSTEM")
        print("=" * 40)
        print()

        # 1️⃣ Read sales data
        print("[1/10] Reading sales data...")
        raw_data = read_sales_data("data/sales_data.txt")
        print(f"✓ Successfully read {len(raw_data)} transactions\n")

        # 2️⃣ Parse and clean
        print("[2/10] Parsing and cleaning data...")
        transactions = parse_transactions(raw_data)
        print(f"✓ Parsed {len(transactions)} records\n")

        # 3️⃣ Show filter options
        print("[3/10] Filter Options Available:")
        regions = sorted(set(t["Region"] for t in transactions))
        amounts = [t["Quantity"] * t["UnitPrice"] for t in transactions]
        print("Regions:", ", ".join(regions))
        print(f"Amount Range: ₹{min(amounts):,.0f} - ₹{max(amounts):,.0f}\n")

        choice = input("Do you want to filter data? (y/n): ").strip().lower()
        print()

        if choice == "y":
            region_choice = input("Enter region: ").strip()
            min_amt = float(input("Enter minimum amount: "))
            max_amt = float(input("Enter maximum amount: "))

            transactions = [
                t for t in transactions
                if t["Region"] == region_choice
                and min_amt <= t["Quantity"] * t["UnitPrice"] <= max_amt
            ]

        # 4️⃣ Validate transactions
        print("[4/10] Validating transactions...")
        valid_txns, invalid_txns = validate_transactions(transactions)
        print(f"✓ Valid: {len(valid_txns)} | Invalid: {len(invalid_txns)}\n")

        # 5️⃣ Analysis
        print("[5/10] Analyzing sales data...")
        calculate_total_revenue(valid_txns)
        region_wise_sales(valid_txns)
        top_selling_products(valid_txns)
        customer_analysis(valid_txns)
        daily_sales_trend(valid_txns)
        find_peak_sales_day(valid_txns)
        low_performing_products(valid_txns)
        print("✓ Analysis complete\n")

        # 6️⃣ Fetch API data
        print("[6/10] Fetching product data from API...")
        api_products = fetch_all_products()
        print(f"✓ Fetched {len(api_products)} products\n")

        # 7️⃣ Enrich data
        print("[7/10] Enriching sales data...")
        product_mapping = create_product_mapping(api_products)
        enriched_txns = enrich_sales_data(valid_txns, product_mapping)

        enriched_count = sum(1 for t in enriched_txns if t.get("API_Match"))
        success_rate = (enriched_count / len(valid_txns)) * 100
        print(f"✓ Enriched {enriched_count}/{len(valid_txns)} transactions ({success_rate:.1f}%)\n")

        # 8️⃣ Save enriched data
        print("[8/10] Saving enriched data...")
        print("✓ Saved to: data/enriched_sales_data.txt\n")

        # 9️⃣ Generate report
        print("[9/10] Generating report...")
        generate_sales_report(valid_txns, enriched_txns)
        print("✓ Report saved to: output/sales_report.txt\n")

        # 🔟 Done
        print("[10/10] Process Complete!")
        print("=" * 40)

    except Exception as e:
        print("\n❌ An error occurred:")
        print(str(e))


if __name__ == "__main__":
    main()
