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
