import click

from python.zaf.fishfeed import run_fishfeed

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(invoke_without_command=True, context_settings=CONTEXT_SETTINGS)
@click.version_option(version='0.1')
def fishfeed():
    pass


@fishfeed.command()
def run(**kwargs):
    run_fishfeed()


@fishfeed.command()
def last5(**kwargs):
    click.echo(5)


@fishfeed.command()
def last50(**kwargs):
    click.echo(50)


if __name__ == '__main__':
    fishfeed()
