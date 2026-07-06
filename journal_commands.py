import click
import requests

from auth import clear_token, load_token, save_token

def api_error(e: requests.RequestException) -> click.ClickException:
    return click.ClickException(e.response.json()["detail"])

@click.command()
@click.option("--username", "-u", prompt=True, help="API username.")
@click.option(
    "--password",
    "-p",
    prompt=True,
    hide_input=True,
    help="API password.",
)
@click.pass_context
def login(ctx: click.Context, username: str, password: str):
    url = f"{ctx.obj['api_url']}/login"
    try:
        res = requests.post(
            url,
            data={"username": username, "password": password},
            timeout=5,
        )
        res.raise_for_status()
    except requests.RequestException as e:
        raise api_error(e)
    save_token(res.json()["access_token"])
    print("Login succesful.")

@click.command()
def logout():
    clear_token()
    print("Logged out.")

@click.command()
@click.pass_context
def list(ctx: click.Context):
    url = f"{ctx.obj['api_url']}/api/journal"
    headers = {"Authorization": f"Bearer {load_token()}"}
    try:
        res = requests.get(url, headers=headers, timeout=5)
        res.raise_for_status()
    except requests.RequestException as e:
        raise api_error(e)
    for entry in res.json():
        print(f"{entry['id']}: {entry['title']}")

@click.command()
@click.argument("journal_id", type=int)
@click.pass_context
def get(ctx: click.Context, journal_id: int):
    url = f"{ctx.obj['api_url']}/api/journal/{journal_id}"
    headers = {"Authorization": f"Bearer {load_token()}"}
    try:
        res = requests.get(url, headers=headers, timeout=5)
        res.raise_for_status()
    except requests.RequestException as e:
        raise api_error(e)
    data = res.json()
    print(f"Title: {data['title']}")
    print(f"Body: {data['body']}")

@click.command()
@click.argument("journal_id", type=int)
@click.pass_context
def delete(ctx: click.Context, journal_id: int):
    url = f"{ctx.obj['api_url']}/api/journal/{journal_id}"
    headers = {"Authorization": f"Bearer {load_token()}"}
    try:
        res = requests.delete(url, headers=headers, timeout=5)
        res.raise_for_status()
    except requests.RequestException as e:
        raise api_error(e)
    print(f"Deleted entry {journal_id}")

@click.command()
@click.option("--title", prompt=True, help="Title of the journal entry.")
@click.option("--body", prompt=True, help="Body of the journal entry.")
@click.pass_context
def create(ctx: click.Context, title: str, body: str):
    url = f"{ctx.obj['api_url']}/api/journal/create"
    headers = {"Authorization": f"Bearer {load_token()}"}
    try:
        res = requests.post(
            url,
            json={"title": title, "body": body},
            headers=headers,
            timeout=5,
        )
        res.raise_for_status()
    except requests.RequestException as e:
        raise api_error(e)
    data = res.json()
    print(f"Created entry {data['id']}: {data['title']}")

@click.command()
@click.argument("journal_id", type=int)
@click.option("--title", prompt=True, help="Title of the journal entry.")
@click.option("--body", prompt=True, help="Body of the journal entry.")
@click.pass_context
def replace(
    ctx: click.Context,
    journal_id: int,
    title: str,
    body: str,
):
    url = f"{ctx.obj['api_url']}/api/journal/{journal_id}"
    headers = {"Authorization": f"Bearer {load_token()}"}
    try:
        res = requests.put(
            url,
            json={"title": title, "body": body},
            headers=headers,
            timeout=5,
        )
        res.raise_for_status()
    except requests.RequestException as e:
        raise api_error(e)
    data = res.json()
    print(f"Replaced entry {data['id']}: {data['title']}")

@click.command()
@click.argument("journal_id", type=int)
@click.option(
    "--title",
    prompt=True,
    default="",
    show_default=False,
    help="New title of the journal entry (leave blank to keep unchanged).",
)
@click.option(
    "--body",
    prompt=True,
    default="",
    show_default=False,
    help="New body of the journal entry (leave blank to keep unchanged).",
)
@click.pass_context
def update(
    ctx: click.Context,
    journal_id: int,
    title: str | None,
    body: str | None,
):
    payload = {k: v for k, v in {"title": title, "body": body}.items() if v}
    if not payload:
        raise click.UsageError("Provide at least one of --title or --body.")
    url = f"{ctx.obj['api_url']}/api/journal/{journal_id}"
    headers = {"Authorization": f"Bearer {load_token()}"}
    try:
        res = requests.patch(url, json=payload, headers=headers, timeout=5)
        res.raise_for_status()
    except requests.RequestException as e:
        raise api_error(e)
    data = res.json()
    print(f"Updated entry {data['id']}: {data['title']}")
