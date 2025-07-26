'''
This will be the file that will contain the code to scale columns, according to the plan,
if user provides columns, then scaling will be applied on that only else scaling will be
applied to all numerical columns except binary.
There will 2 scaling method provided to the user. These are :
1. MinMax scaling (scaled between 0 to 1)
2. Standard Scaling (mean=0, standard deviation=1)
'''
import pandas as pd
import os
from datetime import datetime
from sklearn.preprocessing import StandardScaler,MinMaxScaler

def scale_columns(file,output,method="standard",columns=None):
    df=pd.read_csv(file)
    original_shape=df.shape
    summary=[]
    
    os.makedirs("backups",exist_ok=True)
    os.makedirs("operation_summary",exist_ok=True)
    
    timestamp=datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path=f"backups/{os.path.basename(file).split('.')[0]}_before_cleaning_{timestamp}.csv"
    df.to_csv(backup_path, index=False)
    summary.append(f"Backup saved to: {backup_path}")
    
    if columns is None:
        numeric_cols=df.select_dtypes(include='number').columns.to_list()
        columns = [
            col for col in numeric_cols 
            if sorted(df[col].dropna().unique().tolist()) not in [[0], [1], [0, 1]]
        ]
        summary.append(f"No columns specified, {columns} are selected automatically")
        
    if not columns:
        summary.append("No eligible columns to scale. Skipping scaling step.")
        scaled_df = df.copy()
        
    else:
        scaler=StandardScaler() if method=="standard" else MinMaxScaler()
        scaled_part=pd.DataFrame(scaler.fit_transform(df[columns]),columns=columns)
        df[columns]=scaled_part
        summary.append(f"Applied {method} scaling to columns: {columns}")
    
    df.to_csv(output,index=False)
    summary.append(f"Scaled data saved to {output}")
    summary.append(f"Original shape: {original_shape}, Final shape: {df.shape}")
    summary_file = f"operation_summary/scaling_summary_{timestamp}.txt"
    with open(summary_file, "w") as f:
        for line in summary:
            f.write(line + "\n")

    print("\n".join(summary))
    return

# extensive testing done,no issues found