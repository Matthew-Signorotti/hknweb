from fabric import Connection, Config, Group
from fabric import task
from invoke import Collection
from invoke.config import merge_dicts

from pprint import pprint
from datetime import datetime
import posixpath

from deploy import git
from deploy import path

def timestamp(c: Connection) -> str:
    """
    Returns the server date-time, encoded as YYYYMMSS_HHMMSS.
    """
    return c.run("date +%Y%m%d_%H%M%S").stdout.strip()

def make_dirs(c: Connection):
    dirs = (
        c.repo_path,
        c.deploy_path,
        c.releases_path,
        c.shared_path,
        c.release_path,
    )
    for path in dirs:
        c.run("mkdir -p {}".format(path))

class DeployConfig(Config):
    @staticmethod
    def global_defaults():
        hkn_defaults = {
            'deploy': {
                'name': 'default',
                'host': 'apphost.ocf.berkeley.edu',
                'path': {
                    'root': '/home/h/hk/hkn/hknweb',
                    'repo': 'repo',
                    'releases': 'releases',
                    'current': 'current',
                    'shared': 'shared',
                },
                'repo_url': 'https://github.com/compserv/hknweb.git',
                'branch': 'master',
                'linked_files': [],
                'linked_dirs': [],
                'keep_releases': 10,
            },
        }
        return merge_dicts(Config.global_defaults(), hkn_defaults)


targets = {
    'prod': {
        'deploy': {
            'name': 'prod',
            'branch': 'master',
        },
    },
    'deploy': {
        'deploy': {
            'name': 'prod',
            'branch': 'deploy',
        },
    },
}

configs = { target: DeployConfig(overrides=config)
            for target, config in targets.items() }

# pprint(vars(configs['prod']))

def create_release(c):
    print("-- Creating release")
    git.check(c)
    git.update(c)
    c.commit = git.revision_number(c, c.commit)
    git.create_archive(c)

def symlink_shared(c):
    print("-- Symlinking shared files")
    print("(TODO: do something)")

def blackbox_decrypt(c):
    print("-- Decrypting secrets")
    with c.cd(c.release_path):
        c.run("blackbox_postdeploy", echo=True)

def symlink_release(c):
    print("-- Symlinking current@ to release")
    c.run("ln -s {} {}".format(c.release_path, c.current_path), echo=True)

def systemd_restart(c):
    print("-- Restarting systemd unit")
    c.run("systemctl --user restart hknweb.service", echo=True)

def setup(c, commit=None, release=None):
    print("== Setup ==")
    if release is None:
        c.release = timestamp(c)
    else:
        c.release = release
    c.deploy_path = path.deploy_path(c)
    c.repo_path = path.repo_path(c)
    c.releases_path = path.releases_path(c)
    c.current_path = path.current_path(c)
    c.shared_path = path.shared_path(c)
    c.release_path = path.release_path(c)
    if commit is None:
        c.commit = c.deploy.branch
    else:
        c.commit = commit
    print("release: {}".format(c.release))
    print("commit: {}".format(c.commit))
    make_dirs(c)

def update(c):
    print("== Update ==")
    create_release(c)
    symlink_shared(c)
    blackbox_decrypt(c)

def publish(c):
    print("== Publish ==")
    symlink_release(c)
    systemd_restart(c)

def finish(c):
    pass

@task
def deploy(c, commit=None):
    setup(c, commit=commit)
    update(c)
    publish(c)
    finish(c)
    c.close()

@task
def rollback(c, release=None):
    setup(c, release=release)
    update(c)
    publish(c)
    finish(c)

ns = Collection(deploy, rollback)
ns.configure(configs['deploy'])
