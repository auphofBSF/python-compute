# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import warnings
from typing import Callable, Dict, Optional, Sequence, Tuple

from google.api_core import gapic_v1  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore

import grpc  # type: ignore

from google.auth.transport.requests import AuthorizedSession

from google.cloud.compute_v1.types import compute

from .base import MachineTypesTransport, DEFAULT_CLIENT_INFO


class MachineTypesRestTransport(MachineTypesTransport):
    """REST backend transport for MachineTypes.

    The MachineTypes API.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "compute.googleapis.com",
        credentials: ga_credentials.Credentials = None,
        credentials_file: str = None,
        scopes: Sequence[str] = None,
        client_cert_source_for_mtls: Callable[[], Tuple[bytes, bytes]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.

            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if ``channel`` is provided.
            client_cert_source_for_mtls (Callable[[], Tuple[bytes, bytes]]): Client
                certificate to configure mutual TLS HTTP channel. It is ignored
                if ``channel`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
        """
        # Run the base constructor
        # TODO(yon-mg): resolve other ctor params i.e. scopes, quota, etc.
        # TODO: When custom host (api_endpoint) is set, `scopes` must *also* be set on the
        # credentials object
        super().__init__(
            host=host, credentials=credentials, client_info=client_info,
        )
        self._session = AuthorizedSession(
            self._credentials, default_host=self.DEFAULT_HOST
        )
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._prep_wrapped_messages(client_info)

    def aggregated_list(
        self,
        request: compute.AggregatedListMachineTypesRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.MachineTypeAggregatedList:
        r"""Call the aggregated list method over HTTP.

        Args:
            request (~.compute.AggregatedListMachineTypesRequest):
                The request object. A request message for
                MachineTypes.AggregatedList. See the
                method description for details.

            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.compute.MachineTypeAggregatedList:

        """

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/aggregated/machineTypes".format(
            host=self._host, project=request.project,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {}
        if compute.AggregatedListMachineTypesRequest.filter in request:
            query_params["filter"] = request.filter
        if compute.AggregatedListMachineTypesRequest.include_all_scopes in request:
            query_params["includeAllScopes"] = request.include_all_scopes
        if compute.AggregatedListMachineTypesRequest.max_results in request:
            query_params["maxResults"] = request.max_results
        if compute.AggregatedListMachineTypesRequest.order_by in request:
            query_params["orderBy"] = request.order_by
        if compute.AggregatedListMachineTypesRequest.page_token in request:
            query_params["pageToken"] = request.page_token
        if compute.AggregatedListMachineTypesRequest.return_partial_success in request:
            query_params["returnPartialSuccess"] = request.return_partial_success

        # TODO(yon-mg): further discussion needed whether 'python truthiness' is appropriate here
        #               discards default values
        # TODO(yon-mg): add test for proper url encoded strings
        query_params = ["{k}={v}".format(k=k, v=v) for k, v in query_params.items()]
        url += "?{}".format("&".join(query_params)).replace(" ", "+")

        # Send the request
        response = self._session.get(url,)

        # Raise requests.exceptions.HTTPError if the status code is >= 400
        response.raise_for_status()

        # Return the response
        return compute.MachineTypeAggregatedList.from_json(
            response.content, ignore_unknown_fields=True
        )

    def get(
        self,
        request: compute.GetMachineTypeRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.MachineType:
        r"""Call the get method over HTTP.

        Args:
            request (~.compute.GetMachineTypeRequest):
                The request object. A request message for
                MachineTypes.Get. See the method
                description for details.

            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.compute.MachineType:
                Represents a Machine Type resource.

                You can use specific machine types for your VM instances
                based on performance and pricing requirements. For more
                information, read Machine Types. (== resource_for
                {$api_version}.machineTypes ==)

        """

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/zones/{zone}/machineTypes/{machine_type}".format(
            host=self._host,
            project=request.project,
            zone=request.zone,
            machine_type=request.machine_type,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {}

        # TODO(yon-mg): further discussion needed whether 'python truthiness' is appropriate here
        #               discards default values
        # TODO(yon-mg): add test for proper url encoded strings
        query_params = ["{k}={v}".format(k=k, v=v) for k, v in query_params.items()]
        url += "?{}".format("&".join(query_params)).replace(" ", "+")

        # Send the request
        response = self._session.get(url,)

        # Raise requests.exceptions.HTTPError if the status code is >= 400
        response.raise_for_status()

        # Return the response
        return compute.MachineType.from_json(
            response.content, ignore_unknown_fields=True
        )

    def list(
        self,
        request: compute.ListMachineTypesRequest,
        *,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> compute.MachineTypeList:
        r"""Call the list method over HTTP.

        Args:
            request (~.compute.ListMachineTypesRequest):
                The request object. A request message for
                MachineTypes.List. See the method
                description for details.

            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.compute.MachineTypeList:
                Contains a list of machine types.
        """

        # TODO(yon-mg): need to handle grpc transcoding and parse url correctly
        #               current impl assumes basic case of grpc transcoding
        url = "https://{host}/compute/v1/projects/{project}/zones/{zone}/machineTypes".format(
            host=self._host, project=request.project, zone=request.zone,
        )

        # TODO(yon-mg): handle nested fields corerctly rather than using only top level fields
        #               not required for GCE
        query_params = {}
        if compute.ListMachineTypesRequest.filter in request:
            query_params["filter"] = request.filter
        if compute.ListMachineTypesRequest.max_results in request:
            query_params["maxResults"] = request.max_results
        if compute.ListMachineTypesRequest.order_by in request:
            query_params["orderBy"] = request.order_by
        if compute.ListMachineTypesRequest.page_token in request:
            query_params["pageToken"] = request.page_token
        if compute.ListMachineTypesRequest.return_partial_success in request:
            query_params["returnPartialSuccess"] = request.return_partial_success

        # TODO(yon-mg): further discussion needed whether 'python truthiness' is appropriate here
        #               discards default values
        # TODO(yon-mg): add test for proper url encoded strings
        query_params = ["{k}={v}".format(k=k, v=v) for k, v in query_params.items()]
        url += "?{}".format("&".join(query_params)).replace(" ", "+")

        # Send the request
        response = self._session.get(url,)

        # Raise requests.exceptions.HTTPError if the status code is >= 400
        response.raise_for_status()

        # Return the response
        return compute.MachineTypeList.from_json(
            response.content, ignore_unknown_fields=True
        )


__all__ = ("MachineTypesRestTransport",)
