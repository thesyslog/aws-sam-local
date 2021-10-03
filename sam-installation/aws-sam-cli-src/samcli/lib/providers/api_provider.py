"""Class that provides the Api with a list of routes from a Template"""

import logging
from typing import List, Optional, Iterator

from samcli.lib.providers.api_collector import ApiCollector
from samcli.lib.providers.cfn_api_provider import CfnApiProvider
from samcli.lib.providers.cfn_base_api_provider import CfnBaseApiProvider
from samcli.lib.providers.provider import AbstractApiProvider, Stack, Api
from samcli.lib.providers.sam_api_provider import SamApiProvider

LOG = logging.getLogger(__name__)

SRE_LOOGER = logging.getLogger(" " + __file__ )


class ApiProvider(AbstractApiProvider):
    def __init__(self, stacks: List[Stack], cwd: Optional[str] = None):
        """
        Initialize the class with template data. The template_dict is assumed
        to be valid, normalized and a dictionary. template_dict should be normalized by running any and all
        pre-processing before passing to this class.
        This class does not perform any syntactic validation of the template.

        After the class is initialized, changes to ``template_dict`` will not be reflected in here.
        You will need to explicitly update the class with new template, if necessary.

        Parameters
        ----------
        stacks : dict
            List of stacks apis are extracted from
        cwd : str
            Optional working directory with respect to which we will resolve relative path to Swagger file
        """

        SRE_CLASS_NAME = "ApiProvider"
        SRE_LOOGER.error( "file: samcli.lib.providers.api_provider -- class " +  SRE_CLASS_NAME)

        self.stacks = stacks

        # Store a set of apis
        self.cwd = cwd
        self.api = self._extract_api()
        self.routes = self.api.routes
        LOG.debug("%d APIs found in the template", len(self.routes))

    def get_all(self) -> Iterator[Api]:
        """
        Yields all the Apis in the current Provider

        :yields api: an Api object with routes and properties
        """

        SRE_CLASS_NAME = "get_all"
        SRE_LOOGER.error( "file: samcli.lib.providers.api_provider -- def " +  SRE_CLASS_NAME)

        yield self.api

    def _extract_api(self) -> Api:
        """
        Extracts all the routes by running through the one providers. The provider that has the first type matched
        will be run across all the resources

        Parameters
        ----------
        Returns
        ---------
        An Api from the parsed template
        """

        SRE_CLASS_NAME = "_extract_api"
        SRE_LOOGER.error( "file: samcli.lib.providers.api_provider -- def " +  SRE_CLASS_NAME)

        collector = ApiCollector()
        provider = ApiProvider.find_api_provider(self.stacks)
        provider.extract_resources(self.stacks, collector, cwd=self.cwd)
        return collector.get_api()

    @staticmethod
    def find_api_provider(stacks: List[Stack]) -> CfnBaseApiProvider:
        """
        Finds the ApiProvider given the first api type of the resource

        Parameters
        -----------
        stacks: List[Stack]
            List of stacks apis are extracted from

        Return
        ----------
        Instance of the ApiProvider that will be run on the template with a default of SamApiProvider
        """

        SRE_CLASS_NAME = "find_api_provider"
        SRE_LOOGER.error( "file: samcli.lib.providers.api_provider -- def " +  SRE_CLASS_NAME)

        for stack in stacks:
            for _, resource in stack.resources.items():
                if resource.get(CfnBaseApiProvider.RESOURCE_TYPE) in SamApiProvider.TYPES:
                    return SamApiProvider()

                if resource.get(CfnBaseApiProvider.RESOURCE_TYPE) in CfnApiProvider.TYPES:
                    return CfnApiProvider()

        return SamApiProvider()
