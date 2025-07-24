import click
from datadoctor.cleaner import clean_csv
from datadoctor.encoder import encode_columns
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
@click.option("--output", default="encoded_output.csv", help="Output file path")
@click.option("--method",type=click.Choice(['label','onehot']),default='label',help='Encoding method')
def encode(file,method):
    encode_columns(file,method)
    click.echo(f"{method} encoding done successfully!")

if __name__ == "__main__":
    cli()