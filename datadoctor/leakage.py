'''
This is the file where code for checking leakage will be written.
Data leakage occurs when information from outside the training dataset is used to 
create the model — leading to unrealistically good performance during training but poor generalization
on real data.

The most common form is when features are too correlated with 
the target — i.e., they directly or indirectly contain the target value.

User will give :
1. Target
2. Threshold
'''
import pandas as pd
import numpy as np
from sklearn.feature_selection import mutual_info_classif
import os
from datetime import datetime

def detect_leakage(file,target,threshold,output):
    df=pd.read_csv(file)
    if(target not in df.columns):
        raise ValueError(f"Target column '{target}' not found.")
    
    os.makedirs("operation_summary",exist_ok=True)
    timestamp=datetime.now().strftime("%Y%m%d_%H%M%S")
    y=df[target]
    x=df.drop(columns=[target])
    report=[]
    
    for col in x.columns:
        try:
            if pd.api.types.is_numeric_dtype(y):
                if pd.api.types.is_numeric_dtype(x[col]):
                    score=abs(df[col].corr(y))
                    method="Pearson"
                else:
                    continue
            else:
                if pd.api.types.is_numeric_dtype(x[col]):
                    score = mutual_info_classif(x[[col]].fillna(0), y, discrete_features=False)[0]
                else:
                    score = mutual_info_classif(pd.get_dummies(x[[col]].fillna("NA")), y)[0]
                method = "Mutual Info"
            is_flagged = score >= threshold
            report.append({
                "feature": col,
                "method": method,
                "score": round(score, 4),
                "leak_risk": "High" if is_flagged else "Low"
            })

        except Exception as e:
            print(f"Skipped column '{col}' due to error: {e}")
            continue

    report_df = pd.DataFrame(report).sort_values(by="score", ascending=False)
    report_df.to_csv(output, index=False)

    # Save step summary
    summary_path = summary_path = f"operation_summary/{os.path.basename(file).split('.')[0]}_leakage_summary{timestamp}.txt"
    with open(summary_path, "w") as f:
        f.write(f"Target: {target}\nThreshold: {threshold}\n")
        f.write("Potential leakage columns:\n")
        f.write(report_df[report_df["leak_risk"] == "High"].to_string(index=False))
        f.write("\n\nDisclaimer : Some features are flagged due to strong correlation with the target.\n"
        "This doesn't always imply data leakage.\n"
        "Use domain knowledge before removing any column.\n",)

    return report_df, summary_path