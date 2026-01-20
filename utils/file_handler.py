def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues

    Returns: list of raw lines (strings)
    """

    encodings = ["utf-8", "latin-1", "cp1252"]

    for enc in encodings:
        try:
            with open(filename, "r", encoding=enc) as file:
                lines = file.readlines()
                break
        except UnicodeDecodeError:
            continue
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return []
    else:
        print("Error: Unable to read file with supported encodings.")
        return []

    cleaned_lines = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith("TransactionID"):
            continue
        cleaned_lines.append(line)

    return cleaned_lines
