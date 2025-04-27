import pandas as pd
import os
import json

async def upload_files(input_file, reference_file):
    input_path = f"uploads/{input_file.filename}"
    reference_path = f"uploads/{reference_file.filename}"
    
    with open(input_path, "wb") as f:
        f.write(await input_file.read())
    
    with open(reference_path, "wb") as f:
        f.write(await reference_file.read())
    
    return {"input_file": input_path, "reference_file": reference_path}

async def generate_report():
    # Load transformation rules
    with open("app/rules.json") as f:
        rules = json.load(f)

    # Load input and reference data
    input_df = pd.read_csv("uploads/input.csv")
    reference_df = pd.read_csv("uploads/reference.csv")
    
    # Merge input and reference data on keys
    merged_df = input_df.merge(reference_df, on=['refkey1', 'refkey2'], how='left')

    # Create an empty DataFrame for output
    output_df = pd.DataFrame()

# Apply transformations based on rules
    for rule in rules:
        if rule["operation"] == "concat":
            output_df[rule["output_field"]] = merged_df[rule["inputs"][0]] + merged_df[rule["inputs"][1]]
        elif rule["operation"] == "reference":
            output_df[rule["output_field"]] = merged_df[rule["reference_field"]]
        elif rule["operation"] == "multiply_max":
            output_df[rule["output_field"]] = merged_df[rule["inputs"][0]].astype(float) * merged_df[[rule["inputs"][1], rule["reference_field"]]].max(axis=1)
        elif rule["operation"] == "max":
            output_df[rule["output_field"]] = merged_df[[rule["inputs"][0], rule["reference_field"]]].max(axis=1)

    report_path = "uploads/output.csv"
    output_df.to_csv(report_path, index=False)
    return report_path