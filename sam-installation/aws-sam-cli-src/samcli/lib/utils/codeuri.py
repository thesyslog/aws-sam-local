"""
Contains CodeUri Related methods
"""

import os
import logging

LOG = logging.getLogger(__name__)

SRE_LOOGER = logging.getLogger(" " + __file__ )

PRESENT_DIR = "."


def resolve_code_path(cwd, codeuri):
    """
    Returns path to the function code resolved based on current working directory.

    Parameters
    ----------
    cwd str
        Current working directory
    codeuri
        CodeURI of the function. This should contain the path to the function code

    Returns
    -------
    str
        Absolute path to the function code

    """

    SRE_CLASS_NAME = "resolve_code_path"
    SRE_LOOGER.error( "file: samcli.lib.utils.codeuri -- def " +  SRE_CLASS_NAME)

    LOG.debug("Resolving code path. Cwd=%s, CodeUri=%s", cwd, codeuri)

    # First, let us figure out the current working directory.
    # If current working directory is not provided, then default to the directory where the CLI is running from
    if not cwd or cwd == PRESENT_DIR:
        cwd = os.getcwd()
        SRE_LOOGER.error( "------- cwd: " +  cwd )

    # Make sure cwd is an absolute path
    cwd = os.path.abspath(cwd)
    SRE_LOOGER.error( "------- cwd.abspath: " +  cwd )

    # Next, let us get absolute path of function code.
    # Codepath is always relative to current working directory
    # If the path is relative, then construct the absolute version
    if not os.path.isabs(codeuri):
        codeuri = os.path.normpath(os.path.join(cwd, codeuri))
        SRE_LOOGER.error( "------- codeuri: " +  codeuri )

    return codeuri
