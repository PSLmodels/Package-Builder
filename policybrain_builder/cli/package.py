import os.path
import shutil

import click

from . import utils as u


class Package(object):
    def __init__(self, name, repo, cachedir, dependencies=[]):
        self._name = name
        self._repo = repo
        self._dependencies = dependencies
        self._cachedir = cachedir
        self._tag = None

    @property
    def name(self):
        return self._name

    @property
    def repo(self):
        return self._repo

    @property
    def dependencies(self):
        return self._dependencies

    @property
    def cachedir(self):
        return self._cachedir

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

        click.echo("[{}] {}".format(self.header, click.style("archiving", fg='green')))
        self.repo.archive(self.name, self.tag, self.cachedir)

    def build(self):
        channel = "ospc"
        py_versions = ('2.7', '3.5', '3.6')
        platforms = ('osx-64', 'linux-32', 'linux-64', 'win-32', 'win-64')

        with u.change_working_directory(self.cachedir):
            u.call("tar xvf {}-{}.tar".format(self.name, self.tag))

        archivedir = os.path.join(self.cachedir, "{}-{}".format(self.name, self.tag))
        conda_recipe = u.find_first_filename(archivedir, "conda.recipe", "Python/conda.recipe")
        conda_meta = os.path.join(archivedir, conda_recipe, "meta.yaml")

        u.replace_all(conda_meta, r'version: .*', "version: " + self.tag)
        for pkg in self.dependencies:
            u.replace_all(conda_meta, "- {}.*".format(pkg.name), "- {} >={}".format(pkg.name, pkg.tag))

        with u.change_working_directory(archivedir):
            for py_version in py_versions:
                click.echo("[{}] {}".format(self.header, click.style("building {}".format(py_version), fg='green')))
                u.call("conda build -c {} --no-anaconda-upload --python {} {}".format(channel, py_version, conda_recipe))
                build_file = u.check_output("conda build --python {} {} --output".format(py_version, conda_recipe)).strip()
                build_dir = os.path.dirname(build_file)
                current_platform = os.path.basename(build_dir)
                package = os.path.basename(build_file)

                with u.change_working_directory(build_dir):
                    for platform in platforms:
                        if platform == current_platform:
                            continue
                        click.echo("[{}] {}".format(self.header, click.style("converting to {}".format(platform), fg='green')))
                        u.call("conda convert --platform {} {} -o ../".format(platform, package))

                # Copy package to cache directory for upload
                click.echo("[{}] {}".format(self.header, click.style("caching packages", fg='green')))
                for platform in platforms:
                    dst = os.path.join(self.cachedir, self.name, platform)
                    u.ensure_directory_exists(dst)
                    shutil.copy(build_file, os.path.join(dst, package))

    def upload(self):
        click.echo("[{}] {}".format(self.header, click.style("uploading", fg='green')))
        #u.call("anaconda [-t $OSPC_UPLOAD_TOKEN] upload $force --no-progress $1 --label $OSPC_ANACONDA_CHANNEL")
