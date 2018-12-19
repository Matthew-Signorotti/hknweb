from fabric import Connection, Config, Group
from fabric import task
from invoke import Collection
from invoke.config import merge_dicts

from pprint import pprint
import posixpath

from deploy import git

class DeployConfig(Config):
    @staticmethod
    def global_defaults():
        hkn_defaults = {
            'forward_agent': True,
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
                'repo_url': 'git@github.com:compserv/hknweb.git',
                'branch': 'master',
                'linked_files': [],
                'linked_dirs': [],
                'keep_releases': 5,
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
    'dev': {
        'deploy': {
            'name': 'dev',
            'branch': 'develop',
        },
    },
}

configs = { target: DeployConfig(overrides=config)
            for target, config in targets.items() }

# pprint(vars(configs['prod']))

def create_release(c):
    print("Creating release...")
    git.check(c)

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
    update(c)
    publish(c)

@task
def rollback(c, release=None):
    pass

ns = Collection(deploy, rollback)
ns.configure(configs['prod'])