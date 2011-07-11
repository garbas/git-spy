import os
import git
import ConfigParser


def main():

    config_file = os.environ.get('GIT_SPY', '~/.gitspy')
    if os.environ.has_key('HOME'):
        config_file = config_file.replace('~', os.environ.get('HOME'))
    if not os.path.exists(config_file):
        return

    config = ConfigParser.SafeConfigParser()
    config.read(config_file)

    if not config.has_section('main'):
        return
    if not config.has_option('main', 'repositories'):
        return


    for repo in config.get('main', 'repositories').split('\n'):
        repo = git.Repo(repo)

        # get loast local state for all remotes all refs

        import ipdb; ipdb.set_trace()
        
        #get last commits in current remote ref
        local_commits, remote_commits, local_refs, remote_refs = {}, [], [], []
        for rem in self.repo.remotes.origin.refs:
            try:
                local_refs.append(rem.name)
                local_commits[rem.remote_head] = rem.commit
            except Exception as e:
                if verbose:
                    print u'Failed getting remote branch %s on repo %s: %s' % (rem.name,
                                                                 self.name, e)
        try:
