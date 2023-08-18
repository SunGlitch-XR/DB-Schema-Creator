import pandas as pd
from graphviz import Digraph
import tkinter as tk
from tkinter import filedialog

def read_csv(file_path):
    return pd.read_csv(file_path)

def create_graph(schema_df):
    dot = Digraph('DatabaseSchema')

    # Add tables as nodes
    for table in schema_df['table_name'].unique():
        columns = schema_df[schema_df['table_name'] == table]
        label = '{' + table + '|'
        for _, column in columns.iterrows():
            label += column['column_name'] + ': ' + column['data_type'] + '\\l'
        label += '}'
        dot.node(table, label, shape='record')

    # Add relationships as edges
    for _, row in schema_df.iterrows():
        if row['is_foreign_key'] == 'YES':
            dot.edge(row['table_name'], row['referenced_table_name'], label=row['column_name'])

    return dot

def render_and_save(dot, output_path):
    dot.render(output_path, view=True)

def select_csv_and_generate_pdf():
    root = tk.Tk()
    root.withdraw() # Hide the main window
    csv_path = filedialog.askopenfilename(title="Select a CSV file", filetypes=[("CSV files", "*.csv")])
    if csv_path:
        schema_df = read_csv(csv_path)
        dot = create_graph(schema_df)
        output_path = csv_path.rsplit('.', 1)[0] # Remove the file extension
        render_and_save(dot, output_path)
        print("PDF generated successfully!")
    else:
        print("No CSV file selected.")

if __name__ == "__main__":
    select_csv_and_generate_pdf()
