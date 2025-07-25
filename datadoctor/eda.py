''' 
This is the file where code for performing eda will be written.
Features to be added in eda:
1. Basic info(shape,size)
2. Descriptive Statistics (mean,median,skeweness)
3. Target Variable insights 
4. Feature distribution
5. Correlation matrix
6. Feature variance 
7. Visual outputs
'''
import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

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
    
    
    #Target insights
    if target not in df.columns:
        summary.append(f"Target column '{target}' not found in the dataset.")
        return

    target_data = df[target]
    summary.append(f"\n--- Target Insights: '{target}' ---")

    if pd.api.types.is_numeric_dtype(target_data):
        summary.append("Target is numeric.")
        summary.append(f"Mean: {round(target_data.mean(), 4)}")
        summary.append(f"Median: {round(target_data.median(), 4)}")
        summary.append(f"Std Deviation: {round(target_data.std(), 4)}")
        summary.append(f"Min: {target_data.min()}, Max: {target_data.max()}")
    else:
        summary.append("Target is categorical.")
        value_counts = target_data.value_counts(dropna=False)
        summary.append("Class distribution:")
        for cls, count in value_counts.items():
            percent = round((count / len(target_data)) * 100, 2)
            summary.append(f"- {cls}: {count} ({percent}%)")
        if value_counts.shape[0] == 2:
            summary.append("Binary classification detected.")
        elif value_counts.shape[0] <= 10:
            summary.append("Multi-class classification detected.")
        else:
            summary.append("High-cardinality target detected.")

    if target_data.isnull().sum() > 0:
        summary.append(f"Warning: Target column has {target_data.isnull().sum()} missing values.")
        
    
    # Feature Distribution
    graph_dir = "generated_graphs"
    os.makedirs(graph_dir, exist_ok=True)

    numeric_cols = df.select_dtypes(include=["int", "float"]).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object", "category", "bool"]).columns.tolist()

    summary.append("\n=== Graphs Generated ===")
    
    # Numerical columns: Histograms
    for col in numeric_cols:
        try:
            plt.figure(figsize=(6, 4))
            sns.histplot(df[col].dropna(), kde=True, bins=30, color='skyblue')
            plt.title(f"Distribution of {col}")
            plt.xlabel(col)
            plt.ylabel("Frequency")
            file_path = os.path.join(graph_dir, f"distribution_{col}.png")
            plt.savefig(file_path)
            plt.close()
            summary.append(f"Distribution graph saved: {file_path}")
        except Exception as e:
            summary.append(f"[x] Could not generate graph for {col}: {e}")
            continue

    # Categorical columns: Count plots
    for col in categorical_cols:
        try:
            plt.figure(figsize=(6, 4))
            sns.countplot(x=col, data=df, order=df[col].value_counts().index[:10],color="skyblue")
            plt.title(f"Count Plot of {col}")
            plt.xticks(rotation=45)
            plt.xlabel(col)
            plt.ylabel("Count")
            file_path = os.path.join(graph_dir, f"countplot_{col}.png")
            plt.tight_layout()
            plt.savefig(file_path)
            plt.close()
            summary.append(f"Count plot saved: {file_path}")
        except Exception as e:
            summary.append(f"[x] Could not generate count plot for {col}: {e}")
            continue
    
    # Correlation heatmap
    numeric_df = df.select_dtypes(include=[np.number])

    if numeric_df.shape[1] >= 2:
        corr_matrix = numeric_df.corr()
        plt.figure(figsize=(12, 8))
        sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", square=True, cbar_kws={"shrink": .5})
        plt.title("Correlation Heatmap")
        corr_path = os.path.join(graph_dir, "correlation_heatmap.png")
        plt.tight_layout()
        plt.savefig(corr_path)
        plt.close()
        summary.append(f"\nCorrelation heatmap saved to {corr_path}")
    else:
        summary.append("Not enough numeric columns to compute correlation heatmap.")
        
        
        
    # Warnings
    warnings = []

    # Constant Columns
    constant_cols = [col for col in df.columns if df[col].nunique() == 1]
    if constant_cols:
        warnings.append(f"Constant columns detected: {', '.join(constant_cols)}")

    # Highly Correlated Features
    corr_matrix = df.select_dtypes(include='number').corr().abs()
    upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
    high_corr_pairs = [(col, row) for col in upper.columns for row in upper.index if pd.notnull(upper.loc[row, col]) and upper.loc[row, col] > 0.95]
    if high_corr_pairs:
        warning_text = "; ".join([f"{a} ~ {b} ({corr_matrix.loc[a, b]:.2f})" for a, b in high_corr_pairs])
        warnings.append(f"Highly correlated feature pairs (corr > 0.95): {warning_text}")

    # Missingness > 50%
    missing_50 = df.columns[df.isnull().mean() > 0.5].tolist()
    if missing_50:
        warnings.append(f"Columns with >50% missing values: {', '.join(missing_50)}")

    # Duplicate Columns
    duplicate_cols = []
    cols = df.columns
    for i in range(len(cols)):
        for j in range(i+1, len(cols)):
            if df[cols[i]].equals(df[cols[j]]):
                duplicate_cols.append((cols[i], cols[j]))
    if duplicate_cols:
        warning_text = "; ".join([f"{a} == {b}" for a, b in duplicate_cols])
        warnings.append(f"Duplicate columns detected: {warning_text}")

    # Append to summary
    summary.append("\n=== Automatic Warnings ===")
    if warnings:
        summary.extend([f"- {w}" for w in warnings])
    else:
        summary.append("No red flags detected.")
        
    summary.append("="*26)
    # Target-specific Analysis
    summary.append("\nTarget-specific Insights")
    target_dtype = df[target].dtype

    if pd.api.types.is_numeric_dtype(df[target]):
        # Outlier Detection using IQR
        Q1 = df[target].quantile(0.25)
        Q3 = df[target].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        outliers = df[(df[target] < lower) | (df[target] > upper)]

        summary.append(f"Target '{target}' is numeric.")
        summary.append(f"IQR-based Outlier Detection:")
        summary.append(f"- Lower Bound: {lower:.2f}")
        summary.append(f"- Upper Bound: {upper:.2f}")
        summary.append(f"- Outliers detected: {len(outliers)} / {len(df)} ({len(outliers)/len(df)*100:.2f}%)")

    else:
        # Class imbalance check
        class_percents = df[target].value_counts(normalize=True) * 100
        min_pct = class_percents.min()
        max_pct = class_percents.max()

        summary.append(f"Target '{target}' is categorical.")
        if (min_pct < 10) or (max_pct > 80):
            summary.append("Potential class imbalance detected. Consider techniques like oversampling/undersampling.")
        else:
            summary.append("No significant class imbalance detected.")

    # Feature Variance
        
    summary.append("\nFeature Variance")
    try:
        variance = df.select_dtypes(include=[np.number]).var()
        low_variance_threshold = 0.01
        low_variance_features = variance[variance < low_variance_threshold]

        summary.append(f"→ Variance calculated for {len(variance)} numerical features.")
        if not low_variance_features.empty:
            summary.append(
                f"⚠️ {len(low_variance_features)} features have low variance (< {low_variance_threshold}):\n"
                + ", ".join(low_variance_features.index.tolist())
            )
        else:
            summary.append("→ No low-variance features detected.")
    except Exception as e:
        summary.append(f"Error while calculating feature variance: {e}")

    
    os.makedirs("operation_summary", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    summary_path= f"operation_summary/eda_report_{timestamp}.txt"
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("\n".join(summary))

    return summary_path