import click
import requests

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
        raise click.ClickException(f"API unreachable at {url}: {e}")
    print(res.json())

if __name__ == "__main__":
    cli()
