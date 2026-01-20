from utils.file_handler import read_sales_file
from utils.data_processor import clean_and_process_data
from utils.api_handler import fetch_product_details

DATA_FILE = "data/sales_data.txt"

def main():
    raw_data = read_sales_file(DATA_FILE)
    cleaned_data = clean_and_process_data(raw_data)

    if cleaned_data:
        product_id = cleaned_data[0]["ProductID"]
        print(fetch_product_details(product_id))

if __name__ == "__main__":
    main()

