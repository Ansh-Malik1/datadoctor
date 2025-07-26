'''
This is the file where code for performing PCA will be written.
User will specify number of PCA componenets to keep and PCA will be executed accordingly.
'''
import os
from datetime import datetime
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import pandas as pd
def perform_pca(file,output,target,components=None,retain=None):
    df=pd.read_csv(file)
    os.makedirs("backup",exist_ok=True)
    os.makedirs("operation_summary",exist_ok=True)
    
    timestamp=datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path=f"backups/{os.path.basename(file).split('.')[0]}_before_cleaning_{timestamp}.csv"
    df.to_csv(backup_path,index=False)
    print(f"Backup saved to: {backup_path}")
    
    if target:
        if target not in df.columns:
            raise ValueError(f"Target column '{target}' not found in dataset.")
        target_series = df[target]
        df = df.drop(columns=[target])
    else:
        target_series = None

    
    numeric_df=df.select_dtypes(include=['int64','float64'])
    numeric_cols = numeric_df.columns.tolist()
    mean_vals = df[numeric_cols].mean()
    std_vals = df[numeric_cols].std()
    if not (abs(mean_vals.mean()) < 1 and 0.5 < std_vals.mean() < 2):
        print("Warning: Data might not be scaled. PCA usually works best on scaled data.")
        confirm = input("Do you still want to proceed? (y/n): ").strip().lower()
        if confirm != 'y':
            print("Aborted PCA operation.")
            return
    if components and retain:
        raise ValueError("Specify only one: --components or --retain (not both).")

    if not components and not retain:
        raise ValueError("You must specify either --components or --retain.")    
    if components and len(numeric_cols) < int(components):
        raise ValueError(f"PCA requires at least {components} numeric columns, but found {len(numeric_cols)}.")
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df[numeric_cols])
    
    if retain:
        pca = PCA(n_components=float(retain))
        pca_result = pca.fit_transform(scaled_data)
        components_used = pca_result.shape[1]
        pca_df = pd.DataFrame(pca_result, columns=[f"PC{i+1}" for i in range(components_used)])
    else:
        pca = PCA(n_components=int(components))
        pca_result = pca.fit_transform(scaled_data)
        pca_df = pd.DataFrame(pca_result, columns=[f"PC{i+1}" for i in range(int(components))])
        
    non_numeric_df=df.drop(columns=numeric_df.columns)
    final_df = pd.concat([pca_df, non_numeric_df.reset_index(drop=True)], axis=1)
    if target_series is not None:
        final_df[target] = target_series.values
    final_df.to_csv(output, index=False)
    print(f"PCA applied with {components} components. Output saved to {output}")
    
    if retain:
        print(f"PCA applied to retain {float(retain)*100:.2f}% variance using {components_used} components. Output saved to {output}")
    else:
        print(f"PCA applied with {components} components. Output saved to {output}")
        
    summary_path = f"operation_summary/{os.path.basename(file).split('.')[0]}_pca_summary_{timestamp}.txt"
    with open(summary_path, "w") as f:
        f.write("PCA Summary\n")
        f.write(f"Input File: {file}\n")
        f.write(f"Output File: {output}\n")
        f.write(f"Timestamp: {timestamp}\n")
        f.write(f"Original Shape: {df.shape}\n")
        f.write(f"Numeric Columns Used: {list(numeric_df.columns)}\n")
        if retain:
            f.write(f"Retained {pca.explained_variance_ratio_.sum() * 100:.2f}% variance with {components_used} components.\n")
        else: f.write(f"Number of Components: {components}\n")
        f.write(f"Explained Variance Ratio: {pca.explained_variance_ratio_.tolist()}\n")

    print(f"Summary saved to {summary_path}")
    