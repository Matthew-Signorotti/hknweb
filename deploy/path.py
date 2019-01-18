import posixpath

from fabric import Connection

def deploy_path(c: Connection) -> str:
    return posixpath.join(c.deploy.path.root, c.deploy.name)

def repo_path(c: Connection) -> str:
    return posixpath.join(deploy_path(c), c.deploy.path.repo)

def releases_path(c: Connection) -> str:
    return posixpath.join(deploy_path(c), c.deploy.path.releases)

def current_path(c: Connection) -> str:
    return posixpath.join(deploy_path(c), c.deploy.path.current)

def shared_path(c: Connection) -> str:
    return posixpath.join(deploy_path(c), c.deploy.path.shared)

def release_path(c: Connection) -> str:
    return posixpath.join(releases_path(c), c.release)