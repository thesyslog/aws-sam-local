"""
Common CLI options for invoke command
"""
from pathlib import Path

import click
import logging

from samcli.commands._utils.options import template_click_option, docker_click_options, parameter_override_click_option
from samcli.commands.local.cli_common.invoke_context import ContainersInitializationMode

SRE_LOOGER = logging.getLogger(" " + __file__ )

def get_application_dir():
    """

    Returns
    -------
    Path
        Path representing the application config directory
    """
    # TODO: Get the config directory directly from `GlobalConfig`

    SRE_DEF_NAME = get_application_dir.__name__
    SRE_LOOGER.error( "here  file: samcli.cli.commands.local.cli_common.options --  def " +  SRE_DEF_NAME + "path: " + Path(click.get_app_dir("AWS SAM", force_posix=True)))
    
    print( f"app_dir = {Path(click.get_app_dir("AWS SAM", force_posix=True)))}")

    return Path(click.get_app_dir("AWS SAM", force_posix=True))


def get_default_layer_cache_dir():
    """
    Default the layer cache directory

    Returns
    -------
    str
        String representing the layer cache directory
    """
    SRE_DEF_NAME = get_default_layer_cache_dir.__name__
    SRE_LOOGER.error( "here file: samcli.cli.commands.local.cli_common.options --   def " +  SRE_DEF_NAME)
    
    layer_cache_dir = get_application_dir().joinpath("layers-pkg")

    print( f"layer_cache_dir = {str(layer_cache_dir)}" )

    return str(layer_cache_dir)


def local_common_options(f):
    """
    Common CLI options shared by "local invoke", "local start-api", and "local start-lambda" commands

    :param f: Callback passed by Click
    """
    SRE_DEF_NAME = local_common_options.__name__
    SRE_LOOGER.error( "here file: samcli.cli.commands.local.cli_common.options --   def " +  SRE_DEF_NAME)
    
    local_options = [
        click.option(
            "--shutdown",
            is_flag=True,
            default=False,
            help="If set, will emulate a shutdown event after the invoke completes, "
            "in order to test extension handling of shutdown behavior.",
        ),
        click.option(
            "--container-host",
            default="localhost",
            show_default=True,
            help="Host of locally emulated Lambda container. "
            "This option is useful when the container runs on a different host than SAM CLI. "
            "For example, if you want to run SAM CLI in a Docker container on macOS, "
            "use this option with host.docker.internal",
        ),
        click.option(
            "--container-host-interface",
            default="127.0.0.1",
            show_default=True,
            help="IP address of the host network interface that container ports should bind to. "
            "Use 0.0.0.0 to bind to all interfaces.",
        ),
    ]

    # Reverse the list to maintain ordering of options in help text printed with --help
    for option in reversed(local_options):
        option(f)

    return f


def service_common_options(port):
    """
    Construct common CLI Options that are shared for service related commands ('start-api' and 'start_lambda')

    Parameters
    ----------
    port
        The port number to listen to
    """
    SRE_DEF_NAME = service_common_options.__name__
    SRE_LOOGER.error( "here file: samcli.cli.commands.local.cli_common.options --   def " +  SRE_DEF_NAME)
    

    def construct_options(f):
        """
        Common CLI Options that are shared for service related commands ('start-api' and 'start_lambda')

        Parameters
        ----------
        f function
            Callback passed by Click
        port int
            port number to use

        Returns
        -------
        function
            The callback function
        """
        SRE_DEF_NAME = construct_options.__name__
        SRE_LOOGER.error( "here file: samcli.cli.commands.local.cli_common.options --   def " +  SRE_DEF_NAME)
    
        service_options = [
            click.option(
                "--host", default="127.0.0.1", help="Local hostname or IP address to bind to (default: '127.0.0.1')"
            ),
            click.option(
                "--port", "-p", default=port, help="Local port number to listen on (default: '{}')".format(str(port))
            ),
        ]

        # Reverse the list to maintain ordering of options in help text printed with --help
        for option in reversed(service_options):
            option(f)

        return f

    return construct_options


def invoke_common_options(f):
    """
    Common CLI options shared by "local invoke" and "local start-api" commands

    :param f: Callback passed by Click
    """
    SRE_DEF_NAME = invoke_common_options.__name__
    SRE_LOOGER.error( "here file: samcli.cli.commands.local.cli_common.options --   def " +  SRE_DEF_NAME)
    

    invoke_options = (
        [
            template_click_option(),
            click.option(
                "--env-vars",
                "-n",
                type=click.Path(exists=True),
                help="JSON file containing values for Lambda function's environment variables.",
            ),
            parameter_override_click_option(),
            click.option(
                "--debug-port",
                "-d",
                help="When specified, Lambda function container will start in debug mode and will expose this "
                "port on localhost.",
                envvar="SAM_DEBUG_PORT",
                type=click.INT,
                multiple=True,
            ),
            click.option(
                "--debugger-path", help="Host path to a debugger that will be mounted into the Lambda container."
            ),
            click.option(
                "--debug-args", help="Additional arguments to be passed to the debugger.", envvar="DEBUGGER_ARGS"
            ),
            click.option(
                "--container-env-vars",
                type=click.Path(exists=True),
                help="JSON file containing environment variables to be set within the container environment",
            ),
            click.option(
                "--docker-volume-basedir",
                "-v",
                envvar="SAM_DOCKER_VOLUME_BASEDIR",
                help="Specifies the location basedir where the SAM file exists. If the Docker is running on "
                "a remote machine, you must mount the path where the SAM file exists on the docker machine "
                "and modify this value to match the remote machine.",
            ),
            click.option("--log-file", "-l", help="logfile to send runtime logs to."),
            click.option(
                "--layer-cache-basedir",
                type=click.Path(exists=False, file_okay=False),
                envvar="SAM_LAYER_CACHE_BASEDIR",
                help="Specifies the location basedir where the Layers your template uses will be downloaded to.",
                default=get_default_layer_cache_dir(),
            ),
        ]
        + docker_click_options()
        + [
            click.option(
                "--force-image-build",
                is_flag=True,
                help="Specify whether CLI should rebuild the image used for invoking functions with layers.",
                envvar="SAM_FORCE_IMAGE_BUILD",
                default=False,
            )
        ]
    )

    # Reverse the list to maintain ordering of options in help text printed with --help
    for option in reversed(invoke_options):
        option(f)

    return f


def warm_containers_common_options(f):
    """
    Warm containers related CLI options shared by "local start-api" and "local start_lambda" commands

    :param f: Callback passed by Click
    """
    SRE_DEF_NAME = warm_containers_common_options.__name__
    SRE_LOOGER.error( "here file: samcli.cli.commands.local.cli_common.options --  def " +  SRE_DEF_NAME)
    

    warm_containers_options = [
        click.option(
            "--warm-containers",
            help="""
            \b
            Optional. Specifies how AWS SAM CLI manages 
            containers for each function.
            Two modes are available:
            EAGER: Containers for all functions are 
            loaded at startup and persist between 
            invocations.
            LAZY:  Containers are only loaded when each 
            function is first invoked. Those containers 
            persist for additional invocations.
            """,
            type=click.Choice(ContainersInitializationMode.__members__, case_sensitive=False),
        ),
        click.option(
            "--debug-function",
            help="Optional. Specifies the Lambda Function logicalId to apply debug options to when"
            " --warm-containers is specified.  This parameter applies to --debug-port, --debugger-path,"
            " and --debug-args.",
            type=click.STRING,
            multiple=False,
        ),
    ]

    # Reverse the list to maintain ordering of options in help text printed with --help
    for option in reversed(warm_containers_options):
        option(f)

    return f

def local_layer_options(f):
    """
    Common CLI options shared by "local invoke" and "local start-api" commands

    :param f: Callback passed by Click
    """
    SRE_DEF_NAME = "local_layer_options"
    SRE_LOOGER.error( "here file: samcli.cli.commands.local.cli_common.options --   def " +  SRE_DEF_NAME)
    

    local_layer_options = [
        click.option(
        "--layer-local-basedir",
        type=click.Path(exists=False, file_okay=False),
        envvar="SAM_LAYER_CACHE_BASEDIR",
        help="Specifies the location basedir where the Layers your template uses is to.",
        default=get_default_layer_cache_dir(),
        )
    ]
    # Reverse the list to maintain ordering of options in help text printed with --help
    for option in reversed(local_layer_options):
        option(f)

    return f