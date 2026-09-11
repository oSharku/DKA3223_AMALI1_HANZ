#!/usr/bin/env python3
"""
Minimal safe wrapper to stage, commit, and push a notebook file.
Usage: python3 git_auto_push.py "commit message"

If GITHUB_TOKEN is set in environment, it will be used to authenticate the push
without exposing the token in git config. The script will restore the original
origin URL after the push.
"""
import os
import shlex
import subprocess
import sys

REPO_URL = "https://github.com/oSharku/DKA3223_AMALI1_HANZ.git"
BRANCH = "main"
NOTEBOOK = "DKA3223_AMALI1_HANZ.ipynb"

if len(sys.argv) < 2 or not sys.argv[1].strip():
    print('Usage: python3 git_auto_push.py "commit message"')
    sys.exit(2)

msg = sys.argv[1]

def run(cmd, check=True):
    print(f"$ {cmd}")
    return subprocess.run(shlex.split(cmd), check=check)

# check git repo
try:
    run("git rev-parse --is-inside-work-tree", check=True)
except Exception:
    print("Error: not inside a git repo. Clone first:", REPO_URL)
    sys.exit(1)

if not os.path.isfile(NOTEBOOK):
    print(f"Error: {NOTEBOOK} not found")
    sys.exit(1)

run(f"git add -- {shlex.quote(NOTEBOOK)}")

# check staged changes
staged = subprocess.run(["git","diff","--no-ext-diff","--cached","--quiet"])
if staged.returncode == 0:
    print("No changes staged for commit.")
    run("git --no-pager log --oneline -n 3")
    sys.exit(0)

run(f'git commit -m {shlex.quote(msg)}')

token = os.environ.get("GITHUB_TOKEN")
if token:
    orig = subprocess.check_output(["git","remote","get-url","origin"], text=True).strip()
    try:
        auth_url = f"https://x-access-token:{token}@github.com/oSharku/DKA3223_AMALI1_HANZ.git"
        run(f"git remote set-url origin {shlex.quote(auth_url)}")
        run(f"git push origin {BRANCH}")
    finally:
        run(f"git remote set-url origin {shlex.quote(orig)}")
else:
    run(f"git push origin {BRANCH}")

run("git --no-pager log --oneline -n 3")
