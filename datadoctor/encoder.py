'''
This is the file that will contain the code to perform column encoding.There will be 2 encoding method
provided to the user. The methods will be:
1. One hot encoding
2. Label Encoding

If the user fails to provide any method,then label encoding will be the default encoding option. 
'''
import os
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from datetime import datetime

def encode_columns(file,output,method='label'):
    df=pd.read_csv(file)
    original_shape=df.shape
    summary=[]
    
    os.makedirs("backups",exist_ok=True)
    os.makedirs("operation_summary",exist_ok=True)
    
    timestamp=datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path=f"backups/{os.path.basename(file).split(".")[0]}_before_encoding_{timestamp}.csv"
    df.to_csv(backup_path,index=False)
    summary.append(f"Backup saved to: {backup_path}")
    
    categorical_columns=df.select_dtypes(include='object').columns.tolist()
    if not categorical_columns:
        summary.append("No categorical columns found to encode")
    else:
        if method=='label':
            le=LabelEncoder()
            for col in categorical_columns:
                df[col]=le.fit_transform(df[col])
                summary.append(f"Label encoded column: {col}")
        elif method=='onehot':
            before_cols=df.columns.tolist()
            df=pd.get_dummies(df,columns=categorical_columns,drop_first=True)
            after_cols=df.columns.tolist()
            added_cols=list(set(after_cols)-set(before_cols))
            summary.append(f"One-hot encoded columns: {categorical_columns}")
            summary.append(f"New columns added: {added_cols}")
        else:
            raise ValueError(f"Invalid encoding method: {method}. Must be 'label' or 'onehot'")

        
    df.to_csv(output,index=False)
    summary.append(f"Encoded data saved to {output}")
    summary.append(f"Original shape: {original_shape}, Final shape: {df.shape}")
    
    summary_file = f"operation_summary/encoding_summary_{timestamp}.txt"
    with open(summary_file, "w") as f:
        for line in summary:
            f.write(line + "\n")

    print("\n".join(summary))