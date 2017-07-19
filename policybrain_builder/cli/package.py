import os.path

import click

from .repository import Repository


class Package(object):
    def __init__(self, name, repo, cachedir):
        self._name = name
        self._repo = repo
        self._cachedir = cachedir
        self._tag = None

    @property
    def name(self):
        return self._name

    @property
    def repo(self):
        return self._repo

    @property
    def tag(self):
        return self._tag

    @tag.setter
    def tag(self, value):
        self._tag = value

    @property
    def header(self):
        return click.style(self.name, fg='cyan')

    def pull(self, tag):
        if self.repo.is_valid():
            click.echo("[{}] {}".format(self.header, click.style("resetting", fg='green')))
            self.repo.reset()

            click.echo("[{}] {}".format(self.header, click.style("pulling", fg='green')))
            self.repo.pull()
        else:
            click.echo("[{}] {}".format(self.header, click.style("removing", fg='green')))
            self.repo.remove()

            click.echo("[{}] {}".format(self.header, click.style("cloning", fg='green')))
            self.repo.clone()

        click.echo("[{}] {}".format(self.header, click.style("fetching", fg='green')))
        self.repo.fetch()

        if tag:
            self.tag = tag
        else:
            self.tag = self.repo.latest_tag()

        click.echo("[{}] {}".format(self.header, click.style("checking out '{}'".format(self.tag), fg='green')))
        self.repo.checkout(tag=self.tag)

    def build(self):
        click.echo("[{}] {}".format(self.header, click.style("archiving", fg='green')))
        return
        self.repo.archive(self.name, self.tag, self._cachedir)

        channel = "ospc"
        for py_version in ('2.7', '3.5', '3.6'):
            u.call("conda build -c {} --no-anaconda-upload --python {} {}".format(channel, py_version, conda_recipe))
            build_file = u.call("conda build --python {} {} --output")
            u.call("conda convert -p all {} -o .".format(build_file))

    def upload(self):
        click.echo("[{}] {}".format(self.header, click.style("uploading", fg='green')))
        #u.call("anaconda [-t $OSPC_UPLOAD_TOKEN] upload $force --no-progress $1 --label $OSPC_ANACONDA_CHANNEL")


def get_packages(names, workdir):
    pkgs = {
        'taxcalc': Package(
            'taxcalc',
            Repository(
                'https://github.com/open-source-economics/Tax-Calculator',
                os.path.join(workdir, 'src', 'taxcalc')),
            os.path.join(workdir, 'pkg')),
        'btax': Package(
            'btax',
            Repository(
                'https://github.com/open-source-economics/B-Tax',
                os.path.join(workdir, 'src', 'btax')),
            os.path.join(workdir, 'pkg')),
        'ogusa': Package(
            'ogusa',
            Repository(
                'https://github.com/open-source-economics/OG-USA',
                os.path.join(workdir, 'src', 'ogusa')),
            os.path.join(workdir, 'pkg'))}
    keys = names if names else pkgs.keys()
    return [pkgs[name] for name in keys]
