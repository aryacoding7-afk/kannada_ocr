import json
import pandas as pd

with open(
    "output/ocr_results.json",
    "r",
    encoding="utf-8"
) as f:

    cells = json.load(f)

max_row = max(cell["row"] for cell in cells)
max_col = max(cell["column"] for cell in cells)

table = []

for r in range(max_row + 1):

    row_data = []

    for c in range(max_col + 1):

        value = ""

        for cell in cells:

            if (
                cell["row"] == r
                and
                cell["column"] == c
            ):
                value = cell.get("text", "")
                break

        row_data.append(value)

    table.append(row_data)

df = pd.DataFrame(table)

output_file = "translated_output.xlsx"

df.to_excel(
    output_file,
    index=False,
    header=False
)

print(f"Saved {output_file}")