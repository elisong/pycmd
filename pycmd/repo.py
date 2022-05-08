import subprocess
from pathlib import Path
from pprint import pprint

import click
import requests
from PyInquirer import prompt

from .utils import cd


def read_lines(file):
    fpath = Path(file)
    if fpath.is_file():
        with open(fpath, "r") as f:
            lines = f.readlines()
        result = [l.strip() for l in lines if l.strip()]
    else:
        result = []
    return result


def ioHandler(file, data=None, op="r"):
    fpath = Path(file)
    if op == "r":
        if fpath.is_file():
            with open(fpath, "r") as f:
                data = [l.rstrip("\n") for l in f if l.rstrip("\n")]
        return data
    else:
        with open(fpath, "w+") as f:
            f.writelines("\n".join(data))


def repo_cloned():
    repos = {}
    for dir in Path(".").iterdir():
        if dir.is_dir() and Path(dir / ".git").is_dir():
            with cd(dir):
                command = ["git", "config", "--get", "remote.origin.url"]
                link = subprocess.check_output(command, text=True).strip()
            repos[link] = dir
    return repos


def upgrade():
    click.secho("Command: repo upgrade ↩︎", fg="green", bold=True)
    repos = repo_cloned()
    links = ioHandler("repo.txt", op="r")

    click.secho("update repo.txt", fg="yellow", bold=True)
    links = sorted(list(set(links) | set(repos.keys())))
    ioHandler("repo.txt", data=links, op="w")
    subprocess.run(["cat", "repo.txt"])

    click.secho("update .gitignore", fg="yellow", bold=True)
    gitignore = ioHandler(".gitignore", op="r")
    for link, dir in repos.item():
        for ignore in gitignore:
            if dir.name in ignore:
                repos.pop(link)
                continue
    gitignore.extend(dir.name for dir in repos.values())
    ioHandler(".gitignore", data=gitignore, op="w")
    click.echo("\n")
    subprocess.run(["cat", ".gitignore"])


@click.group()
def cli():
    pass


@cli.command()
@click.argument("keyword")
def search(keyword):
    click.secho(f"Command: repo search {keyword} ↩︎", fg="green", bold=True)
    resp = requests.get(
        "https://api.github.com/search/repositories",
        params={"q": keyword, "sort": "stars", "order": "desc"},
        headers={"Accept": "application/vnd.github.v3+json"},
    )
    result = []
    for item in resp.json()["items"]:
        result.append(
            {
                "name": item["name"],
                "full_name": item["full_name"],
                "description": item["description"],
                "ssh_url": item["ssh_url"],
                "visibility": item["visibility"],
                "updated_at": item["updated_at"],
                "created_at": item["created_at"],
            }
        )

    pprint(result, sort_dicts=False)


@cli.command()
@click.option("--all", is_flag=True)
def clone(all):
    links = ioHandler("repo.txt", op="r")
    if all:
        click.secho("Command: repo clone --all ↩︎", fg="green", bold=True)
        for link in links:
            name = link.rpartition(".")[0].partition(":")[-1].partition("/")[-1]
            if not Path(name).is_dir():
                subprocess.run(["git", "clone", link])
    else:
        question = [
            {
                "type": "list",
                "name": "repo",
                "message": "Which repo do you want?",
                "choices": links,
            }
        ]
        link = prompt(question)["repo"]
        name = link.rpartition(".")[0].partition(":")[-1].partition("/")[-1]
        if not Path(name).is_dir():
            subprocess.run(["git", "clone", link])
    upgrade()


@cli.command()
@click.option("--all", is_flag=True)
def pull(all):
    repos = repo_cloned()
    if all:
        click.secho("Command: repo pull --all ↩︎", fg="green", bold=True)
        for dir in repos.values():
            click.secho(f"Command: repo pull {dir.name} ↩︎", fg="green", bold=True)
            with cd(dir):
                subprocess.run(["git", "pull"])

    else:
        question = [
            {
                "type": "list",
                "name": "repo",
                "message": "Which repo do you want?",
                "choices": [dir.name for dir in repos.values()],
            }
        ]
        name = prompt(question)["repo"]
        with cd(name):
            click.secho(f"Command: repo pull {name} ↩︎", fg="green", bold=True)
            subprocess.run(["git", "pull"])


if __name__ == "__main__":
    cli()
