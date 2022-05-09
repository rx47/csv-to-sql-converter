import csv, glob, os


def read_csv_file(file_name):
    rows = []
    with open(file_name, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            rows.append(row)
    return rows

def create_sql_insert_statement(file_name):
    table_name = file_name.split(".")[0]
    rows = read_csv_file(file_name)
    headers = ",".join(rows[0])
    insert_line = "INSERT INTO " + table_name + " (" + headers + ") VALUES\n"
    entries = []

    for row in rows[1:]:
        value = "('" + "', '".join(row) + "'),"
        entries.append(value)

    entry_lines = "\n".join(entries)
    result = insert_line + entry_lines + ";"

    last_comma = result.replace(",;",";")[0:]
    return last_comma

def save_data_to_sql_file(csv_file_name):
    output_file_name = csv_file_name.split(".")[0]
    with open(output_file_name+".sql", "a") as f:
        print(create_sql_insert_statement(csv_file_name), file=f)

def get_csv_files_from_current_directory():
    os.getcwd()
    for file in glob.glob("*.csv"):
        save_data_to_sql_file(file)

if __name__ == "__main__":
    get_csv_files_from_current_directory()
