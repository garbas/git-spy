import os
import ConfigParser

from argh import arg
from argh.helpers import confirm
from argh import ArghParser
from argh.exceptions import CommandError
from git.cmd import Git
from git.exc import GitCommandError

from gitspy.utils import getch


class Commands(object):

    def __init__(self, config_fp):
        self._cache = {}
        self.config_change = False
        self.config_fp = config_fp

        self.config = ConfigParser.SafeConfigParser()
        self.config.readfp(config_fp)

    def __iter__(self):
        for i in ['list', 'add', 'rm', 'status']:
            yield getattr(self, i)

    def config_write(self):
        if not self.config.has_section('main'):
            self.config.add_section('main')
        self.config.set('main', 'repositories',
                '\n' + '\n'.join(sorted(self.repos)))
        config_fp_writable = open(self.config_fp.name, 'w+')
        self.config.write(config_fp_writable)
        config_fp_writable.close()

    @property
    def repos(self):
        if 'repos' not in self._cache.keys():
            if not self.config.has_section('main') or \
               not self.config.has_option('main', 'repositories'):
                self._cache['repos'] = set([])
            else:
                self._cache['repos'] = set([i.strip() for i in
                    self.config.get('main', 'repositories').split('\n')
                    if i])
        return self._cache['repos']

    def repos_listing(self, repos):
        for i, repo in repos:
            yield '    %s.) %s' % (i+1, repo)

    def list(self, args):
        if len(self.repos) == 0:
            yield 'List empty.'
        else:
            yield 'Listing repositories:'
            for line in self.repos_listing(enumerate(self.repos)):
                yield line

    def rm(self, args):
        if len(self.repos) == 0:
            yield 'List empty. Nothing to delete.'
        else:
            yield 'Choose repository to remove from list:'
            yield '    0.) Exit'
            for line in self.repos_listing(enumerate(self.repos)):
                yield line
    
            prompt= ('Select repository [0-%s]: ' % len(self.repos)).encode('utf-8')
            try:
                correct_option_selected = True
                while correct_option_selected:
                    repo_to_remove = getch(prompt)
                    try:
                        repo_to_remove = int(repo_to_remove)
                        if repo_to_remove <= len(self.repos) and \
                           repo_to_remove >= 0:
                            correct_option_selected = True
                        correct_option_selected = False
                    except:
                        pass
            except KeyboardInterrupt:
                pass
    
            if repo_to_remove == 0:
                yield 'Exiting...'
    
            else:
                repo_to_remove = tuple(self.repos)[repo_to_remove-1]
                self.repos.remove(repo_to_remove)
                self.config_write()
                yield "'%s' removed from gitspy list." % repo_to_remove

    @arg('path', default='.', nargs='?',
            help="Path to repositoy. Default is repository in path")
    @arg('-n', '--name', required=False,
            help="Custom name for repository. Default is folder name.")
    def add(self, args):
        # make path absolute and check if exists
        path = os.path.abspath(args.path)
        if not os.path.isdir(path):
            raise CommandError(u'Directory does not exists: %s.' % path)
        
        # is git repo?
        if not os.path.exists(os.path.join(path, '.git')):
            raise CommandError(u'Not a git repository: %s' % path)

        # already in repositories list?
        if path in self.repos:
            raise CommandError(u'Repository already in list: %s.' % path)

        self.repos.add(path)
        self.config_write()
        yield "'%s' added to gitspy list." % path

    def status(self, args):
        yield 'Status of repositories:'


def main():
    config_file = os.environ.get('GIT_SPY', '~/.gitspy')
    if os.environ.has_key('HOME'):
        config_file = config_file.replace('~', os.environ.get('HOME'))
    if not os.path.exists(config_file):
        config_fp = open(config_file, 'w+')
    else:
        config_fp = open(config_file, 'r')

    commands = Commands(config_fp)

    parser = ArghParser()
    parser.add_commands(commands)
    parser.dispatch()
    config_fp.close()
