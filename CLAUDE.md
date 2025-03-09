# Project Guidelines

## Environment Setup
```
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install pandas matplotlib seaborn numpy openpyxl xlrd
```

## Commands
- Data analysis: `python analyze_excel.py`
- Generate report: Report is automatically generated in `report_output/`

## Conventions
- Code style: Follow PEP 8
- Function doc-strings: Use triple quotes with brief description
- Error handling: Use try/except blocks around file operations
- Naming: Use snake_case for variables and functions
- Imports: Group standard library, third-party, and local imports
- Always include type hints for function parameters and return values

## Project Structure
- Python scripts in root directory
- Reports generated in `report_output/`
- Visualizations in `report_output/visualizations/`