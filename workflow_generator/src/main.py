#!/usr/bin/env python3
import os
import sys
from typing import ValuesView
from view import ViewCLI
sys.path.append(os.path.join(os.path.dirname(__file__), "../ush/rocoto"))

import workflow_utils as wfu





def main():
    """Main function to start the workflow generator

    This is the main function that will read in the command line arguments
    using the parse_command_line function and create an array for the
    environment configurations to be used throughout the application.

    For the ecFlow setup, it sets up a new workflow and then uses the generic
    functions which are available for the Rocoto setup as well of
    generate_workflow and save.

    ** Important note: This function does also pull from the ush/rocoto
    application to use the get_configs and config_parser functions to populate
    the environment variable array.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    args = ViewCLI().get_args()

    environment_configs = wfu.get_configs(args.expdir)
    envconfigs = {}
    envconfigs['base'] = wfu.config_parser([wfu.find_config('config.base',
                                            environment_configs)])

    # The default setup in the parse_command_line() function assumes that if
    # the --ecflow-config file is set that it should be an ecflow setup. When
    # Rocoto is implemented, the default for --ecflow-config should be removed
    # and additional parameters added.
    if args.ecflow_config is not None:
        from ecflow_setup.ecflow_setup import Ecflowsetup
        workflow = Ecflowsetup(args, envconfigs)
    else:
        import rocoto_setup

    workflow.generate_workflow()
    workflow.save()


# Main Initializer
if __name__ == "__main__":
    main()
    sys.exit(0)
