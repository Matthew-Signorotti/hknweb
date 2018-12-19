from fabric import Connection

from .path import repo_path

def repo_exists(c: Connection) -> bool:
    return c.run("[ -f {}/HEAD ]".format(repo_path(c)), warn=True)

def remote_reachable(c: Connection) -> bool:
    c.run("cd {}".format(repo_path(c)), warn=True, hide=True)
    return c.run("git ls-remote {}".format(c.deploy.repo_url), warn=True)

def check(c: Connection):
    if remote_reachable(c):
        if repo_exists(c):
            update(c)
        else:
            clone(c)
    else:
        raise RuntimeError("remote not reachable")

def clone(c: Connection):
    c.run("git clone --bare {} {}".format(c.deploy.repo_url, repo_path(c)))

def update(c: Connection):
    c.run("cd {}".format(repo_path(c)))
    c.run("git fetch")
    c.run("git checkout {}".format(c.deploy.branch))

def release(c: Connection):
    pass