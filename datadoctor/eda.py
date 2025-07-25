''' 
This is the file where code for performing eda will be written.
Features to be added in eda:
1. Basic info(shape,size)
2. Descriptive Statistics (mean,median,skeweness)
3. Target Variable insights 
4. Feature distribution
5. Correlation matrix
6. Feature varianve 
8. Visual outputs
'''
import pandas as pd
import os
from datetime import datetime

def perform_eda(file,target=None,output="eda_report.txt"):
    # Basic information
    df=pd.read_csv(file)
    summary=[]
    summary.append(f"# Basic Dataset Summary for: {file}")
    summary.append("=" * 60)
    summary.append(f"\nShape: {df.shape[0]} rows x {df.shape[1]} columns")
    summary.append("\nColumn Info:")
    summary.append(df.dtypes.to_string())
    summary.append("\nMissing Values:")
    missing = df.isnull().sum()
    if missing.sum() == 0:
        summary.append("No missing values found.")
    else:
        summary.append(missing[missing > 0].to_string())
        
    summary.append("\nUnique Values:")
    uniques = df.nunique()
    for col, count in uniques.items():
        summary.append(f"{col}: {count} unique")
    summary.append("")
    dup_count = df.duplicated().sum()
    summary.append(f"Duplicate Rows: {dup_count}")
    
    
    # Descriptive statistics
    summary.append("\nDescriptive Statistics (Numerical Columns):")
    if df.select_dtypes(include='number').empty:
        summary.append("No numerical columns found.")
    else:
        desc = df.describe().T.round(2)
        for col in desc.index:
            stats = desc.loc[col]
            summary.append(f"\nColumn: {col}")
            summary.append(f"  Count : {int(stats['count'])}")
            summary.append(f"  Mean  : {stats['mean']}")
            summary.append(f"  Std   : {stats['std']}")
            summary.append(f"  Min   : {stats['min']}")
            summary.append(f"  25%   : {stats['25%']}")
            summary.append(f"  Median: {stats['50%']}")
            summary.append(f"  75%   : {stats['75%']}")
            summary.append(f"  Max   : {stats['max']}")
    summary.append("=" * 60)
    
    os.makedirs("operation_summary", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    summary_path= f"operation_summary/eda_report_{timestamp}.txt"
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("\n".join(summary))

    return summary_path