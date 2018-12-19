from fabric import Connection, Config, Group
from fabric import task
from invoke.config import merge_dicts

from pprint import pprint

class DeployConfig(Config):
    @staticmethod
    def global_defaults():
        hkn_defaults = {
            'deploy': {
                'hosts': ['apphost.ocf.berkeley.edu'],
                'path': '/home/h/hk/hkn/hknweb',
                'repo': 'git@github.com:compserv/hknweb.git',
                'branch': 'master',
                'linked_files': [],
                'linked_dirs': [],
                'keep_releases': 5,
            },
        }
        return merge_dicts(Config.global_defaults(), hkn_defaults)

targets = {
    'prod': dict(
        branch = 'master',
    ),
    'dev': dict(
        branch = 'develop',
    ),
}

configs = { target: DeployConfig(overrides=config)
            for target, config in targets.items() }

pprint(vars(configs['prod']))

def create_release(c):
    print("Creating release...")

def symlink_shared(c):
    print("Symlinking shared files...")

def symlink_release(c):
    print("Symlinking current@ to release...")

def update(c):
    create_release(c)
    symlink_shared(c)

def publish(c):
    symlink_release(c)

@task
def deploy(c):
    for connection in Group(c.hosts):
        update(connection)
        publish(connection)

@task
def rollback(c, release=None):
    pass
