import requests
from datetime import datetime, timedelta
from collections import defaultdict
from fpdf import FPDF

# API Credentials
API_URL = "https://platform.driveaxleapp.com/api/v1/usage?month=current"
HEADERS = {
	"Authorization": "Key key={your api key}",
	"Content-Type": "application/json"
}

# Fetch data
response = requests.get(API_URL, headers=HEADERS)

if response.status_code == 200:
	data = response.json()
	print("Data fetched successfully!")
else:
	print(f"Error: {response.status_code}, {response.text}")
	exit()

# Group data by billing_code
grouped_data = defaultdict(list)
for record in data:
	billing_code = record.get("billing_code", "UNKNOWN")
	grouped_data[billing_code].append(record)

# PDF Class
class PDF(FPDF):
	def header(self):
		self.set_font("Arial", "B", 14)
		self.cell(200, 10, "Billing Report", ln=True, align="C")
		self.ln(10)

def create_pdf(billing_code, records):
	pdf = PDF(orientation='P', unit='mm', format='A4')  # Portrait mode
	pdf.set_auto_page_break(auto=True, margin=10)
	pdf.add_page()
	pdf.set_font("Arial", "B", 9)

	# Column Headers (Adjusted widths to fit A4 portrait)
	column_widths = [20, 35, 15, 15, 15, 20, 40, 20]  # Adjusted widths
	headers = ["Month", "Username", "Telem.", "Days", "Loads", "Bill Code", "Description", "Type"]

	for i in range(len(headers)):
		pdf.cell(column_widths[i], 8, headers[i], 1, 0, "C")
	pdf.ln()

	# Table Content
	pdf.set_font("Arial", "", 8)

	for record in records:
		# Determine max row height based on wrapped text in description
		desc_text = str(record["billing_description"])
		desc_width = column_widths[6]
		line_height = 5  # Adjust line height if needed
		desc_height = pdf.get_string_width(desc_text) / desc_width * line_height + line_height
		row_height = max(8, desc_height)  # Ensure all columns match this height

		# Capture current X, Y before writing the row
		x = pdf.get_x()
		y = pdf.get_y()

		# Print normal cells first
		pdf.cell(column_widths[0], row_height, str(record["month"]), 1)
		pdf.cell(column_widths[1], row_height, str(record["username"]), 1)
		pdf.cell(column_widths[2], row_height, str(record["telematics_enabled"]), 1)
		pdf.cell(column_widths[3], row_height, str(record["days_used"]), 1)
		pdf.cell(column_widths[4], row_height, str(record["unique_loads"]), 1)
		pdf.cell(column_widths[5], row_height, str(record["billing_code"]), 1)

		# MultiCell for Description (ensures wrapping without breaking the table)
		pdf.set_xy(x + sum(column_widths[:6]), y)  # Move to correct X before writing multi-cell
		pdf.multi_cell(column_widths[6], row_height, desc_text, border=1)

		# Ensure the next column aligns by resetting the Y position
		pdf.set_xy(x + sum(column_widths[:7]), y)
		pdf.cell(column_widths[7], row_height, str(record["billing_type"]), 1)

		# Move to the next row manually
		pdf.ln(row_height)

	pdf.output(f"billing_report_{billing_code}.pdf")
	print(f"PDF created for {billing_code}")

# Generate PDFs
for billing_code, records in grouped_data.items():
	create_pdf(billing_code, records)

print("All PDFs generated!")
