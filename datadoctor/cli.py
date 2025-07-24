import click
from datadoctor.cleaner import clean_csv
from datadoctor.encoder import encode_columns
from datadoctor.scaler import scale_columns
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
def clean(file,output,dropna,dropdupe,fix_cols):
    clean_csv(file,output,dropna,dropdupe,fix_cols)
    click.echo(f"File cleaned succesfully and saved to {output}")

@cli.command()
@click.argument("file",type=click.Path(exists=True))
@click.option("--output","-o", default="encoded_output.csv", help="Output file path")
@click.option("--method",type=click.Choice(["label","onehot"]),default='label',help='Encoding method')
def encode(file,method,output):
    encode_columns(file,output,method)
    click.echo(f"{method} encoding done successfully!")

@cli.command()
@click.argument("file",type=click.Path(exists=True))
@click.option("--output","-o",default="scaled_output.csv",help="Output file path")
@click.option("--method",type=click.Choice(["standard", "minmax"], case_sensitive=False), help="Scaling method: standard or minmax")
@click.option("--columns", multiple=True, help="Optional: Specific columns to scale. If not provided, all numerical columns (excluding binary) will be scaled")
def scale(file,output,method,columns):
    scale_columns(file, method.lower(), output, list(columns) if columns else None)
    click.echo(f"Columns scaled successfully using {method} scaling method!.")
if __name__ == "__main__":
    cli()