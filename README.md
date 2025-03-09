# Excel Data Analysis Tool

This tool analyzes Excel files and generates comprehensive reports with visualizations and insights.

## Features

- Loads data from Excel files
- Generates basic summary statistics
- Creates visualizations based on data types
- Identifies trends and patterns in the data
- Produces a markdown report with all findings

## Usage

1. Place your Excel file in the same directory as the script
2. Run the Python script:

```bash
python analyze_excel.py
```

3. View the generated report in the `report_output` directory

## Requirements

- Python 3.6+
- pandas
- matplotlib
- seaborn
- numpy

## Installation

It's recommended to install the required packages in a virtual environment:

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages
pip install pandas matplotlib seaborn numpy openpyxl xlrd
```

With uv (faster installation):
```bash
# Install using uv if available
uv pip install pandas matplotlib seaborn numpy openpyxl xlrd
```

Note: `openpyxl` is required for pandas to read Excel files.