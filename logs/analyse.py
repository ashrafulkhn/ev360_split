import re
import pandas as pd

def summarize_can_log(file_path, save_csv=False, save_excel=False):
    """
    Summarize CAN dump logs by unique CAN IDs.
    
    Args:
        file_path (str): Path to the CAN dump text file.
        save_csv (bool): Save summary as CSV if True.
        save_excel (bool): Save summary as Excel if True.
    
    Returns:
        pandas.DataFrame: Summary table (ID hex, ID dec, count, last data).
    """
    # Read log file
    with open(file_path, "r") as f:
        raw_text = f.read()

    # Regex to extract CAN ID and data
    pattern = re.compile(r"can\d+\s+([0-9A-F]+)\s+\[\d+\]\s+((?:[0-9A-F]{2}\s+)+)")
    matches = pattern.findall(raw_text)

    records = []
    for can_id, data in matches:
        data_bytes = data.strip()
        records.append({
            "ID_hex": f"0x{can_id}",
            "ID_dec": int(can_id, 16),
            "Data": data_bytes
        })

    df = pd.DataFrame(records)

    # Summarize by unique CAN IDs
    summary = (
        df.groupby(["ID_hex", "ID_dec"])
        .agg(
            Count=("Data", "count"),
            Last_Data=("Data", "last")
        )
        .reset_index()
        .sort_values("ID_dec")
    )

    # Save outputs if requested
    if save_csv:
        summary.to_csv("can_summary.csv", index=False)
    if save_excel:
        summary.to_excel("can_summary.xlsx", index=False)

    return summary


if __name__ == "__main__":
    # Example usage
    file_path = "candump.log"  # replace with your CAN log filename
    summary_table = summarize_can_log(file_path, save_csv=True, save_excel=True)
    print(summary_table.to_string(index=False))
