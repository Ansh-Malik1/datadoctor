import click
from datamedic.cleaner import clean_csv
from datamedic.encoder import encode_columns
from datamedic.scaler import scale_columns
from datamedic.pca import perform_pca
from datamedic.leakage import detect_leakage
from datamedic.eda import perform_eda
from datamedic import __version__
import time
@click.group()
@click.version_option(version=__version__, prog_name="datamedic")
def cli():
    """datamedic CLI"""
    pass
    
@cli.command()
@click.argument("file",type=click.Path(exists=True))
@click.option("--output","-o", default="cleaned.csv", help="User defined output file's name. Default : cleaned.csv")
@click.option("--dropna",is_flag=True,help="Drop the rows with missing values")
@click.option("--dropdupe",is_flag=True,help="Drop duplicate rows")
@click.option("--fix-cols",is_flag=True,help="Standardize column names (converts name to lowercase,removes trailing spaces etc)")
@click.option("--fillna",type=str,required=False,default=None,help="Fill out null values using mean,median,mode or constant fill strategy. Mutually exclusive with dropna")
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
@click.option("--output","-o", default="encoded_output.csv", help="User defined output file's name. Default : encoded_output.csv")
@click.option("--method",type=click.Choice(["label","onehot"],case_sensitive=False),default='label',help='Encoding method')
@click.option('--columns',multiple=True, default=None,help='Specify columns to operate on (comma-separated).')
def encode(file,method,output,columns):
    if columns and len(columns) == 1 and ',' in columns[0]:
        columns = [col.strip() for col in columns[0].split(',')]
    encode_columns(file,output,method,list(columns))
    click.echo(f"{method} encoding done successfully!")

@cli.command()
@click.argument("file",type=click.Path(exists=True))
@click.option("--output","-o",default="scaled_output.csv",help="User defined output file's name. Default : scaled_output.csv")
@click.option("--method",type=click.Choice(["standard", "minmax"], case_sensitive=False), help="Scaling method: standard or minmax,default method : standard")
@click.option("--columns", multiple=True, help="Optional: Specific columns to scale. If not provided, all numerical columns (excluding binary) will be scaled")
def scale(file,output,method,columns):
    if method:
        method=method.lower()
    scale_columns(file, output,method, list(columns) if columns else None)
    click.echo(f"Columns scaled successfully using {method} scaling method!.")
    

@cli.command()
@click.argument("file",type=click.Path(exists=True))
@click.option('--components', type=int, help='Number of PCA components to keep')
@click.option("--output","-o",default="pca_output.csv",help="User defined output file's name. Default : pca_output.csv")
@click.option('--retain', type=float, help='Fraction of variance to retain (e.g., 0.95). Mutually exclusive with components')
@click.option('--target' ,required=True,help='Column name of target variable to exclude from PCA.')
def pca(file,output,target,components,retain):
    perform_pca(file,output,target,components,retain)
    
    
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
@click.option("--output", "-o", default="eda_report.txt", help="User defined output file's name. Default : eda_report.txt")
@click.option("--skip_graphs",is_flag=True,help="Provides user an option to skip graph generation for faster EDA.")
def eda(file,target,output,skip_graphs):
    start_time = time.time()
    click.echo(f"Running EDA on {file} ...")
    try:
        summary_path = perform_eda(file, target, output,skip_graphs)
    except Exception as e:
        click.secho(f"Error: {e}", fg="red")
        return
    click.echo(f"\nEDA summary saved to: {summary_path}")
    click.echo(f"\nTime taken: {round(time.time() - start_time, 2)} seconds")
    click.secho("\nEDA complete.", fg="green")

if __name__ == "__main__":
    cli()