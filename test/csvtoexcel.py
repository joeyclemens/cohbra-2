import os
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

def csv_to_excel(csv_files, output_file):
    # Create an Excel workbook object
    workbook = Workbook()
    
    # Iterate over the CSV files
    for csv_file in csv_files:
        # Read the CSV file into a Pandas DataFrame
        df = pd.read_csv(csv_file)
        
        # Extract the file name without the extension
        sheet_name = os.path.splitext(os.path.basename(csv_file))[0]
        
        # Create a worksheet in the workbook
        worksheet = workbook.create_sheet(title=sheet_name)
        
        # Write the DataFrame to the worksheet
        for row in dataframe_to_rows(df, index=False, header=True):
            worksheet.append(row)
    
    # Remove the default sheet created by openpyxl
    workbook.remove(workbook["Sheet"])
    
    # Save the Excel file
    workbook.save(output_file)
    print(f'Successfully created {output_file}')

# Function to get all CSV files in a given folder
def get_csv_files(folder):
    csv_files = []
    for file in os.listdir(folder):
        if file.endswith('.csv'):
            csv_files.append(os.path.join(folder, file))
    return csv_files

# Example usage
folder_path = 'C:/Users/Joey/Desktop/Github/cohbra/test/csv'
output_file = 'combined.xlsx'
csv_files = get_csv_files(folder_path)
csv_to_excel(csv_files, output_file)
