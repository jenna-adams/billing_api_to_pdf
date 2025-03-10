import requests
from datetime import datetime, timedelta
from collections import defaultdict
from fpdf import FPDF
from PIL import Image

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

# Group data by billing_code and summarize data
summarized_data = defaultdict(lambda: {
	"total_users": 0,
	"total_loads": 0,
	"users_with_telematics": 0,
	"billing_code": "",
	"months": set()
})

for record in data:
	billing_code = record.get("billing_code", "UNKNOWN")
	month = record.get("month", "UNKNOWN")
	telematics_enabled = record.get("telematics_enabled", False)
	
	# Ensure that unique_loads is treated as an integer
	unique_loads = int(record.get("unique_loads", 0))
	
	# Summing up data by billing_code
	summarized_data[billing_code]["total_users"] += 1
	summarized_data[billing_code]["total_loads"] += unique_loads
	if telematics_enabled:
		summarized_data[billing_code]["users_with_telematics"] += 1
	summarized_data[billing_code]["billing_code"] = billing_code
	summarized_data[billing_code]["months"].add(month)

# PDF Generation
def create_summary_pdf(summarized_data):
	pdf = FPDF()
	pdf.set_auto_page_break(auto=True, margin=15)
	pdf.add_page()
	pdf.set_font("Arial", "B", 16)

	# Add Company Logo (Make sure to replace with your actual logo file path)
	logo_path = "Your-Logo-here.png"
	
	# Use Pillow to get image size
	with Image.open(logo_path) as img:
		logo_width, logo_height = img.size  # Get the dimensions of the logo

	# Scale logo to fit width of page (e.g., 30mm width)
	max_logo_width = 30  # Maximum width of the logo (in mm)
	scale_factor = max_logo_width / logo_width
	logo_width = max_logo_width
	logo_height = int(logo_height * scale_factor)

	pdf.image(logo_path, x=10, y=8, w=logo_width, h=logo_height)  # Adjust size and position of logo

	# Dynamically adjust the space after the logo based on its height
	space_after_logo = logo_height + 10  # 10mm space after the logo
	pdf.ln(space_after_logo)  # Add dynamic space after the logo

	# Add Company Info below the logo
	pdf.set_font("Arial", "", 8)
	pdf.cell(200, 5, "Company Name - Address", ln=True, align="L")
	pdf.cell(200, 5, "Phone: (123) 456-7890 - Email: contact@company.com", ln=True, align="L")
	pdf.cell(200, 5, "Website: www.company.com", ln=True, align="L")
	pdf.ln(5)  # Add some space before the title

	# Title
	pdf.set_font("Arial", "B", 16) # set larger font for title
	title = "Billing Summary report"
	title_width = pdf.get_string_width(title)
	pdf.cell(title_width, 10, title, ln=True, align="L")
	
	# Table Headers
	pdf.set_font("Arial", "B", 12)
	headers = ["Month", "Total Users", "Total Loads", "Users with Telematics", "Billing Code"]

	# Calculate dynamic column widths based on header and data length
	column_widths = []
	for i, header in enumerate(headers):
		max_header_width = pdf.get_string_width(header)  # Width of the header
		max_data_width = 0

		column_widths.append(max(max_header_width, max_data_width) + 5)  # Add a little buffer (5mm)
	    
	# Center the table headers
	for i, header in enumerate(headers):
		pdf.cell(column_widths[i], 10, header, 1, 0, 'C')
	pdf.ln()

	# Table Content
	pdf.set_font("Arial", "", 12)
	for billing_code, data in summarized_data.items():
		for month in data["months"]:
			# Add data rows to the PDF
			pdf.cell(column_widths[0], 10, str(month), 1, 0, 'C')
			pdf.cell(column_widths[1], 10, str(data["total_users"]), 1, 0, 'C')
			pdf.cell(column_widths[2], 10, str(data["total_loads"]), 1, 0, 'C')
			pdf.cell(column_widths[3], 10, str(data["users_with_telematics"]), 1, 0, 'C')
			pdf.cell(column_widths[4], 10, str(data["billing_code"] or "null"), 1, 0, 'C')
			pdf.ln()

	pdf.output("billing_summary_report.pdf")

# Generate Summary PDF
create_summary_pdf(summarized_data)
print("Summary PDF generated!")

