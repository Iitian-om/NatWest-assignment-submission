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

    # Perform transformations based on rules
    output_df = pd.DataFrame()
    output_df['outfield1'] = input_df['field1'] + input_df['field2']
    output_df['outfield2'] = reference_df['refdata1']
    output_df['outfield3'] = reference_df['refdata2'] + reference_df['refdata3']
    output_df['outfield4'] = input_df['field3'].astype(float) * input_df[['field5', 'refdata4']].max(axis=1)
    output_df['outfield5'] = input_df[['field5', 'refdata4']].max(axis=1)

    report_path = "uploads/output.csv"
    output_df.to_csv(report_path, index=False)
    return report_path