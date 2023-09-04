# CSV to SQL Converter

This utility provides an efficient way to convert CSV files into SQL scripts. It automates the process of generating SQL `CREATE TABLE` and `INSERT` statements based on the data in your CSV files.

## Features

- **Automatic Table Creation**: Generates SQL statements to create tables named after the CSV files.
- **Dynamic Data Type Inference**: The utility intelligently infers SQL data types from the CSV data. For instance, columns with all integer values will be inferred as `INT`, and those with string values will be designated as `VARCHAR`.
- **Null Value Handling**: Recognizes various representations of null values (e.g., "null", "na", "n/a") and converts them to SQL `NULL`.

## Usage

1. Place the script in the directory containing your CSV files.
2. Execute the script. It will process all `.csv` files in the directory.
3. For each CSV file, an SQL file with the same name but with an `.sql` extension will be created. This SQL file contains the necessary statements to create a table and insert the data from the CSV file.

## Example

Given a CSV file named `users.csv` with the following content:

```
id,name,age
1,John,25
2,Alice,28
3,,30
```

The script will produce an `users.sql` file with the statements:

```sql
CREATE TABLE `users` (
`id` INT,
`name` VARCHAR(255),
`age` INT
);

INSERT INTO `users` (`id`,`name`,`age`)
VALUES
(1,'John',25),
(2,'Alice',28),
(3,NULL,30);
```

By using this script, you can quickly transform your CSV datasets into SQL-ready scripts, streamlining the process of integrating data into your databases.