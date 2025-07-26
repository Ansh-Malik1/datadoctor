import click
from datadoctor.cleaner import clean_csv
from datadoctor.encoder import encode_columns
from datadoctor.scaler import scale_columns
from datadoctor.pca import perform_pca
from datadoctor.leakage import detect_leakage
from datadoctor.eda import perform_eda
import time
@click.group()
def cli():
    """Datadoctor CLI"""
    pass
    
@cli.command()
@click.argument("file",type=click.Path(exists=True))
@click.option("--output","-o", default="cleaned.csv", help="Output file path")
@click.option("--dropna",is_flag=True,help="Drop the rows with missing values")
@click.option("--dropdupe",is_flag=True,help="Drop duplicate rows")
@click.option("--fix-cols",is_flag=True,help="Standardize column names")
@click.option("--fillna",help="Fill out null values using mean,median,mode or constand fill strategy")
@click.option('--columns',multiple=True, default=None, help='Specify columns to operate on (comma-separated).')
def clean(file,output,dropna,dropdupe,fix_cols,fillna,columns):
    if fillna == "":
        fillna = True
    if columns and len(columns) == 1 and ',' in columns[0]:
        columns = [col.strip() for col in columns[0].split(',')]
    clean_csv(file,output,dropna,dropdupe,fix_cols,fillna,list(columns))
    click.echo(f"File cleaned succesfully and saved to {output}")

@cli.command()
@click.argument("file",type=click.Path(exists=True))
@click.option("--output","-o", default="encoded_output.csv", help="Output file path")
@click.option("--method",type=click.Choice(["label","onehot"]),default='label',help='Encoding method')
@click.option('--columns',multiple=True, default=None,help='Specify columns to operate on (comma-separated).')
def encode(file,method,output,columns):
    if columns and len(columns) == 1 and ',' in columns[0]:
        columns = [col.strip() for col in columns[0].split(',')]
    encode_columns(file,output,method,list(columns))
    click.echo(f"{method} encoding done successfully!")

@cli.command()
@click.argument("file",type=click.Path(exists=True))
@click.option("--output","-o",default="scaled_output.csv",help="Output file path")
@click.option("--method",type=click.Choice(["standard", "minmax"], case_sensitive=False), help="Scaling method: standard or minmax")
@click.option("--columns", multiple=True, help="Optional: Specific columns to scale. If not provided, all numerical columns (excluding binary) will be scaled")
def scale(file,output,method,columns):
    if method:
        method=method.lower()
    scale_columns(file, output,method, list(columns) if columns else None)
    click.echo(f"Columns scaled successfully using {method} scaling method!.")
    

@cli.command()
@click.argument("file",type=click.Path(exists=True))
@click.option('--components', type=int, help='Number of PCA components to keep')
@click.option("--output","-o",default="pca_output.csv",help="Output file path")
def pca(file,components,output):
    perform_pca(file,components,output)
    
    
@cli.command()
@click.argument("file",type=click.Path(exists=True))
@click.option('--target',help="Name of the target column")
@click.option('--threshold',type=float ,default=0.85,help="Threshold value to flag high risk features")
@click.option("--output","-o",default="leakage_report.csv",help="Output file path")
def leakage(file,target,threshold,output):
    start_time=time.time()
    click.echo(f"Analysing data leakage for the file with target as {target}")
    try:
        report_df, summary_path = detect_leakage(file, target, threshold, output)
    except Exception as e:
        click.secho(f"Error: {e}", fg="red")
        return
    click.echo(f"\n Leakage report saved to: {output}")
    click.echo(f" Top suspicious features:")
    click.echo(report_df[["feature", "score", "leak_risk"]].head(10).to_string(index=False))
    click.echo(f"\n Step summary saved to: {summary_path}")
    click.echo(f"\n Time taken: {round(time.time() - start_time, 2)} seconds")
    click.secho(
    "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", fg="yellow"
    )
    click.secho(
        "Reminder: High correlation ≠ Leakage", fg="yellow", bold=True
    )
    click.secho(
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", fg="yellow"
    )
    click.secho(
        "Some features are flagged due to strong correlation with the target.\n"
        "This doesn't always imply data leakage.\n"
        "Use domain knowledge before removing any column.\n",
        fg="yellow"
    )

@cli.command()
@click.argument("file",type=click.Path(exists=True))
@click.option("--target",help="Optional: Name of the target column")
@click.option("--output", "-o", default="eda_report.txt", help="Output report file")
def eda(file,target,output):
    start_time = time.time()
    click.echo(f"Running EDA on {file} ...")
    try:
        summary_path = perform_eda(file, target, output)
    except Exception as e:
        click.secho(f"Error: {e}", fg="red")
        return
    click.echo(f"\nEDA summary saved to: {summary_path}")
    click.echo(f"\nTime taken: {round(time.time() - start_time, 2)} seconds")
    click.secho("\nEDA complete.", fg="green")

if __name__ == "__main__":
    cli()