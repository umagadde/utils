from fpdf import FPDF
import pandas as pd
from fpdf.fonts import FontFace
import numpy as np
from datetime import datetime
# Your DataFrame
# df = pd.DataFrame({
#     "First name": ["Jules", "Mary", "Carlson", "Lucas"],
#     "Last name": ["Smith", "Ramos", "Banks", "Cimon"],
#     "Age": [34, 45, 19, 31],
#     "City": ["San Juan", "Orlando", "Los Angelesddddddddddddddddddddddddddddddddddddddddd", "Angers"]
# })
df=pd.read_csv("current.csv")
def process_csv_and_add_missing_columns(csv_path):
    # Read the CSV file into a DataFrame
    # csv_path="L2_architecture/data/Final_API.csv"
    df = pd.read_csv(csv_path)
    
    # Get today's date for Due_date comparison
    today = datetime.now().date()
    
    # Columns to check for missing values or specific conditions
    columns_to_check = [
         'parent_key', 'summary', 'description', 'acceptance_crieteria','fix_versions',
        'labels', 'components', 'story_points' ]
    
    def check_row(row):
        missing_cols = []
        
        # Check for missing values (NaN or empty strings)
        for col in columns_to_check:
            value = row[col]
            if pd.isna(value) or (isinstance(value, str) and value.strip() == ''):
                missing_cols.append(col)
        
        
        return ', '.join(missing_cols) if missing_cols else '-'
    
    # Apply the check_row function to each row
    df['Missing_Columns'] = df.apply(check_row, axis=1)
    return df
# key	issue_type	parent_key	project_key	fix_versions	status	sprint	sprint_status	priority	labels	assignee	components	description	summary	acceptance_crieteria	reporter	story_points	requested_by	employment_type

df=process_csv_and_add_missing_columns("current.csv")
#add a column missing fields check. if missing columns is empty then it should be PASSED else it should be FAILED
df['missing_fields_check'] = df['Missing_Columns'].apply(lambda x: 'PASSED' if x == '-' else 'FAILED') 
# df = df.drop(columns=["issue_type","parent_key","project_key","fix_versions",'status','sprint','sprint_status','priority','labels','assignee','components','description','acceptance_crieteria','reporter']) 
# Convert DataFrame to tuple of tuples, including headers
required_columns=['key','summary','missing_fields_check','Missing_Columns']
df = df[required_columns]  # Select only the required columns
TABLE_DATA = (tuple(df.columns),) + tuple(df.astype(str).itertuples(index=False, name=None))

# Create PDF
pdf = FPDF(orientation='L')  # 'L' for landscape orientation
pdf.add_page()
pdf.set_font("Times", size=12)

style_n= FontFace(emphasis="BOLD",color=(255, 0, 0),  family="Times")
style_y= FontFace(emphasis="BOLD",color=(0, 128, 0),  family="Times")
# Draw table
with pdf.table() as table:
    for data_row in TABLE_DATA:

        row = table.row()
        for datum in data_row:
            if datum=='FAILED':
                row.cell(datum, style=style_n)
            elif datum=='PASSED':
                row.cell(datum, style=style_y)
            else:
                row.cell(datum)
# Output PDF
pdf.output("table_from_df.pdf")

