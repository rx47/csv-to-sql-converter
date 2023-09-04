import csv, glob, os

def read_csv_file(file_name):
    """Read a CSV file and return its rows."""
    rows = []
    try:
        with open(file_name, 'r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                rows.append(row)
    except FileNotFoundError:
        print(f"Error: {file_name} not found.")
        return []
    except Exception as e:
        print(f"Error reading {file_name}: {e}")
        return []
    return rows

def infer_data_type(column_name, data):
    """Infer SQL data type based on column name and data."""
    if any(keyword in column_name.lower() for keyword in ["date", "time"]):
        return "DATE"
    if any(keyword in column_name.lower() for keyword in ["id", "num"]) and all(item.isdigit() for item in data):
        return "INT"
    if any("." in item for item in data):
        return "DECIMAL(10,2)"
    return "VARCHAR(255)"

def create_sql_table_statement(file_name):
    """Generate SQL CREATE TABLE statement based on CSV file."""
    table_name = os.path.basename(file_name).split(".")[0]
    rows = read_csv_file(file_name)

    if not rows:
        return

    headers = rows[0]
    column_definitions = []
    for i, header in enumerate(headers):
        column_data = [row[i] for row in rows[1:]]
        data_type = infer_data_type(header, column_data)
        column_definitions.append(f"`{header}` {data_type}")

    columns_str = ",\n".join(column_definitions)
    create_statement = "CREATE TABLE `{}` (\n{}\n);\n".format(table_name, columns_str)
    return create_statement

def create_sql_insert_statement(file_name):
    """Create an SQL INSERT statement for a given CSV file."""
    table_name = os.path.basename(file_name).split(".")[0]
    rows = read_csv_file(file_name)
    if len(rows) <= 1:
        return
    headers = "`,`".join(rows[0])

    # List of values considered as NULL
    null_values = ["null", "na", "n/a", ""]

    # Adjusting the formation of SQL values
    entries = []
    for row in rows[1:]:
        formatted_row = []
        for item in row:
            # Check if the item is considered as NULL
            if item.lower() in null_values:
                formatted_row.append("NULL")
            # Check if the item is numeric, including negative numbers and decimals
            elif item.lstrip('-').replace('.', '', 1).isdigit():
                formatted_row.append(item)
            # If it's alphanumeric or has special characters, enclose in quotes
            else:
                formatted_row.append(f"'{item}'")
        entries.append(f"({','.join(formatted_row)})")


    insert_line = f"INSERT INTO `{table_name}` (`{headers}`) VALUES\n"
    result = insert_line + ",\n".join(entries) + ";"
    return result



def save_data_to_sql_file(csv_file_name):
    """Save the generated SQL statements (CREATE and INSERT) into an .sql file."""
    create_statement = create_sql_table_statement(csv_file_name)
    insert_statement = create_sql_insert_statement(csv_file_name)

    if not create_statement or not insert_statement:
        return

    output_file_name = os.path.basename(csv_file_name).split(".")[0]
    with open(output_file_name + ".sql", "a") as f:
        print(create_statement, file=f)
        print(insert_statement, file=f)

def get_csv_files_from_current_directory():
    """Get all CSV files in the current directory and convert them to SQL."""
    for file in glob.glob("*.csv"):
        save_data_to_sql_file(file)

if __name__ == "__main__":
    print("Starting CSV to SQL conversion...")
    get_csv_files_from_current_directory()
    print("Conversion completed.")
