from fake.api import env
from fake.api import run
from fake.api import task
from fake.tasks.deploy import *

env.roledefs = {
    'prod': {
        'hosts': ['apphost.ocf.berkeley.edu'],
        'branch': 'master',
    },
}

env.forward_agent = True
env.deploy_path = '/home/h/hk/hkn/hknweb'
env.user = 'hkn'
env.repo_url = 'git@github.com:compserv/hknweb.git'
env.linked_dirs = ['config']
# env.keep_releases = 5


@task
def start():
    run('systemctl --user start hknweb.service')


@task
def stop():
    run('systemctl --user stop hknweb.service')


@task
def restart():
    run('systemctl --user restart hknweb.service')


after(finished, restart)
