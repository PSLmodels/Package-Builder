import os
import shutil

import click

from . import utils as u


class Repository(object):
    def __init__(self, url, path):
        self._url = url
        self._path = path

    @property
    def url(self):
        return self._url

    @property
    def path(self):
        return self._path

    def is_valid(self):
        if not os.path.exists(self.path):
            return False
        with u.change_working_directory(self.path):
            is_git = u.check_output("git rev-parse --is-inside-work-tree").strip()
            if is_git != "true":
                return False
            url = u.check_output("git ls-remote --get-url").strip()
            if url != self.url:
                return False
        return True

    def remove(self):
        click.echo("removing {}".format(self.path))
        if os.path.exists(self.path):
            shutil.rmtree(self.path)

    def reset(self):
        with u.change_working_directory(self.path):
            u.call("git checkout .")

    def clone(self):
        click.echo("cloning {} to {}".format(self.url, self.path))
        u.call("git clone {} {}".format(self.url, self.path))

    def latest_tag(self):
        tags = None
        with u.change_working_directory(self.path):
            output = u.check_output("git tag")
            tags = sorted(output.splitlines())
        return tags[-1] if tags else None

    def fetch(self):
        with u.change_working_directory(self.path):
            click.echo("fetching origin/tags for {}".format(self.path))
            u.call("git fetch origin")
            u.call("git fetch origin --tags")

    def pull(self):
        with u.change_working_directory(self.path):
            u.call("git pull origin master")

    def checkout(self, branch='master', tag=None):
        with u.change_working_directory(self.path):
            if tag:
                click.echo("checking out tag '{}'".format(tag))
                u.call("git checkout " + tag)
            else:
                click.echo("checking out branch '{}'".format(branch))
                u.call("git checkout " + branch)

    def archive(self, name, tag, archive_path):
        with u.change_working_directory(self.path):
            click.echo("archiving {}".format(self.path))
            u.ensure_directory_exists(archive_path)
            u.call("git archive --prefix={0}/ -o {2}/{0}.tar {1}".format(name, tag, archive_path))
