# Function to generate .NET DTO class for a given table
import os

import pandas as pd

from ClassCreator import get_dotnet_type


def generate_dto_class(table_name, columns):
    dto_lines = []
    # Add necessary namespaces
    dto_lines.append("using System.ComponentModel.DataAnnotations;")
    dto_lines.append("using System.ComponentModel.DataAnnotations.Schema;")
    dto_lines.append("")  # Add an empty line for better readability
    dto_lines.append("namespace DTOs;")
    dto_lines.append("")  # Add an empty line for better readability
    dto_lines.append(f"/// <summary>")
    dto_lines.append(f"/// {table_name} DTO representation.")
    dto_lines.append(f"/// </summary>")
    dto_lines.append(f"public class {table_name}DTO")
    dto_lines.append("{")
    for column in columns:
        if column['is_nullable'] == 'NO':
            dto_lines.append("    [Required]")
        if column['data_type'] in ['nvarchar', 'varchar'] and 'max_length' in column:
            dto_lines.append(f"    [StringLength({column['max_length']})]")
        if column['is_primary_key'] == 'YES':
            dto_lines.append("    [Key]")
        if column['is_foreign_key'] == 'YES':
            dto_lines.append(f"    [ForeignKey(\"{column['referenced_table_name']}\")]")
        # Add more annotations based on the column properties as needed

        dto_lines.append(f"    /// <summary>")
        dto_lines.append(f"    /// {column['column_name']} field.")
        dto_lines.append(f"    /// </summary>")
        dotnet_type = get_dotnet_type(column['data_type'])
        dto_lines.append(f"    public {dotnet_type} {column['column_name']} {{ get; set; }}")
        dto_lines.append("")
    dto_lines.append("}")
    return "\n".join(dto_lines)




def create_dtos_from_csv(csv_path):
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

    # Create a directory called DTOS if it doesn't exist
    output_folder = os.path.join(os.path.dirname(csv_path), 'DTOS')
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Generate the DTOs
    for table_name, columns in tables.items():
        dto_code = generate_dto_class(table_name, columns)  # You need to define this function

        # Create a file with the class name inside the DTOS folder
        file_name = f'{output_folder}/{table_name}DTO.cs'
        with open(file_name, 'w') as file:
            file.write(dto_code)

        print(f'{table_name} DTO written to {file_name}')
