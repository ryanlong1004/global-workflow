"""
view.py

CLI View layer

author: Kyle Nevins <kyle.nevina@noaa.gov>
        Ryan Long <ryan.long@noaa.gov>
"""

import argparse
import os

class ViewCLI:
    """interfaces user via cli"""

    @classmethod
    def get_args(cls):
        """get_args display CLI to user and gets options

        Returns:
            Namespace: object-
        """
        parser = argparse.ArgumentParser(
            description=""" Create the workflow files for
                                ecFlow by deploying scripts and definition
                                files or Rocoto""",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )
        parser.add_argument(
            "--ecflow-config",
            type=str,
            default="ecflow_build.yml",
            required=False,
            help="ecFlow Generator configuration file",
        )
        parser.add_argument(
            "--expdir",
            type=str,
            required=False,
            default=os.environ["PWD"],
            help="""This is to be the full path to experiment'
                        'directory containing config files""",
        )
        parser.add_argument(
            "--savedir",
            type=str,
            default=os.environ["PWD"],
            required=False,
            help="Location to save the definition files",
        )
        return parser.parse_args()
