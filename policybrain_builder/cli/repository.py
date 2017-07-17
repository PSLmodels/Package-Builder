import os
import shutil

import click

from .utils import call, change_working_directory, check_output


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

    def remove(self):
        click.echo("removing {}".format(self.path))
        if os.path.exists(self.path):
            shutil.rmtree(self.path)

    def clone(self):
        click.echo("cloning {} to {}".format(self.url, self.path))
        call("git clone {} {}".format(self.url, self.path))

    def latest_tag(self):
        tags = None
        with change_working_directory(self.path):
            output = check_output("git tag")
            tags = sorted(output.splitlines())
        return tags[-1] if tags else None

    def fetch(self):
        with change_working_directory(self.path):
            click.echo("fetching origin/tags for {}".format(self.path))
            call("git fetch origin")
            call("git fetch origin --tags")

    def checkout(self, branch='master', tag=None):
        pass
