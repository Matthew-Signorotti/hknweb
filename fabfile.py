from fabric import Connection, Config, Group
from fabric import task

class DeployConfig(Config):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_defaults(dict(
            deploy_path = '/home/h/hk/hkn/hknweb',
            repo_url = 'git@github.com:compserv/hknweb.git',
            branch = 'master',
            hosts = ['apphost.ocf.berkeley.edu'],
            user = 'hkn',
            linked_files = [],
            linked_dirs = [],
            keep_releases = 5,
        ), merge=True)

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

print(configs)

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
