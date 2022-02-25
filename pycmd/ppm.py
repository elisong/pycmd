# -*- coding: utf-8 -*-
# Usage:
#   ppm <command> [options]

# Commands:
#   install                     Install packages.
#   download                    Download packages.
#   uninstall                   Uninstall packages.
#   freeze                      Output installed packages in requirements format.
#   list                        List installed packages.
#   show                        Show information about installed packages.
#   check                       Verify installed packages have compatible dependencies.
#   config                      Manage local and global configuration.
#   search                      Search PyPI for packages.
#   cache                       Inspect and manage pip's wheel cache.
#   wheel                       Build wheels from your requirements.
#   hash                        Compute hashes of package archives.
#   completion                  A helper command used for command completion.
#   debug                       Show information useful for debugging.
#   help                        Show help for commands.

######################################################
# More packages related to `pip` environment
# - pipenv
# - Hatch
# - Poetry
# - flit
######################################################
import sys
from pathlib import Path
import subprocess
from pip._vendor.packaging.utils import canonicalize_name
from pip._internal.cli.main_parser import parse_command

args = sys.argv[1:]
cmd_name, cmd_args = parse_command(args)


def pip_freeze():
    freeze = subprocess.run(["pip", "freeze"], capture_output=True, text=True).stdout.strip()
    if freeze:
        return dict(i.split("==") for i in freeze.split("\n"))
    else:
        return {}


def update_reqs(pkgs):
    file = Path("requirements.txt")
    if not file.exists():
        file.open("w").close()
    with file.open("r+") as f:
        requires = {}
        for line in f.read().splitlines():
            pkg, ver = line.split("==")
            if cmd_name == "uninstall" and pkg in pkgs:
                continue
            else:
                requires[pkg] = ver.strip() + "\n"
        if cmd_name == "install":
            requires.update(pkgs)
        f.seek(0)
        f.writelines("==".join(item) for item in requires.items())
        f.truncate()


def main():

    if cmd_name in ("install", "uninstall"):
        pkgs_maybe = {canonicalize_name(i.split("==")[0]) for i in cmd_args if not i.startswith("-")}
        pkgs_before = pip_freeze()
        subprocess.run(["pip"] + args, check=False)
        pkgs_after = pip_freeze()

        pkgs_bfrset = set(canonicalize_name(i) for i in pkgs_before.keys())
        pkgs_afrset = set(canonicalize_name(i) for i in pkgs_after.keys())
        if cmd_name == "install":
            pkgs = (pkgs_afrset - pkgs_bfrset) & pkgs_maybe
            if pkgs:
                add_pkgs = {k: v for k, v in pkgs_after.items() if k in pkgs}
                update_reqs(add_pkgs)
        else:
            pkgs = (pkgs_bfrset - pkgs_afrset) & pkgs_maybe
            if pkgs:
                rm_pkgs = {k: v for k, v in pkgs_before.items() if k in pkgs}
                update_reqs(rm_pkgs)
    else:
        subprocess.run(["pip"] + args, check=False)


if __name__ == "__main__":
    main()
