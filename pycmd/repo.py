import json
import subprocess
from pathlib import Path
from pprint import pprint
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import click
from InquirerPy import prompt

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


def io_handler(file, data=None, op="r"):
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


def _sync():
    repos = repo_cloned()
    links = io_handler("repo.txt", op="r")

    click.secho("update repo.txt", fg="yellow", bold=True)
    links = sorted(list(set(links) | set(repos.keys())))
    io_handler("repo.txt", data=links, op="w")
    subprocess.run(["cat", "repo.txt"])

    click.echo("\n")
    click.secho("update .gitignore", fg="yellow", bold=True)
    gitignore = io_handler(".gitignore", op="r")
    addtions = []
    for dir in repos.values():
        has_found = False
        for ignore in gitignore:
            if dir.name in ignore:
                has_found = True
                continue
        if not has_found:
            addtions.append(dir.name + "/")
    gitignore.extend(addtions)
    io_handler(".gitignore", data=gitignore, op="w")
    subprocess.run(["cat", ".gitignore"])


@click.group()
def cli():
    pass


@cli.command()
@click.argument("q")
@click.option("-l", "--language")
@click.option(
    "-s",
    "--sort",
    type=click.Choice(["best-match", "stars", "forks", "help-wanted-issues", "updated"]),
    default="best-match",
)
@click.option("-o", "--order", type=click.Choice(["desc", "asc"]), default="desc")
def search(q, language, sort, order):
    if language:
        params = urlencode({"q": f"{q}+language:{language}", "sort": sort, "order": order})
    else:
        params = urlencode({"q": q, "sort": sort, "order": order})

    click.secho(f"Command: repo search {params} ↩︎", fg="green", bold=True)
    base_url = "https://api.github.com/search/repositories"
    request = Request(f"{base_url}?{params}")
    request.add_header("Accept", "application/vnd.github.v3+json")

    result = []
    for item in json.load(urlopen(request))["items"]:
        result.append(
            {
                "name": item["name"],
                "full_name": item["full_name"],
                "description": item["description"],
                "ssh_url": item["ssh_url"],
                "html_url": item["html_url"],
                "visibility": item["visibility"],
                "updated_at": item["updated_at"],
                "created_at": item["created_at"],
            }
        )

    pprint(result, sort_dicts=False)


@cli.command()
@click.option("--all", is_flag=True)
def clone(all):
    links = io_handler("repo.txt", op="r")
    if all:
        click.secho("Command: repo clone --all ↩︎", fg="green", bold=True)
        for link in links:
            name = link.rpartition(".")[0].partition(":")[-1].partition("/")[-1]
            if not Path(name).is_dir():
                click.secho(f"clone {link}", fg="yellow", bold=True)
                subprocess.run(["git", "clone", link])
    else:
        click.secho("Command: repo clone ↩︎", fg="green", bold=True)
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
            click.secho(f"git clone {link}", fg="yellow", bold=True)
            subprocess.run(["git", "clone", link])
    _sync()


@cli.command()
@click.option("--all", is_flag=True)
def pull(all):
    repos = repo_cloned()
    if all:
        click.secho("Command: repo pull --all ↩︎", fg="green", bold=True)
        for dir in repos.values():
            with cd(dir):
                click.secho(f"cd {dir.name}; git pull", fg="yellow", bold=True)
                subprocess.run(["git", "pull"])

    else:
        click.secho("Command: repo pull ↩︎", fg="green", bold=True)
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
            click.secho(f"cd {name}; git pull", fg="yellow", bold=True)
            subprocess.run(["git", "pull"])


@cli.command()
@click.option("-o", "--output", defalut=repo.txt)
def sync(output):
    click.secho(f"Command: repo sync ↩︎", fg="green", bold=True)
    _sync()


if __name__ == "__main__":
    cli()
