
# CSV to SQL Converter

converts csv data to sql code

## Usage

Simply put the script in the folder with csv files and run it all files in that directory will be converted into sql files
to use it into you project for converting specific files import the following function from the script `from csv_to_sql_converter import save_data_to_sql_file` and insert the name of the file into the function `save_data_to_sql_file("insert_name_here.csv")`

#### v0.1
* fixed issues related to `sql format`

#### v0.2
* minor bugfixes
* fixed comma issue on the last line
* it has been replaced with `;`