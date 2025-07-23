import click

@click.group()
def cli():
    """Datadoctor CLI"""
    pass

@cli.command()
@click.option('--name', default='world', help='Name to greet')
def hello(name):
    """Say hello!"""
    click.echo(f"Hello, {name}!")
    
@cli.command()
@click.option('--name',default='world',help='this a function to say bye')
def bye(name):
    click.echo(f"Bye {name}, It was a nice time having you!")
    

if __name__ == "__main__":
    cli()