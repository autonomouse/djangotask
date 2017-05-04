#!/usr/bin/env python3
import os
import sys
import argparse
import subprocess
from config import PRIMARY_APP_NAME
from urllib import parse as urlparse


application = PRIMARY_APP_NAME
python_version = "python3"
manage_cmd = [python_version, "manage.py"]
jslibs_dir = os.path.join(application, "static")
test_runner = 'py.test-3'
geckodriver = 'v0.10.0/geckodriver-v0.10.0-linux64.tar.gz'
chromedriver = '2.29/chromedriver_linux64.zip'
tests_dir = 'tests'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command")
    parser.add_argument('extra', nargs='*')
    args = parser.parse_args()
    args_dict = {key: value for key, value in
                 [arg.split('=') for arg in args.extra]}
    private_methods = TaskBase().getAvailableMethods()
    tasks = Tasks()
    public_methods = tasks.getAvailableMethods()
    available_methods = [
        method for method in public_methods if method not in private_methods]
    if not hasattr(tasks, args.command):
        print("There is no '" + args.command + "' command.")
        print("Available commands: \n * " + "\n * ".join(available_methods))
        sys.exit()
    return getattr(tasks, args.command)(**args_dict)


class TaskBase():
    """Helper methods, not meant to be called from the cli. """

    def getAvailableMethods(self):
        return [func for func in dir(self) if callable(getattr(self, func)) and
                not func.startswith("__")]

    def run(self, cmd):
        subprocess.check_call(cmd)

    def shell(self, cmd):
        subprocess.call(cmd, shell=True)

    def manage(self, cmd):
        full_cmd = [item for item in manage_cmd]
        full_cmd.extend(cmd)
        return subprocess.check_output(full_cmd)

    def sudo(self, cmd):
        sudo_cmd = ["sudo"]
        sudo_cmd.extend(cmd)
        return subprocess.check_output(sudo_cmd)

    def apt(self, pkglist):
        self.sudo(["apt", "update"])
        print("Installing packages via apt")
        aptlist = ["apt", "-y", "--no-upgrade", "install"]
        endlist = ["--fix-missing"]
        aptlist.extend(pkglist)
        aptlist.extend(endlist)
        self.sudo(aptlist)

    def npm(self, pkglist):
        print("Installing packages via npm")
        npmlist = ["npm", "install", "--prefix", jslibs_dir]
        npmlist.extend(pkglist)
        self.run(["mkdir", "-p", jslibs_dir])
        self.run(npmlist)

    def pip(self, pkglist):
        print("Installing packages via pip")
        piplist = ["pip3", "install"]
        piplist.extend(pkglist)
        self.run(piplist)


class Tasks(TaskBase):
    """Tasks meant to be callable from the cli. """

    def schema(self, filetype="png"):
        """Generates an image depicting the current database schema. """
        dot = self.manage([
            "graph_models", "-X", "TimeStampedBaseModel", "-E", "-a"])
        with open(application + ".dot", "wb") as text_file:
            text_file.write(dot)
        self.run(["dot", "-T" + filetype, application + ".dot", "-o",
                  application + "_schema." + filetype])
        self.run(["rm", application + ".dot"])
        print("Schema generated at {0}_schema.{1}".format(
              application, filetype))

    def install_browser_drivers(self):
        mzla_repo = 'https://github.com/mozilla/geckodriver/releases/download/'
        chromedriver_repo = 'http://chromedriver.storage.googleapis.com/'
        drivers = [urlparse.urljoin(mzla_repo, geckodriver),
                   urlparse.urljoin(chromedriver_repo, chromedriver), ]
        for driver in drivers:
            try:
                os.remove(os.path.join(tests_dir, driver.split('/')[-1]))
            except FileNotFoundError:
                pass
            self.run(['wget', driver, '-P', tests_dir])
        self.run(['unzip', '-o', os.path.join(tests_dir,
                  'chromedriver_linux64.zip'), '-d', tests_dir])

    def install(self):
        self.apt([
            "python3-pip",
            "python3-pydot",
            "python3-venv",
            "npm", ])
        self.npm([
            "d3@3.5.17",
            "nvd3@1.8.3",
            "angular@1.5.8",
            "angular-nvd3@1.0.7",
            "angular-route@1.5.8",
            "angular-cookies@1.5.8",
            "angular-resource@1.5.8",
            "jquery@3.1.1",
            "bootstrap@3.3.7", ])
        self.pip([
            "Django==1.8.7",
            "django-extensions==1.7.8",
            "django-filter==1.0.2",
            "djangorestframework==3.6.2",
            "flake8==3.3.0",
            "mccabe==0.6.1",
            "py==1.4.33",
            "pycodestyle==2.3.1",
            "pyflakes==1.5.0",
            "pyparsing==2.2.0",
            "pytest==3.0.7",
            "pytz==2017.2",
            "requests==2.13.0",
            "selenium==3.0.0b3",
            "six==1.10.0",
            "selenium==3.0.0b3", ])
        self.install_browser_drivers()
        print("Done")

    def dev(self):
        self.manage(["collectstatic", "--noinput"])
        self.manage(["makemigrations"])
        self.manage(["migrate"])
        self.manage(["loaddata", "fake_data.yaml"])
        self.manage(["runserver"])

    def test(self):
        self.shell([test_runner + ' tests/functional_tests.py', '-v'])
        try:
            self.run(['flake8', '.',
                      '--exclude=./{0}/migrations/'.format(PRIMARY_APP_NAME),
                      '--ignore=E402', ])
        except subprocess.CalledProcessError:
            pass


if __name__ == "__main__":
    sys.exit(main())
