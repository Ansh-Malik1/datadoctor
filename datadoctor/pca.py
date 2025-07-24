'''
This is the file where code for performing PCA will be written.
User will specify number of PCA componenets to keep and PCA will be executed accordingly.
'''
import os
from datetime import datetime
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import pandas as pd
def perform_pca(file,components,output):
    df=pd.read_csv(file)
    
    os.makedirs("backup",exist_ok=True)
    os.makedirs("operation_summary",exist_ok=True)
    
    timestamp=datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path=f"backups/{os.path.basename(file).split('.')[0]}_before_cleaning_{timestamp}.csv"
    df.to_csv(backup_path,index=False)
    print(f"Backup saved to: {backup_path}")
    
    numeric_df=df.select_dtypes(include=['int64','float64'])
    
    if numeric_df.shape[1] < components:
        raise ValueError(f"PCA requires at least {components} numeric columns, but found {numeric_df.shape[1]}.")
    
    scaler=StandardScaler()
    scaled=scaler.fit_transform(numeric_df)
    
    #appling pca
    pca=PCA(n_components=components)
    pca_result=pca.fit_transform(scaled)
    
    pca_df=pd.DataFrame(pca_result,columns=[f"PC{i+1}" for i in range(components)])
    non_numeric_df=df.drop(columns=numeric_df.columns)
    final_df = pd.concat([pca_df, non_numeric_df.reset_index(drop=True)], axis=1)
    
    final_df.to_csv(output, index=False)
    print(f"PCA applied with {components} components. Output saved to {output}")
    
    summary_path = f"operation_summary/{os.path.basename(file).split('.')[0]}_pca_summary_{timestamp}.txt"
    with open(summary_path, "w") as f:
        f.write("PCA Summary\n")
        f.write(f"Input File: {file}\n")
        f.write(f"Output File: {output}\n")
        f.write(f"Timestamp: {timestamp}\n")
        f.write(f"Original Shape: {df.shape}\n")
        f.write(f"Numeric Columns Used: {list(numeric_df.columns)}\n")
        f.write(f"Number of Components: {components}\n")
        f.write(f"Explained Variance Ratio: {pca.explained_variance_ratio_.tolist()}\n")

    print(f"📝 Summary saved to {summary_path}")
    