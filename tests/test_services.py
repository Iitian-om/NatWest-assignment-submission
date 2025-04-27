import pytest
import pandas as pd
from app.services import generate_report

@pytest.mark.asyncio
async def test_generate_report():
    # Mock input and reference data
    input_data = {
        "field1": ["A", "B"],
        "field2": ["C", "D"],
        "field3": [1, 2],
        "field5": [10, 20],
        "refkey1": ["key1", "key2"],
        "refkey2": ["key2", "key3"]
    }
    reference_data = {
        "refkey1": ["key1", "key2"],
        "refdata1": ["Ref1", "Ref2"],
        "refkey2": ["key2", "key3"],
        "refdata2": ["R2", "R3"],
        "refdata3": ["R3", "R4"],
        "refdata4": [5, 15]
    }

    input_df = pd.DataFrame(input_data)
    reference_df = pd.DataFrame(reference_data)

    # Save to CSV for testing
    input_df.to_csv("uploads/input.csv", index=False)
    reference_df.to_csv("uploads/reference.csv", index=False)

    # Call the function
    report_path = await generate_report()

    # Load the output report and validate
    output_df = pd.read_csv(report_path)
    assert output_df.shape[0] == 2  # Check number of rows
    assert "outfield1" in output_df.columns  # Check if outfield1 exists
    assert output_df["outfield1"].iloc[0] == "AC"  # Validate transformation
    assert output_df["outfield4"].iloc[0] == 10  # Validate transformation