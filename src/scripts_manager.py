import subprocess
import os

def collect_npm_dependencies():
    # print("         Collecting npm dependencies ...")
    subprocess.call(['sh', '../scripts/npm_dependencies.sh'], stdout=open(os.devnull, 'w'), stderr=subprocess.STDOUT)


def collect_yarn_dependencies():
    # print("         Collecting yarn dependencies ...")
    subprocess.call(['sh', '../scripts/yarn_dependencies.sh'], stdout=open(os.devnull, 'w'), stderr=subprocess.STDOUT)
