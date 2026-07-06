import click
import requests

from journal_commands import (
    api_error,
    create,
    delete,
    get,
    list,
    login,
    logout,
    replace,
    update,
)

@click.group()
@click.version_option()
@click.option(
    "--url",
    envvar="URL",
    default="http://localhost:8000",
    show_default=True,
    help="Base URL of the journal API.",
)
@click.pass_context
def cli(ctx: click.Context, url: str):
    ctx.ensure_object(dict)
    ctx.obj["api_url"] = url.rstrip("/")

@cli.command()
@click.pass_context
def health(ctx: click.Context):
    url = f"{ctx.obj['api_url']}/health"
    try:
        res = requests.get(url, timeout=5)
        res.raise_for_status()
    except requests.RequestException as e:
        raise api_error(e)
    print(f"Status: {res.json()['status']}")

for command in (get, list, login, logout, create, delete, replace, update):
    cli.add_command(command)

if __name__ == "__main__":
    cli()
