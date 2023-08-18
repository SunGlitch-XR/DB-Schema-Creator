import tkinter as tk
from tkinter import filedialog

from ClassCreator import create_classes_from_csv  # Import the create_dtos_from_csv function
from DTOCreator import create_dtos_from_csv
from SchemaCreator import create_graph, read_csv, render_and_save, write_error_to_pdf

if __name__ == "__main__":
    csv_path = ""  # Initialize csv_path to an empty string
    try:
        root = tk.Tk()  # Corrected object creation
        root.withdraw()  # Hide the main window
        csv_path = filedialog.askopenfilename(title="Select a CSV file", filetypes=[("CSV files", "*.csv")])
        if csv_path:
            schema_df = read_csv(csv_path)
            dot = create_graph(schema_df)
            output_path = csv_path.rsplit('.', 1)[0]  # Remove the file extension
            render_and_save(dot, output_path)
            print("PDF generated successfully!")

            # Call the function to create .NET classes
            create_classes_from_csv(csv_path)

            # Call the function to create .NET DTOs
            create_dtos_from_csv(csv_path)  # Call to create DTOs

        else:
            print("No CSV file selected.")
    except Exception as e:
        error_message = str(e)
        print("An error occurred:", error_message)
        write_error_to_pdf(error_message, csv_path.rsplit('.', 1)[0] if csv_path else "error")
