# Sales Analytics System

A complete Python-based **Sales Analytics System** that performs data ingestion, cleaning, validation, analysis, API enrichment, and report generation using structured programming and modular design.

This project is built as per the given assignment specifications and follows proper folder structure, error handling, and reporting standards.

---

## 📌 Features

- File handling with multiple encoding support
- Data parsing, cleaning, and validation
- Interactive filtering (region & amount range)
- Sales analytics and performance metrics
- API integration using DummyJSON
- Sales data enrichment with API product info
- Text-based comprehensive report generation
- Modular, readable, and maintainable codebase

---

## 🗂 Project Structure

sales-analytics-system/
│
├── main.py
├── README.md
├── requirements.txt
│
├── data/
│ ├── sales_data.txt
│ └── enriched_sales_data.txt
│
├── output/
│ └── sales_report.txt
│
└── utils/
├── file_handler.py
├── data_processor.py
└── api_handler.py

yaml
Copy code

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository
git clone https://github.com/<your-username>/sales-analytics-system
cd sales-analytics-system
2️⃣ Install Dependencies
bash
Copy code
pip install -r requirements.txt
▶️ How to Run the Application
bash
Copy code
python main.py
🖥 Console Workflow
The application follows a step-by-step execution flow:

Reads sales data with encoding handling

Parses and cleans transactions

Displays filter options (region & amount range)

Validates transactions

Performs sales analysis

Fetches product data from DummyJSON API

Enriches sales data with API information

Saves enriched data to file

Generates a comprehensive sales report

📄 Output Files
After successful execution, the following files are generated:

📁 Enriched Sales Data
bash
Copy code
data/enriched_sales_data.txt
Contains original sales data along with API-enriched fields:

API_Category

API_Brand

API_Rating

API_Match

📁 Sales Report
bash
Copy code
output/sales_report.txt
Includes:

Overall summary

Region-wise performance

Top products & customers

Daily sales trend

Product performance analysis

API enrichment summary

🌐 API Used
DummyJSON Products API

arduino
Copy code
https://dummyjson.com/products
Used to fetch product details and enrich sales transactions.

📦 Dependencies
Listed in requirements.txt:

nginx
Copy code
requests
✅ Assignment Compliance
✔ Proper folder structure

✔ Modular utility files

✔ Encoding-safe file handling

✔ API integration with error handling

✔ No hardcoded file paths

✔ All required outputs generated

✔ Clean console output and logs

🧪 Tested Scenarios
Missing / invalid records

Encoding mismatches

API failures

Unmatched product IDs

Empty or malformed data rows

All errors are handled gracefully using try-except blocks.

👤 Author
ANIRUDH R

📌 Notes
Ensure sales_data.txt is present inside the data/ folder before running.

The repository must remain public until evaluation is completed.

