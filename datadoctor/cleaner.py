'''
This is the file wherein the code to clean the csv will be written.
As of now the objectives of this 'cleaner' will be :
1. Drop null values
2. Drop duplicate rows
3. standardize the data (lowercase, remove spaces etc)
4. Generate the output
'''
import numpy as np
import pandas as pd
from datetime import datetime
import os

def clean_csv(file,output,dropna=False,dropdupe=False,fix_cols=False,fillna=None,columns=None):
    df=pd.read_csv(file)
    original_shape=df.shape
    summary=[]
    if not any([dropna, fillna, dropdupe, fix_cols]):
        raise ValueError("No operation specified")
    if dropna and fillna:
        raise ValueError("You cannot use both --dropna and --fillna together. Choose one.")
    if columns:
        if all(len(col) == 1 for col in columns):
            joined = ''.join(columns)
            if joined in df.columns:
                columns = [joined]
        missing_cols = [col for col in columns if col not in df.columns]
        if missing_cols:
            raise ValueError(f"The following specified columns do not exist in the dataset: {missing_cols}")
    else:
        columns = df.columns  # Apply to entire dataset if no columns specified
    os.makedirs("backups",exist_ok=True)
    os.makedirs("operation_summary",exist_ok=True)
    
    timestamp=datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path=f"backups/{os.path.basename(file).split('.')[0]}_before_cleaning_{timestamp}.csv"
    df.to_csv(backup_path,index=False)
    summary.append(f"Backup saved to: {backup_path}")
    summary.append(f"Operation/s applied on columns: {columns}")
    if dropna:
        before=df.shape[0]
        df=df.dropna()
        after=df.shape[0]
        summary.append(f"Dropped {before-after} rows with missing values")
        
    if dropdupe:
        before=df.shape[0]
        df=df.drop_duplicates()
        after=df.shape[0]
        summary.append(f"Dropped {before-after} dupliacte rows")
        
    if fix_cols:
        old_cols = df.columns.tolist()
            
        # Step 1: Strip, lower, replace
        cleaned_cols = [col.strip().lower().replace(" ", "_") for col in df.columns]
        
        # Step 2: Handle duplicates by appending _2, _3, etc.
        final_cols = []
        seen = {}
        for col in cleaned_cols:
            if col not in seen:
                seen[col] = 1
                final_cols.append(col)
            else:
                seen[col] += 1
                final_cols.append(f"{col}_{seen[col]}")

        df.columns = final_cols
        
        # Step 3: Report changes
        renamed = [(o, n) for o, n in zip(old_cols, final_cols) if o != n]
        summary.append(f"Renamed columns: {renamed}")
    if fillna is not None:
        if fillna is True:  # Case: user passed --fillna without value
            fillna = "mean"
            summary.append("No fillna strategy specified. Defaulting to 'mean'.")

        strategy = fillna.lower()
        numeric_cols = df.select_dtypes(include='number').columns
        fill_stats = {}

        if strategy in ["mean", "median", "mode"]:
            for col in numeric_cols:
                if df[col].isnull().sum() > 0:
                    if strategy == "mean":
                        value = df[col].mean()
                    elif strategy == "median":
                        value = df[col].median()
                    else:
                        value = df[col].mode().iloc[0]
                    df[col].fillna(value, inplace=True)
                    fill_stats[col] = (df[col].isnull().sum(), value)
            summary.append(f"Filled missing numeric values using '{strategy}' strategy.")

        else:
            # Try using it as a constant
            try:
                constant = float(strategy)
                df.fillna(constant, inplace=True)
                summary.append(f"Filled all missing values with constant value: {constant}")
            except ValueError:
                summary.append(f"Invalid fillna value: '{strategy}'. Skipped filling.")

    df.to_csv(output,index=False)
    summary.append(f"Cleaned data saved to {output}")
    summary.append(f"Original shape : {original_shape}, Final shape : {df.shape}")
    
    summary_file = f"operation_summary/cleaning_summary_{timestamp}.txt"
    with open(summary_file, "w") as f:
        for line in summary:
            f.write(line + "\n")

    print("\n".join(summary))
    return
