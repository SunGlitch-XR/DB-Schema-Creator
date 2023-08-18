import pandas as pd
import os

# Function to convert SQL data types to corresponding .NET data types
def get_dotnet_type(sql_type):
    mapping = {
        "int": "int",
        "nvarchar": "string",
        "varchar": "string",
        "uniqueidentifier": "Guid",
        "datetime": "DateTime",
        "money": "decimal",
    }
    return mapping.get(sql_type, "object")

# Function to generate .NET class for a given table
def generate_class(table_name, columns):
    class_lines = []
    # Add necessary namespaces
    class_lines.append("using System;")
    class_lines.append("using System.ComponentModel.DataAnnotations;")
    class_lines.append("using System.ComponentModel.DataAnnotations.Schema;")
    class_lines.append("")  # Add an empty line for better readability
    class_lines.append("namespace DataModels;")
    class_lines.append("")  # Add an empty line for better readability
    class_lines.append(f"/// <summary>")
    class_lines.append(f"/// {table_name} table representation.")
    class_lines.append(f"/// </summary>")
    class_lines.append(f"public class {table_name}")
    class_lines.append("{")
    for column in columns:
        if column['is_primary_key'] == 'YES':
            class_lines.append("    [Key]")
        if column['is_foreign_key'] == 'YES':
            class_lines.append(f"    [ForeignKey(\"{column['referenced_table_name']}\")]")
        if column['is_nullable'] == 'NO':
            class_lines.append("    [Required]")
        class_lines.append(f"    /// <summary>")
        class_lines.append(f"    /// {column['column_name']} field.")
        class_lines.append(f"    /// </summary>")
        dotnet_type = get_dotnet_type(column['data_type'])
        class_lines.append(f"    public {dotnet_type} {column['column_name']} {{ get; set; }}")
        class_lines.append("")
    class_lines.append("}")
    return "\n".join(class_lines)

def create_classes_from_csv(csv_path):
    # Read the CSV file
    schema_df = pd.read_csv(csv_path)

    # Extract tables and their properties
    tables = {}
    for index, row in schema_df.iterrows():
        table_name = row['table_name']
        column_info = {
            'column_name': row['column_name'],
            'data_type': row['data_type'],
            'is_nullable': row['is_nullable'],
            'is_primary_key': row['is_primary_key'],
            'is_foreign_key': row['is_foreign_key'],
            'referenced_table_name': row['referenced_table_name'],
            'referenced_column_name': row['referenced_column_name'],
        }
        if table_name not in tables:
            tables[table_name] = []
        tables[table_name].append(column_info)

    # Get the directory of the CSV file
    csv_directory = os.path.dirname(csv_path)

    # Create a directory called Classes inside the CSV directory if it doesn't exist
    output_folder = os.path.join(csv_directory, 'Classes')
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

        # Generate the .NET classes
    for table_name, columns in tables.items():
        class_code = generate_class(table_name, columns)  # This function includes XML comments

        # Create a file with the class name inside the Classes folder
        file_name = os.path.join(output_folder, f'{table_name}.cs')
        with open(file_name, 'w') as file:
            file.write(class_code)

        print(f'{table_name} class written to {file_name}')


