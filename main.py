import argparse
import pymupdf4llm
import re
import time

# Accept an argument of what PDF to process
parser = argparse.ArgumentParser(description='Process a PDF file to find its largest number')
parser.add_argument('pdf_path', type=str, help='Path to the PDF file to process')

args = parser.parse_args()

# Convert to Path object for better path handling
pdf_path = args.pdf_path

print(f"Parsing '{pdf_path}' for text content in Markdown format")

start_time = time.time()
text = pymupdf4llm.to_markdown(pdf_path)
end_time = time.time()
elapsed_time = end_time - start_time

print(f"PDF done parsing. Took {elapsed_time:.4f} seconds")

largest_num = float('-inf')

start_time = time.time()

# Some large numbers have a "multiplier" immediately next to them - ex: "1,088.6 million"
# Let's first search for all numbers with a recognized multiplier right next to them, and handle them first
numbers_with_modifications = re.findall(r'(?i)((?=\d|\.\d)(?:\d{1,3}(?:,\d{3})+|\d+)?(?:\.\d+)?)( hundred|k| thousand|m| million)', text)

modifiers_to_numbers = {
    ' hundred': 100,
    'k': 1000,
    ' thousand': 1000,
    'm': 1000000,
    ' million': 1000000,
    '($k)': 1000,
    '($m)': 1000000,
    ' in thousands)': 1000,
    ' in millions)': 1000000
}

numbers_to_ignore_multiplier = ['2023', '2024', '2025']
date_multiplier_override_count = [0]

def get_number(number_pieces: list[str]) -> float:
    number_str, modifier = number_pieces
    number_to_parse = number_str.replace(',', '')
    
    multiplier = modifiers_to_numbers[modifier.lower()]
    return float(number_to_parse) * multiplier

def get_number_with_multiplier(number_str: str, multiplier: int) -> float:
    number_to_parse = number_str.replace(',', '')
    if number_str in numbers_to_ignore_multiplier and multiplier > 1:
        date_multiplier_override_count[0] += 1
        multiplier = 1

    return float(number_to_parse) * multiplier

for number_pieces in numbers_with_modifications:
    current_num = get_number(number_pieces)
    if current_num > largest_num:
        print(f'New largest number: {current_num:.4f} from {number_pieces}')
    largest_num = max(largest_num, current_num)

# Some tables indicate a unit of thousands or millions - ex: "Cost ($M)"
# Looking at our extracted text, it seems to always have an empty line between any change in units
# Let's split our text into blocks, set a unit multiplier for that block if it has one, and analyze all numbers in each block

blocks_with_modifiers = text.split("\n\n")

print(f"Processing text in blocks, looking for modifiers - total number of blocks: {len(blocks_with_modifiers)}")

for block_number, text_block in enumerate(blocks_with_modifiers, start=1):
    multiplier = 1

    result = re.search(r'(?i)(\(\$K\)|\(\$M\))', text_block)
    if result is not None:
        print(f"Found modifier '{result.group()}' in text block {block_number}")
        multiplier = modifiers_to_numbers[result.group().lower()]

    numbers = re.findall(r'(?=\d|\.\d)(?:\d{1,3}(?:,\d{3})+|\d+)?(?:\.\d+)?', text_block)
    for num in numbers:
        current_num = get_number_with_multiplier(num, multiplier)
        if current_num > largest_num:
            print(f'New largest number: {current_num:.4f} in block {block_number} with multiplier {multiplier}')
            largest_num = current_num

print(f"Number of dates with multipliers overriden: {date_multiplier_override_count[0]}")

# Some budgets for specific funds specify that their dollar amounts are in thousands or millions - ex: "(Dollars in Millions)"
# Let's split our text based on the "Fund #" header of each of those sections, and then handle each similarly to above 

text_by_fund = re.split(r'\nFund \d', text)

print(f"Processing text by fund, looking for modifiers - total number of pieces: {len(text_by_fund)}")

for fund_number, fund_text in enumerate(text_by_fund, start=1):
    multiplier = 1

    result = re.search((r'( in Thousands\)| in Millions\))'), fund_text)
    if result is not None:
        multiplier = modifiers_to_numbers[result.group().lower()]

    numbers = re.findall(r'(?=\d|\.\d)(?:\d{1,3}(?:,\d{3})+|\d+)?(?:\.\d+)?', fund_text)
    for num in numbers:
        current_num = get_number_with_multiplier(num, multiplier)
        if current_num > largest_num:
            print(f'New largest number: {current_num:.4f} in fund {fund_number} with multiplier {multiplier}')
            largest_num = current_num

print(f"Total number of dates with multipliers overriden: {date_multiplier_override_count[0]}")

end_time = time.time()
elapsed_time = end_time - start_time
print(f'Number search and comparison complete. Took {elapsed_time:.4f} seconds.')

if largest_num == float('-inf'):
    print("No numbers found in the file")
else:
    print(f'Largest number found was {largest_num:.4f}')