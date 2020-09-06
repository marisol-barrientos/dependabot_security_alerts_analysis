import subprocess
import os


def collect_npm_dependencies():
    """ It calls 'npm_dependencies.sh' to collect npm dependencies.
        """
    subprocess.call(['sh', '../scripts/npm_dependencies.sh'], stdout=open(os.devnull, 'w'), stderr=subprocess.STDOUT)


def collect_yarn_dependencies():
    """ It calls 'yarn_dependencies.sh' to collect yarn dependencies.
        """
    subprocess.call(['sh', '../scripts/yarn_dependencies.sh'], stdout=open(os.devnull, 'w'), stderr=subprocess.STDOUT)
