# Billing Summary Report Script

This script is here to help you quickly generate a **Billing Summary Report** in PDF format! It pulls billing data from the **Billing Usage API**, organizes it, and then neatly lays it out in a PDF so you can easily share it with your team or clients.

**Disclaimer:**  
This is a small side project meant to give you a head start on working with the **Billing Usage API** and generating billing summary reports. It's a starting point, so feel free to tweak, customize, and extend it to fit your specific needs. 

Find more detailed documentation for the **[Billing Usage API](https://dev.eleostech.com/platform/platform.html#tag/Billable-Usage)**.

## What it Does

- **Fetches data** from the **Billing Usage API**, so you don’t have to worry about manually gathering all the details.
- **Summarizes the data** by billing code, giving you a breakdown of total users, total loads, and how many users have telematics.
- **Creates a clean PDF** report with:
  - Your company logo at the top (so it looks professional).
  - A nicely formatted table with billing details for each month and billing code.
  - Dynamically adjusted column widths based on the longest data or header, so everything fits just right.
  - The report title "Billing Summary Report" aligned to the left (no fancy centering here!).
- Handles any missing data gracefully by filling in `"null"` for any missing values in the table, so you don’t have to worry about gaps.

## What You Need

Before you run this, make sure you have the following Python packages installed:

- `requests`: This grabs the data from the API.
- `fpdf`: This helps generate the PDF report.
- `Pillow (PIL)`: This handles your company logo image.

To install everything you need, just run:

```bash
pip install requests fpdf pillow
```

## How to Set It Up
1. First, make sure the API URL and your authorization headers are correct. You'll find these in the API_URL and HEADERS variables.
2. Don’t forget to add the path to your company logo image in the logo_path variable.

## Running the Script
Once everything is set up, run the script:

```bash
python billing_api_totaled_script.py
```
It’ll pull the data, process it, and generate a billing_summary_report.pdf file in the same folder. You’ll be able to open it right away and start using it!

## Customize It
Want to make the report your own? Here are a few easy ways to tweak it:

- Column widths: The script automatically adjusts the column widths based on the content. If you have very long data or headers, it’ll make sure they fit nicely.
- Company Info: You can change the company name, phone number, email, and address by editing the pdf.cell() lines in the script.
- Logo: Want to use a different logo? Just update the logo_path variable with your logo’s file path.
