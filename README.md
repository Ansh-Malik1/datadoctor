# 🩺 datamedic

**It’s not just a CLI, it’s a clinical intervention for your dataset.**  
Clean, encode, scale, reduce, diagnose — all from one powerful CLI tool.

---

## 🚀 Overview

Working with raw data? Facing inconsistent formats, nulls, outliers, or unknown leakage?  
**datamedic** is designed to **automate and simplify** the most common and critical steps in preprocessing, helping you:

- Save hours of manual data cleaning
- Avoid common mistakes like data leakage
- Maintain clean pipelines — all from your terminal

Whether you're a data analyst, scientist, ML engineer, or student — **datamedic is built to make your life easier.**

---

## ⚙️ Installation

```
pip install datamedic
```
For development or editable mode:
```
git clone https://github.com/your-username/datamedic.git
cd datamedic
pip install -e .
```
🛠️ Available Commands
| Command   | Description                                                     |
| --------- | --------------------------------------------------------------- |
| `clean`   | Handle nulls, fix column names, drop duplicates                 |
| `encode`  | Perform label or one-hot encoding                               |
| `scale`   | Standardize or normalize numerical columns                      |
| `pca`     | Apply Principal Component Analysis for dimensionality reduction |
| `leakage` | Detect data leakage between input features and target           |
| `eda`     | Run exploratory data analysis with visual summaries             |


Use --help with any command for detailed options.
Example:
```
datamedic clean --help
```
---
## 📦 Sample Workflow

### Step 1: Clean the data
```datamedic clean data.csv --fillna mean --fix-cols --dropdupe -o cleaned.csv```

### Step 2: Encode categorical columns
```datamedic encode cleaned.csv --method onehot -o encoded.csv```

### Step 3: Scale the numerical features
```datamedic scale encoded.csv --method standard -o scaled.csv```

### Step 4: Apply PCA for dimensionality reduction
```datamedic pca scaled.csv --components 5 -o reduced.csv```

### Step 5: Detect possible data leakage
```datamedic leakage reduced.csv --target sale_price```

### Step 6: Generate an automated EDA report
```
datamedic eda cleaned.csv
```
✨ Key Features
• Intuitive CLI interface with structured command options

• Optional column targeting for all major operations

• PCA with component or variance threshold options

• Detailed summary and fallback backups at each step

• Graphs and automated insights from EDA

• Intelligent detection of potential data leakage

• Lightweight, dependency-optimized, no GUI needed

---
## Testing & Reliability
This tool has been tested with over 50+ CLI test cases across real-world and edge scenarios.
Verified by early-stage testers from diverse backgrounds.

datamedic ensures that your preprocessing is both robust and repeatable.

## 🧪 Troubleshooting
1. 'Command Not Found': Restart terminal or use pip install -e . in dev mode.
2. UnicodeDecodeError: Try --encoding utf-8 while loading file.
3. PCA Warning Despite Scaling: Ensure scaling is done using datamedic scale.
4. CLI Flags Not Working: Pass comma-separated columns like --columns age,salary.

See full Troubleshooting Guide for more.

## 📂 Folder Structure (Core)
```
datamedic/
├── cleaner.py
├── encoder.py
├── scaler.py
├── pca.py
├── leakage.py
├── eda.py
├── cli.py
│
├── eda_outputs/
│   └── [graphs and reports]
│
├── operation_summary/
│   └── [stepwise summaries]
│
```
## 📄 License
This project is licensed under the MIT License — see the LICENSE file for details.

## 🙌 Feedback & Contributions
We’re actively improving datamedic.
Feel free to open issues or submit a PR.

💬 Want to share suggestions or report bugs? Fill out this quick feedback form (anonymous optional).

Link : (https://forms.gle/CTG7bZRPqqGQofnS7)

**Docs are clean. Contributions are welcome. Feedback is gold.**
## 🔥 Why datamedic?
Because every good model starts with great data —
and every great dataset needs a medic.

Use it. Share it. Trust it.
**datamedic saves you time so you can spend it on what actually matters : modeling, insight, and impact.**

## 🤝 Support the Launch

If you found **datamedic** valuable, please consider supporting the project by engaging with my linkedin,

Link : <>

Even a like, comment, or repost goes a long way in helping this reach more people.

 📌 **Products improve over time, but it's the personal brand and community that lasts forever.**

Thanks for being a part of the journey.
