import logging
import os
import shutil

import click

from . import utils as u

logger = logging.getLogger(__name__)

PLATFORMS = ('osx-64', 'linux-32', 'linux-64', 'win-32', 'win-64')


class Package(object):
    def __init__(self, name, repo, cachedir, dependencies=[]):
        self._name = name
        self._dependencies = dependencies
        self._cachedir = cachedir
        self._tag = None

        repo.path = os.path.join(self.pull_cachedir, name)
        self._repo = repo

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
    def pull_cachedir(self):
        return os.path.join(self.cachedir, "pull")

    @property
    def build_cachedir(self):
        return os.path.join(self.cachedir, "build")

    @property
    def upload_cachedir(self):
        return os.path.join(self.cachedir, "upload")

    @property
    def tag(self):
        return self._tag

    @tag.setter
    def tag(self, value):
        self._tag = value

    @property
    def header(self):
        return click.style(self.name, fg='cyan')

    def pull(self):
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

        if not self.tag:
            self.tag = self.repo.latest_tag()

        click.echo("[{}] {}".format(self.header, click.style("checking out '{}'".format(self.tag), fg='green')))
        self.repo.checkout(tag=self.tag)

        click.echo("[{}] {}".format(self.header, click.style("archiving", fg='green')))
        self.repo.archive(self.name, self.tag, self.build_cachedir)

    def build(self, channel, py_versions):
        # Clear cached directory for uploads
        for platform in PLATFORMS:
            dst = os.path.join(self.upload_cachedir, self.name, platform)
            if os.path.exists(dst):
                shutil.rmtree(dst)

        with u.change_working_directory(self.build_cachedir):
            u.call("tar xvf {}-{}.tar".format(self.name, self.tag))

        archivedir = os.path.join(self.build_cachedir, "{}-{}".format(self.name, self.tag))
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
                    for platform in PLATFORMS:
                        if platform == current_platform:
                            continue
                        click.echo("[{}] {}".format(self.header, click.style("converting to {}".format(platform), fg='green')))
                        u.call("conda convert --platform {} {} -o ../".format(platform, package))

                # Copy package to cache directory for upload
                click.echo("[{}] {}".format(self.header, click.style("caching packages", fg='green')))
                for platform in PLATFORMS:
                    dst = os.path.join(self.upload_cachedir, self.name, platform)
                    u.ensure_directory_exists(dst)
                    shutil.copy(build_file, os.path.join(dst, package))

    def upload(self, token, label, user=None, force=False):
        cmd = "anaconda"

        if token:
            logger.info("config for anaconda upload: token was provided")
            cmd += " --token " + token
        else:
            logger.info("config for anaconda upload: token was not provided")

        cmd += " upload --no-progress"

        if force:
            logger.info("config for anaconda upload: force is enabled")
            cmd += " --force"
        else:
            logger.info("config for anaconda upload: force is disabled")

        logger.info("config for anaconda upload: label={}".format(label))
        if label:
            cmd += " --label " + label

        logger.info("config for anaconda upload: user={}".format(user))
        if user:
            cmd += " --user " + user

        for platform in PLATFORMS:
            click.echo("[{}] {}".format(self.header, click.style("uploading {} packages".format(platform), fg='green')))
            tmpdir = os.path.join(self.upload_cachedir, self.name, platform)

            pkgs = [f for f in os.listdir(tmpdir) if os.path.isfile(os.path.join(tmpdir, f))]
            for pkg in pkgs:
                fullpkg = os.path.join(tmpdir, pkg)
                logger.info("uploading " + fullpkg)
                try:
                    u.call("{} {}".format(cmd, fullpkg))
                except:
                    logger.error("Failed on anaconda upload likely because version already exists - continuing")
