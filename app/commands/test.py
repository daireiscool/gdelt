import click

@click.command()
def hello(name):
    """This prints Hello World!"""
    print(f"Hello World!")

