# PDF Largest Number Finder

This program analyzes a provided PDF file to find the largest number present in the document. It can handle a decent number of number formats and has some heuristics for understanding natural numbers, but likely would struggle to work on documents outside of the example one provided. It does not take into account units, like comparings milliliters to liters.

## Features

- Parses PDF files and extracts text content
- Handles various number formats including:
  - Regular numbers (e.g., 1,234.56)
  - Numbers with multipliers (e.g., 1.5 million, 2.3k)
  - Numbers in different units (thousands, millions)
- Processes text in different contexts present in the example file:
  - Individual numbers with modifiers
  - Numbers in tables with unit indicators
  - Numbers in fund sections

## Installation

1. Clone this repository

2. Create and activate a virtual environment:
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Linux/Mac:
source .venv/bin/activate
# On Windows:
# .venv\Scripts\activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the program by providing a path to a PDF file:

```bash
python main.py path/to/your/file.pdf
```

The program will:
1. Parse the PDF file (or use cached content if available)
2. Search for numbers throughout the document
3. Apply appropriate multipliers based on context
4. Print the largest number found

## Output

The program provides detailed output including:
- Parsing time
- New largest numbers as they're found
- Final result with the largest number found
- Processing time for number search and comparison

## Limitations

- The PDF content will likely not be processed correctly if it is scanned or has had OCR applied
- The regex requires that numbers either contain commas between every 3 digits, or no commas - otherwise, they'll be parsed incorrectly (ex: "2,333,3333" would not be handled correctly)
- Numbers with leading zeros will cause an error when Python's built-in float parsing tries to process them
- The list of years to ignore multipliers for would need to be expanded in different documents, and probably a better way of detecting years would be helpful 
- The list of supported modifiers would likely need improvement and expansion for other files
- The breaking up sections by "Fund #" is very specific to this document or format of document
