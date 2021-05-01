# coding: utf-8

"""

launcher
***************

This script allow users to launch the dash web application.

Example:
        $ python launcher.py

"""

import os


# Set python path env variable
ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
os.environ['PYTHONPATH'] = ROOT_DIR

if __name__ == '__main__':

    os.system("python src/webApp/index.py")
