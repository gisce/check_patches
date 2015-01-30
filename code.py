from collections import OrderedDict

from fabric.api import *


def status_dict(directory):
    with cd(directory):
        status = OrderedDict()
        x = run("git describe --tags").split('-')
        labels = ['version', 'num patches', 'last_commit']
        for field, label in zip(x, labels):
            status[label] = field
        if 'last_commit' in status:
            commit_hash = status['last_commit'][1:]
            log = run("git log -n1 --format=%%s %(commit_hash)s"
            % locals(), pty=False).strip()
            status['last_commit'] = {
                'hash': commit_hash,
                'log': log
            }
        if 'num patches' in status:
            logs = run("git log --no-merges --format=%h%s "
            "{version}..{last_commit[hash]}".format(**status), pty=False)
            status['applied patches'] = OrderedDict()
            for log in logs.split('\n'):
                status['applied patches'][log[:7]] = log[7:]
        return status

def pretty(d, depth=0):
    depth = depth
    for k, v in d.items():
        if isinstance(v, dict):
            print '%s%s:' % ('    ' * depth, k.upper())
            pretty(v, depth=depth + 1)
        else:
            print '%s%s: %s' % ('    ' * depth, k.upper(), v)


def status(directory):
    with settings(hide('warnings', 'running', 'stdout', 'stderr')):
        status = status_dict(directory)
        pretty(status)
