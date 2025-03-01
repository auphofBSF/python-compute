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
import os
import mock
import packaging.version

import grpc
from grpc.experimental import aio
import math
import pytest
from proto.marshal.rules.dates import DurationRule, TimestampRule

from requests import Response
from requests.sessions import Session

from google.api_core import client_options
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.compute_v1.services.subnetworks import SubnetworksClient
from google.cloud.compute_v1.services.subnetworks import pagers
from google.cloud.compute_v1.services.subnetworks import transports
from google.cloud.compute_v1.services.subnetworks.transports.base import (
    _API_CORE_VERSION,
)
from google.cloud.compute_v1.services.subnetworks.transports.base import (
    _GOOGLE_AUTH_VERSION,
)
from google.cloud.compute_v1.types import compute
from google.oauth2 import service_account
import google.auth


# TODO(busunkim): Once google-api-core >= 1.26.0 is required:
# - Delete all the api-core and auth "less than" test cases
# - Delete these pytest markers (Make the "greater than or equal to" tests the default).
requires_google_auth_lt_1_25_0 = pytest.mark.skipif(
    packaging.version.parse(_GOOGLE_AUTH_VERSION) >= packaging.version.parse("1.25.0"),
    reason="This test requires google-auth < 1.25.0",
)
requires_google_auth_gte_1_25_0 = pytest.mark.skipif(
    packaging.version.parse(_GOOGLE_AUTH_VERSION) < packaging.version.parse("1.25.0"),
    reason="This test requires google-auth >= 1.25.0",
)

requires_api_core_lt_1_26_0 = pytest.mark.skipif(
    packaging.version.parse(_API_CORE_VERSION) >= packaging.version.parse("1.26.0"),
    reason="This test requires google-api-core < 1.26.0",
)

requires_api_core_gte_1_26_0 = pytest.mark.skipif(
    packaging.version.parse(_API_CORE_VERSION) < packaging.version.parse("1.26.0"),
    reason="This test requires google-api-core >= 1.26.0",
)


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"


# If default endpoint is localhost, then default mtls endpoint will be the same.
# This method modifies the default endpoint so the client can produce a different
# mtls endpoint for endpoint testing purposes.
def modify_default_endpoint(client):
    return (
        "foo.googleapis.com"
        if ("localhost" in client.DEFAULT_ENDPOINT)
        else client.DEFAULT_ENDPOINT
    )


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert SubnetworksClient._get_default_mtls_endpoint(None) is None
    assert (
        SubnetworksClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    )
    assert (
        SubnetworksClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        SubnetworksClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        SubnetworksClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert SubnetworksClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


@pytest.mark.parametrize("client_class", [SubnetworksClient,])
def test_subnetworks_client_from_service_account_info(client_class):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == "compute.googleapis.com:443"


@pytest.mark.parametrize("client_class", [SubnetworksClient,])
def test_subnetworks_client_from_service_account_file(client_class):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file("dummy/file/path.json")
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        client = client_class.from_service_account_json("dummy/file/path.json")
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == "compute.googleapis.com:443"


def test_subnetworks_client_get_transport_class():
    transport = SubnetworksClient.get_transport_class()
    available_transports = [
        transports.SubnetworksRestTransport,
    ]
    assert transport in available_transports

    transport = SubnetworksClient.get_transport_class("rest")
    assert transport == transports.SubnetworksRestTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [(SubnetworksClient, transports.SubnetworksRestTransport, "rest"),],
)
@mock.patch.object(
    SubnetworksClient, "DEFAULT_ENDPOINT", modify_default_endpoint(SubnetworksClient)
)
def test_subnetworks_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(SubnetworksClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(SubnetworksClient, "get_transport_class") as gtc:
        client = client_class(transport=transport_name)
        gtc.assert_called()

    # Check the case api_endpoint is provided.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class()
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class()
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError):
            client = client_class()

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError):
            client = client_class()

    # Check the case quota_project_id is provided
    options = client_options.ClientOptions(quota_project_id="octopus")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id="octopus",
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,use_client_cert_env",
    [
        (SubnetworksClient, transports.SubnetworksRestTransport, "rest", "true"),
        (SubnetworksClient, transports.SubnetworksRestTransport, "rest", "false"),
    ],
)
@mock.patch.object(
    SubnetworksClient, "DEFAULT_ENDPOINT", modify_default_endpoint(SubnetworksClient)
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_subnetworks_client_mtls_env_auto(
    client_class, transport_class, transport_name, use_client_cert_env
):
    # This tests the endpoint autoswitch behavior. Endpoint is autoswitched to the default
    # mtls endpoint, if GOOGLE_API_USE_CLIENT_CERTIFICATE is "true" and client cert exists.

    # Check the case client_cert_source is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        options = client_options.ClientOptions(
            client_cert_source=client_cert_source_callback
        )
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options)

            if use_client_cert_env == "false":
                expected_client_cert_source = None
                expected_host = client.DEFAULT_ENDPOINT
            else:
                expected_client_cert_source = client_cert_source_callback
                expected_host = client.DEFAULT_MTLS_ENDPOINT

            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=expected_host,
                scopes=None,
                client_cert_source_for_mtls=expected_client_cert_source,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
            )

    # Check the case ADC client cert is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=True,
            ):
                with mock.patch(
                    "google.auth.transport.mtls.default_client_cert_source",
                    return_value=client_cert_source_callback,
                ):
                    if use_client_cert_env == "false":
                        expected_host = client.DEFAULT_ENDPOINT
                        expected_client_cert_source = None
                    else:
                        expected_host = client.DEFAULT_MTLS_ENDPOINT
                        expected_client_cert_source = client_cert_source_callback

                    patched.return_value = None
                    client = client_class()
                    patched.assert_called_once_with(
                        credentials=None,
                        credentials_file=None,
                        host=expected_host,
                        scopes=None,
                        client_cert_source_for_mtls=expected_client_cert_source,
                        quota_project_id=None,
                        client_info=transports.base.DEFAULT_CLIENT_INFO,
                    )

    # Check the case client_cert_source and ADC client cert are not provided.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=False,
            ):
                patched.return_value = None
                client = client_class()
                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=client.DEFAULT_ENDPOINT,
                    scopes=None,
                    client_cert_source_for_mtls=None,
                    quota_project_id=None,
                    client_info=transports.base.DEFAULT_CLIENT_INFO,
                )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [(SubnetworksClient, transports.SubnetworksRestTransport, "rest"),],
)
def test_subnetworks_client_client_options_scopes(
    client_class, transport_class, transport_name
):
    # Check the case scopes are provided.
    options = client_options.ClientOptions(scopes=["1", "2"],)
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=["1", "2"],
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [(SubnetworksClient, transports.SubnetworksRestTransport, "rest"),],
)
def test_subnetworks_client_client_options_credentials_file(
    client_class, transport_class, transport_name
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


def test_aggregated_list_rest(
    transport: str = "rest", request_type=compute.AggregatedListSubnetworksRequest
):
    client = SubnetworksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.SubnetworkAggregatedList(
            id="id_value",
            items={
                "key_value": compute.SubnetworksScopedList(
                    subnetworks=[
                        compute.Subnetwork(
                            creation_timestamp="creation_timestamp_value"
                        )
                    ]
                )
            },
            kind="kind_value",
            next_page_token="next_page_token_value",
            self_link="self_link_value",
            unreachables=["unreachables_value"],
            warning=compute.Warning(code=compute.Warning.Code.CLEANUP_FAILED),
        )

        # Wrap the value into a proper Response obj
        json_return_value = compute.SubnetworkAggregatedList.to_json(return_value)
        response_value = Response()
        response_value.status_code = 200
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.aggregated_list(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.AggregatedListPager)
    assert response.id == "id_value"
    assert response.items == {
        "key_value": compute.SubnetworksScopedList(
            subnetworks=[
                compute.Subnetwork(creation_timestamp="creation_timestamp_value")
            ]
        )
    }
    assert response.kind == "kind_value"
    assert response.next_page_token == "next_page_token_value"
    assert response.self_link == "self_link_value"
    assert response.unreachables == ["unreachables_value"]
    assert response.warning == compute.Warning(code=compute.Warning.Code.CLEANUP_FAILED)


def test_aggregated_list_rest_from_dict():
    test_aggregated_list_rest(request_type=dict)


def test_aggregated_list_rest_flattened():
    client = SubnetworksClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.SubnetworkAggregatedList()

        # Wrap the value into a proper Response obj
        json_return_value = compute.SubnetworkAggregatedList.to_json(return_value)
        response_value = Response()
        response_value.status_code = 200
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.aggregated_list(project="project_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, http_call, http_params = req.mock_calls[0]
        body = http_params.get("data")
        assert "project_value" in http_call[1] + str(body)


def test_aggregated_list_rest_flattened_error():
    client = SubnetworksClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.aggregated_list(
            compute.AggregatedListSubnetworksRequest(), project="project_value",
        )


def test_aggregated_list_pager():
    client = SubnetworksClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Set the response as a series of pages
        response = (
            compute.SubnetworkAggregatedList(
                items={
                    "a": compute.SubnetworksScopedList(),
                    "b": compute.SubnetworksScopedList(),
                    "c": compute.SubnetworksScopedList(),
                },
                next_page_token="abc",
            ),
            compute.SubnetworkAggregatedList(items={}, next_page_token="def",),
            compute.SubnetworkAggregatedList(
                items={"g": compute.SubnetworksScopedList(),}, next_page_token="ghi",
            ),
            compute.SubnetworkAggregatedList(
                items={
                    "h": compute.SubnetworksScopedList(),
                    "i": compute.SubnetworksScopedList(),
                },
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(compute.SubnetworkAggregatedList.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        metadata = ()
        pager = client.aggregated_list(request={})

        assert pager._metadata == metadata

        assert isinstance(pager.get("a"), compute.SubnetworksScopedList)
        assert pager.get("h") is None

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, tuple) for i in results)
        for result in results:
            assert isinstance(result, tuple)
            assert tuple(type(t) for t in result) == (
                str,
                compute.SubnetworksScopedList,
            )

        assert pager.get("a") is None
        assert isinstance(pager.get("h"), compute.SubnetworksScopedList)

        pages = list(client.aggregated_list(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_delete_rest(
    transport: str = "rest", request_type=compute.DeleteSubnetworkRequest
):
    client = SubnetworksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            error=compute.Error(errors=[compute.Errors(code="code_value")]),
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id="id_value",
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id="target_id_value",
            target_link="target_link_value",
            user="user_value",
            warnings=[compute.Warnings(code=compute.Warnings.Code.CLEANUP_FAILED)],
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        json_return_value = compute.Operation.to_json(return_value)
        response_value = Response()
        response_value.status_code = 200
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.delete(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.error == compute.Error(errors=[compute.Errors(code="code_value")])
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == "id_value"
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == "target_id_value"
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.warnings == [
        compute.Warnings(code=compute.Warnings.Code.CLEANUP_FAILED)
    ]
    assert response.zone == "zone_value"


def test_delete_rest_from_dict():
    test_delete_rest(request_type=dict)


def test_delete_rest_flattened():
    client = SubnetworksClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # Wrap the value into a proper Response obj
        json_return_value = compute.Operation.to_json(return_value)
        response_value = Response()
        response_value.status_code = 200
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete(
            project="project_value",
            region="region_value",
            subnetwork="subnetwork_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, http_call, http_params = req.mock_calls[0]
        body = http_params.get("data")
        assert "project_value" in http_call[1] + str(body)
        assert "region_value" in http_call[1] + str(body)
        assert "subnetwork_value" in http_call[1] + str(body)


def test_delete_rest_flattened_error():
    client = SubnetworksClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete(
            compute.DeleteSubnetworkRequest(),
            project="project_value",
            region="region_value",
            subnetwork="subnetwork_value",
        )


def test_expand_ip_cidr_range_rest(
    transport: str = "rest", request_type=compute.ExpandIpCidrRangeSubnetworkRequest
):
    client = SubnetworksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            error=compute.Error(errors=[compute.Errors(code="code_value")]),
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id="id_value",
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id="target_id_value",
            target_link="target_link_value",
            user="user_value",
            warnings=[compute.Warnings(code=compute.Warnings.Code.CLEANUP_FAILED)],
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        json_return_value = compute.Operation.to_json(return_value)
        response_value = Response()
        response_value.status_code = 200
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.expand_ip_cidr_range(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.error == compute.Error(errors=[compute.Errors(code="code_value")])
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == "id_value"
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == "target_id_value"
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.warnings == [
        compute.Warnings(code=compute.Warnings.Code.CLEANUP_FAILED)
    ]
    assert response.zone == "zone_value"


def test_expand_ip_cidr_range_rest_from_dict():
    test_expand_ip_cidr_range_rest(request_type=dict)


def test_expand_ip_cidr_range_rest_flattened():
    client = SubnetworksClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # Wrap the value into a proper Response obj
        json_return_value = compute.Operation.to_json(return_value)
        response_value = Response()
        response_value.status_code = 200
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        subnetworks_expand_ip_cidr_range_request_resource = compute.SubnetworksExpandIpCidrRangeRequest(
            ip_cidr_range="ip_cidr_range_value"
        )
        client.expand_ip_cidr_range(
            project="project_value",
            region="region_value",
            subnetwork="subnetwork_value",
            subnetworks_expand_ip_cidr_range_request_resource=subnetworks_expand_ip_cidr_range_request_resource,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, http_call, http_params = req.mock_calls[0]
        body = http_params.get("data")
        assert "project_value" in http_call[1] + str(body)
        assert "region_value" in http_call[1] + str(body)
        assert "subnetwork_value" in http_call[1] + str(body)
        assert compute.SubnetworksExpandIpCidrRangeRequest.to_json(
            subnetworks_expand_ip_cidr_range_request_resource,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        ) in http_call[1] + str(body)


def test_expand_ip_cidr_range_rest_flattened_error():
    client = SubnetworksClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.expand_ip_cidr_range(
            compute.ExpandIpCidrRangeSubnetworkRequest(),
            project="project_value",
            region="region_value",
            subnetwork="subnetwork_value",
            subnetworks_expand_ip_cidr_range_request_resource=compute.SubnetworksExpandIpCidrRangeRequest(
                ip_cidr_range="ip_cidr_range_value"
            ),
        )


def test_get_rest(transport: str = "rest", request_type=compute.GetSubnetworkRequest):
    client = SubnetworksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Subnetwork(
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            enable_flow_logs=True,
            fingerprint="fingerprint_value",
            gateway_address="gateway_address_value",
            id="id_value",
            ip_cidr_range="ip_cidr_range_value",
            ipv6_cidr_range="ipv6_cidr_range_value",
            kind="kind_value",
            log_config=compute.SubnetworkLogConfig(
                aggregation_interval=compute.SubnetworkLogConfig.AggregationInterval.INTERVAL_10_MIN
            ),
            name="name_value",
            network="network_value",
            private_ip_google_access=True,
            private_ipv6_google_access=compute.Subnetwork.PrivateIpv6GoogleAccess.DISABLE_GOOGLE_ACCESS,
            purpose=compute.Subnetwork.Purpose.INTERNAL_HTTPS_LOAD_BALANCER,
            region="region_value",
            role=compute.Subnetwork.Role.ACTIVE,
            secondary_ip_ranges=[
                compute.SubnetworkSecondaryRange(ip_cidr_range="ip_cidr_range_value")
            ],
            self_link="self_link_value",
            state=compute.Subnetwork.State.DRAINING,
        )

        # Wrap the value into a proper Response obj
        json_return_value = compute.Subnetwork.to_json(return_value)
        response_value = Response()
        response_value.status_code = 200
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Subnetwork)
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.enable_flow_logs is True
    assert response.fingerprint == "fingerprint_value"
    assert response.gateway_address == "gateway_address_value"
    assert response.id == "id_value"
    assert response.ip_cidr_range == "ip_cidr_range_value"
    assert response.ipv6_cidr_range == "ipv6_cidr_range_value"
    assert response.kind == "kind_value"
    assert response.log_config == compute.SubnetworkLogConfig(
        aggregation_interval=compute.SubnetworkLogConfig.AggregationInterval.INTERVAL_10_MIN
    )
    assert response.name == "name_value"
    assert response.network == "network_value"
    assert response.private_ip_google_access is True
    assert (
        response.private_ipv6_google_access
        == compute.Subnetwork.PrivateIpv6GoogleAccess.DISABLE_GOOGLE_ACCESS
    )
    assert response.purpose == compute.Subnetwork.Purpose.INTERNAL_HTTPS_LOAD_BALANCER
    assert response.region == "region_value"
    assert response.role == compute.Subnetwork.Role.ACTIVE
    assert response.secondary_ip_ranges == [
        compute.SubnetworkSecondaryRange(ip_cidr_range="ip_cidr_range_value")
    ]
    assert response.self_link == "self_link_value"
    assert response.state == compute.Subnetwork.State.DRAINING


def test_get_rest_from_dict():
    test_get_rest(request_type=dict)


def test_get_rest_flattened():
    client = SubnetworksClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Subnetwork()

        # Wrap the value into a proper Response obj
        json_return_value = compute.Subnetwork.to_json(return_value)
        response_value = Response()
        response_value.status_code = 200
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get(
            project="project_value",
            region="region_value",
            subnetwork="subnetwork_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, http_call, http_params = req.mock_calls[0]
        body = http_params.get("data")
        assert "project_value" in http_call[1] + str(body)
        assert "region_value" in http_call[1] + str(body)
        assert "subnetwork_value" in http_call[1] + str(body)


def test_get_rest_flattened_error():
    client = SubnetworksClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get(
            compute.GetSubnetworkRequest(),
            project="project_value",
            region="region_value",
            subnetwork="subnetwork_value",
        )


def test_get_iam_policy_rest(
    transport: str = "rest", request_type=compute.GetIamPolicySubnetworkRequest
):
    client = SubnetworksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Policy(
            audit_configs=[
                compute.AuditConfig(
                    audit_log_configs=[
                        compute.AuditLogConfig(
                            exempted_members=["exempted_members_value"]
                        )
                    ]
                )
            ],
            bindings=[compute.Binding(binding_id="binding_id_value")],
            etag="etag_value",
            iam_owned=True,
            rules=[compute.Rule(action=compute.Rule.Action.ALLOW)],
            version=774,
        )

        # Wrap the value into a proper Response obj
        json_return_value = compute.Policy.to_json(return_value)
        response_value = Response()
        response_value.status_code = 200
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.get_iam_policy(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Policy)
    assert response.audit_configs == [
        compute.AuditConfig(
            audit_log_configs=[
                compute.AuditLogConfig(exempted_members=["exempted_members_value"])
            ]
        )
    ]
    assert response.bindings == [compute.Binding(binding_id="binding_id_value")]
    assert response.etag == "etag_value"
    assert response.iam_owned is True
    assert response.rules == [compute.Rule(action=compute.Rule.Action.ALLOW)]
    assert response.version == 774


def test_get_iam_policy_rest_from_dict():
    test_get_iam_policy_rest(request_type=dict)


def test_get_iam_policy_rest_flattened():
    client = SubnetworksClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Policy()

        # Wrap the value into a proper Response obj
        json_return_value = compute.Policy.to_json(return_value)
        response_value = Response()
        response_value.status_code = 200
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_iam_policy(
            project="project_value", region="region_value", resource="resource_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, http_call, http_params = req.mock_calls[0]
        body = http_params.get("data")
        assert "project_value" in http_call[1] + str(body)
        assert "region_value" in http_call[1] + str(body)
        assert "resource_value" in http_call[1] + str(body)


def test_get_iam_policy_rest_flattened_error():
    client = SubnetworksClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_iam_policy(
            compute.GetIamPolicySubnetworkRequest(),
            project="project_value",
            region="region_value",
            resource="resource_value",
        )


def test_insert_rest(
    transport: str = "rest", request_type=compute.InsertSubnetworkRequest
):
    client = SubnetworksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            error=compute.Error(errors=[compute.Errors(code="code_value")]),
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id="id_value",
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id="target_id_value",
            target_link="target_link_value",
            user="user_value",
            warnings=[compute.Warnings(code=compute.Warnings.Code.CLEANUP_FAILED)],
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        json_return_value = compute.Operation.to_json(return_value)
        response_value = Response()
        response_value.status_code = 200
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.insert(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.error == compute.Error(errors=[compute.Errors(code="code_value")])
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == "id_value"
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == "target_id_value"
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.warnings == [
        compute.Warnings(code=compute.Warnings.Code.CLEANUP_FAILED)
    ]
    assert response.zone == "zone_value"


def test_insert_rest_from_dict():
    test_insert_rest(request_type=dict)


def test_insert_rest_flattened():
    client = SubnetworksClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # Wrap the value into a proper Response obj
        json_return_value = compute.Operation.to_json(return_value)
        response_value = Response()
        response_value.status_code = 200
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        subnetwork_resource = compute.Subnetwork(
            creation_timestamp="creation_timestamp_value"
        )
        client.insert(
            project="project_value",
            region="region_value",
            subnetwork_resource=subnetwork_resource,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, http_call, http_params = req.mock_calls[0]
        body = http_params.get("data")
        assert "project_value" in http_call[1] + str(body)
        assert "region_value" in http_call[1] + str(body)
        assert compute.Subnetwork.to_json(
            subnetwork_resource,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        ) in http_call[1] + str(body)


def test_insert_rest_flattened_error():
    client = SubnetworksClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.insert(
            compute.InsertSubnetworkRequest(),
            project="project_value",
            region="region_value",
            subnetwork_resource=compute.Subnetwork(
                creation_timestamp="creation_timestamp_value"
            ),
        )


def test_list_rest(
    transport: str = "rest", request_type=compute.ListSubnetworksRequest
):
    client = SubnetworksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.SubnetworkList(
            id="id_value",
            items=[compute.Subnetwork(creation_timestamp="creation_timestamp_value")],
            kind="kind_value",
            next_page_token="next_page_token_value",
            self_link="self_link_value",
            warning=compute.Warning(code=compute.Warning.Code.CLEANUP_FAILED),
        )

        # Wrap the value into a proper Response obj
        json_return_value = compute.SubnetworkList.to_json(return_value)
        response_value = Response()
        response_value.status_code = 200
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListPager)
    assert response.id == "id_value"
    assert response.items == [
        compute.Subnetwork(creation_timestamp="creation_timestamp_value")
    ]
    assert response.kind == "kind_value"
    assert response.next_page_token == "next_page_token_value"
    assert response.self_link == "self_link_value"
    assert response.warning == compute.Warning(code=compute.Warning.Code.CLEANUP_FAILED)


def test_list_rest_from_dict():
    test_list_rest(request_type=dict)


def test_list_rest_flattened():
    client = SubnetworksClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.SubnetworkList()

        # Wrap the value into a proper Response obj
        json_return_value = compute.SubnetworkList.to_json(return_value)
        response_value = Response()
        response_value.status_code = 200
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list(
            project="project_value", region="region_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, http_call, http_params = req.mock_calls[0]
        body = http_params.get("data")
        assert "project_value" in http_call[1] + str(body)
        assert "region_value" in http_call[1] + str(body)


def test_list_rest_flattened_error():
    client = SubnetworksClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list(
            compute.ListSubnetworksRequest(),
            project="project_value",
            region="region_value",
        )


def test_list_pager():
    client = SubnetworksClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Set the response as a series of pages
        response = (
            compute.SubnetworkList(
                items=[
                    compute.Subnetwork(),
                    compute.Subnetwork(),
                    compute.Subnetwork(),
                ],
                next_page_token="abc",
            ),
            compute.SubnetworkList(items=[], next_page_token="def",),
            compute.SubnetworkList(
                items=[compute.Subnetwork(),], next_page_token="ghi",
            ),
            compute.SubnetworkList(
                items=[compute.Subnetwork(), compute.Subnetwork(),],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(compute.SubnetworkList.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        metadata = ()
        pager = client.list(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, compute.Subnetwork) for i in results)

        pages = list(client.list(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_list_usable_rest(
    transport: str = "rest", request_type=compute.ListUsableSubnetworksRequest
):
    client = SubnetworksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.UsableSubnetworksAggregatedList(
            id="id_value",
            items=[compute.UsableSubnetwork(ip_cidr_range="ip_cidr_range_value")],
            kind="kind_value",
            next_page_token="next_page_token_value",
            self_link="self_link_value",
            warning=compute.Warning(code=compute.Warning.Code.CLEANUP_FAILED),
        )

        # Wrap the value into a proper Response obj
        json_return_value = compute.UsableSubnetworksAggregatedList.to_json(
            return_value
        )
        response_value = Response()
        response_value.status_code = 200
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.list_usable(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListUsablePager)
    assert response.id == "id_value"
    assert response.items == [
        compute.UsableSubnetwork(ip_cidr_range="ip_cidr_range_value")
    ]
    assert response.kind == "kind_value"
    assert response.next_page_token == "next_page_token_value"
    assert response.self_link == "self_link_value"
    assert response.warning == compute.Warning(code=compute.Warning.Code.CLEANUP_FAILED)


def test_list_usable_rest_from_dict():
    test_list_usable_rest(request_type=dict)


def test_list_usable_rest_flattened():
    client = SubnetworksClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.UsableSubnetworksAggregatedList()

        # Wrap the value into a proper Response obj
        json_return_value = compute.UsableSubnetworksAggregatedList.to_json(
            return_value
        )
        response_value = Response()
        response_value.status_code = 200
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_usable(project="project_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, http_call, http_params = req.mock_calls[0]
        body = http_params.get("data")
        assert "project_value" in http_call[1] + str(body)


def test_list_usable_rest_flattened_error():
    client = SubnetworksClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_usable(
            compute.ListUsableSubnetworksRequest(), project="project_value",
        )


def test_list_usable_pager():
    client = SubnetworksClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Set the response as a series of pages
        response = (
            compute.UsableSubnetworksAggregatedList(
                items=[
                    compute.UsableSubnetwork(),
                    compute.UsableSubnetwork(),
                    compute.UsableSubnetwork(),
                ],
                next_page_token="abc",
            ),
            compute.UsableSubnetworksAggregatedList(items=[], next_page_token="def",),
            compute.UsableSubnetworksAggregatedList(
                items=[compute.UsableSubnetwork(),], next_page_token="ghi",
            ),
            compute.UsableSubnetworksAggregatedList(
                items=[compute.UsableSubnetwork(), compute.UsableSubnetwork(),],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(
            compute.UsableSubnetworksAggregatedList.to_json(x) for x in response
        )
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode("UTF-8")
            return_val.status_code = 200
        req.side_effect = return_values

        metadata = ()
        pager = client.list_usable(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, compute.UsableSubnetwork) for i in results)

        pages = list(client.list_usable(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_patch_rest(
    transport: str = "rest", request_type=compute.PatchSubnetworkRequest
):
    client = SubnetworksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            error=compute.Error(errors=[compute.Errors(code="code_value")]),
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id="id_value",
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id="target_id_value",
            target_link="target_link_value",
            user="user_value",
            warnings=[compute.Warnings(code=compute.Warnings.Code.CLEANUP_FAILED)],
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        json_return_value = compute.Operation.to_json(return_value)
        response_value = Response()
        response_value.status_code = 200
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.patch(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.error == compute.Error(errors=[compute.Errors(code="code_value")])
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == "id_value"
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == "target_id_value"
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.warnings == [
        compute.Warnings(code=compute.Warnings.Code.CLEANUP_FAILED)
    ]
    assert response.zone == "zone_value"


def test_patch_rest_from_dict():
    test_patch_rest(request_type=dict)


def test_patch_rest_flattened():
    client = SubnetworksClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # Wrap the value into a proper Response obj
        json_return_value = compute.Operation.to_json(return_value)
        response_value = Response()
        response_value.status_code = 200
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        subnetwork_resource = compute.Subnetwork(
            creation_timestamp="creation_timestamp_value"
        )
        client.patch(
            project="project_value",
            region="region_value",
            subnetwork="subnetwork_value",
            subnetwork_resource=subnetwork_resource,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, http_call, http_params = req.mock_calls[0]
        body = http_params.get("data")
        assert "project_value" in http_call[1] + str(body)
        assert "region_value" in http_call[1] + str(body)
        assert "subnetwork_value" in http_call[1] + str(body)
        assert compute.Subnetwork.to_json(
            subnetwork_resource,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        ) in http_call[1] + str(body)


def test_patch_rest_flattened_error():
    client = SubnetworksClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.patch(
            compute.PatchSubnetworkRequest(),
            project="project_value",
            region="region_value",
            subnetwork="subnetwork_value",
            subnetwork_resource=compute.Subnetwork(
                creation_timestamp="creation_timestamp_value"
            ),
        )


def test_set_iam_policy_rest(
    transport: str = "rest", request_type=compute.SetIamPolicySubnetworkRequest
):
    client = SubnetworksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Policy(
            audit_configs=[
                compute.AuditConfig(
                    audit_log_configs=[
                        compute.AuditLogConfig(
                            exempted_members=["exempted_members_value"]
                        )
                    ]
                )
            ],
            bindings=[compute.Binding(binding_id="binding_id_value")],
            etag="etag_value",
            iam_owned=True,
            rules=[compute.Rule(action=compute.Rule.Action.ALLOW)],
            version=774,
        )

        # Wrap the value into a proper Response obj
        json_return_value = compute.Policy.to_json(return_value)
        response_value = Response()
        response_value.status_code = 200
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.set_iam_policy(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Policy)
    assert response.audit_configs == [
        compute.AuditConfig(
            audit_log_configs=[
                compute.AuditLogConfig(exempted_members=["exempted_members_value"])
            ]
        )
    ]
    assert response.bindings == [compute.Binding(binding_id="binding_id_value")]
    assert response.etag == "etag_value"
    assert response.iam_owned is True
    assert response.rules == [compute.Rule(action=compute.Rule.Action.ALLOW)]
    assert response.version == 774


def test_set_iam_policy_rest_from_dict():
    test_set_iam_policy_rest(request_type=dict)


def test_set_iam_policy_rest_flattened():
    client = SubnetworksClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Policy()

        # Wrap the value into a proper Response obj
        json_return_value = compute.Policy.to_json(return_value)
        response_value = Response()
        response_value.status_code = 200
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        region_set_policy_request_resource = compute.RegionSetPolicyRequest(
            bindings=[compute.Binding(binding_id="binding_id_value")]
        )
        client.set_iam_policy(
            project="project_value",
            region="region_value",
            resource="resource_value",
            region_set_policy_request_resource=region_set_policy_request_resource,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, http_call, http_params = req.mock_calls[0]
        body = http_params.get("data")
        assert "project_value" in http_call[1] + str(body)
        assert "region_value" in http_call[1] + str(body)
        assert "resource_value" in http_call[1] + str(body)
        assert compute.RegionSetPolicyRequest.to_json(
            region_set_policy_request_resource,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        ) in http_call[1] + str(body)


def test_set_iam_policy_rest_flattened_error():
    client = SubnetworksClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.set_iam_policy(
            compute.SetIamPolicySubnetworkRequest(),
            project="project_value",
            region="region_value",
            resource="resource_value",
            region_set_policy_request_resource=compute.RegionSetPolicyRequest(
                bindings=[compute.Binding(binding_id="binding_id_value")]
            ),
        )


def test_set_private_ip_google_access_rest(
    transport: str = "rest",
    request_type=compute.SetPrivateIpGoogleAccessSubnetworkRequest,
):
    client = SubnetworksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation(
            client_operation_id="client_operation_id_value",
            creation_timestamp="creation_timestamp_value",
            description="description_value",
            end_time="end_time_value",
            error=compute.Error(errors=[compute.Errors(code="code_value")]),
            http_error_message="http_error_message_value",
            http_error_status_code=2374,
            id="id_value",
            insert_time="insert_time_value",
            kind="kind_value",
            name="name_value",
            operation_type="operation_type_value",
            progress=885,
            region="region_value",
            self_link="self_link_value",
            start_time="start_time_value",
            status=compute.Operation.Status.DONE,
            status_message="status_message_value",
            target_id="target_id_value",
            target_link="target_link_value",
            user="user_value",
            warnings=[compute.Warnings(code=compute.Warnings.Code.CLEANUP_FAILED)],
            zone="zone_value",
        )

        # Wrap the value into a proper Response obj
        json_return_value = compute.Operation.to_json(return_value)
        response_value = Response()
        response_value.status_code = 200
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.set_private_ip_google_access(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.Operation)
    assert response.client_operation_id == "client_operation_id_value"
    assert response.creation_timestamp == "creation_timestamp_value"
    assert response.description == "description_value"
    assert response.end_time == "end_time_value"
    assert response.error == compute.Error(errors=[compute.Errors(code="code_value")])
    assert response.http_error_message == "http_error_message_value"
    assert response.http_error_status_code == 2374
    assert response.id == "id_value"
    assert response.insert_time == "insert_time_value"
    assert response.kind == "kind_value"
    assert response.name == "name_value"
    assert response.operation_type == "operation_type_value"
    assert response.progress == 885
    assert response.region == "region_value"
    assert response.self_link == "self_link_value"
    assert response.start_time == "start_time_value"
    assert response.status == compute.Operation.Status.DONE
    assert response.status_message == "status_message_value"
    assert response.target_id == "target_id_value"
    assert response.target_link == "target_link_value"
    assert response.user == "user_value"
    assert response.warnings == [
        compute.Warnings(code=compute.Warnings.Code.CLEANUP_FAILED)
    ]
    assert response.zone == "zone_value"


def test_set_private_ip_google_access_rest_from_dict():
    test_set_private_ip_google_access_rest(request_type=dict)


def test_set_private_ip_google_access_rest_flattened():
    client = SubnetworksClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.Operation()

        # Wrap the value into a proper Response obj
        json_return_value = compute.Operation.to_json(return_value)
        response_value = Response()
        response_value.status_code = 200
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        subnetworks_set_private_ip_google_access_request_resource = compute.SubnetworksSetPrivateIpGoogleAccessRequest(
            private_ip_google_access=True
        )
        client.set_private_ip_google_access(
            project="project_value",
            region="region_value",
            subnetwork="subnetwork_value",
            subnetworks_set_private_ip_google_access_request_resource=subnetworks_set_private_ip_google_access_request_resource,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, http_call, http_params = req.mock_calls[0]
        body = http_params.get("data")
        assert "project_value" in http_call[1] + str(body)
        assert "region_value" in http_call[1] + str(body)
        assert "subnetwork_value" in http_call[1] + str(body)
        assert compute.SubnetworksSetPrivateIpGoogleAccessRequest.to_json(
            subnetworks_set_private_ip_google_access_request_resource,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        ) in http_call[1] + str(body)


def test_set_private_ip_google_access_rest_flattened_error():
    client = SubnetworksClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.set_private_ip_google_access(
            compute.SetPrivateIpGoogleAccessSubnetworkRequest(),
            project="project_value",
            region="region_value",
            subnetwork="subnetwork_value",
            subnetworks_set_private_ip_google_access_request_resource=compute.SubnetworksSetPrivateIpGoogleAccessRequest(
                private_ip_google_access=True
            ),
        )


def test_test_iam_permissions_rest(
    transport: str = "rest", request_type=compute.TestIamPermissionsSubnetworkRequest
):
    client = SubnetworksClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.TestPermissionsResponse(
            permissions=["permissions_value"],
        )

        # Wrap the value into a proper Response obj
        json_return_value = compute.TestPermissionsResponse.to_json(return_value)
        response_value = Response()
        response_value.status_code = 200
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value
        response = client.test_iam_permissions(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, compute.TestPermissionsResponse)
    assert response.permissions == ["permissions_value"]


def test_test_iam_permissions_rest_from_dict():
    test_test_iam_permissions_rest(request_type=dict)


def test_test_iam_permissions_rest_flattened():
    client = SubnetworksClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, "request") as req:
        # Designate an appropriate value for the returned response.
        return_value = compute.TestPermissionsResponse()

        # Wrap the value into a proper Response obj
        json_return_value = compute.TestPermissionsResponse.to_json(return_value)
        response_value = Response()
        response_value.status_code = 200
        response_value._content = json_return_value.encode("UTF-8")
        req.return_value = response_value

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        test_permissions_request_resource = compute.TestPermissionsRequest(
            permissions=["permissions_value"]
        )
        client.test_iam_permissions(
            project="project_value",
            region="region_value",
            resource="resource_value",
            test_permissions_request_resource=test_permissions_request_resource,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, http_call, http_params = req.mock_calls[0]
        body = http_params.get("data")
        assert "project_value" in http_call[1] + str(body)
        assert "region_value" in http_call[1] + str(body)
        assert "resource_value" in http_call[1] + str(body)
        assert compute.TestPermissionsRequest.to_json(
            test_permissions_request_resource,
            including_default_value_fields=False,
            use_integers_for_enums=False,
        ) in http_call[1] + str(body)


def test_test_iam_permissions_rest_flattened_error():
    client = SubnetworksClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.test_iam_permissions(
            compute.TestIamPermissionsSubnetworkRequest(),
            project="project_value",
            region="region_value",
            resource="resource_value",
            test_permissions_request_resource=compute.TestPermissionsRequest(
                permissions=["permissions_value"]
            ),
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.SubnetworksRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = SubnetworksClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.SubnetworksRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = SubnetworksClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.SubnetworksRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = SubnetworksClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.SubnetworksRestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = SubnetworksClient(transport=transport)
    assert client.transport is transport


@pytest.mark.parametrize("transport_class", [transports.SubnetworksRestTransport,])
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, "default") as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


def test_subnetworks_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.SubnetworksTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_subnetworks_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.compute_v1.services.subnetworks.transports.SubnetworksTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.SubnetworksTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "aggregated_list",
        "delete",
        "expand_ip_cidr_range",
        "get",
        "get_iam_policy",
        "insert",
        "list",
        "list_usable",
        "patch",
        "set_iam_policy",
        "set_private_ip_google_access",
        "test_iam_permissions",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())


@requires_google_auth_gte_1_25_0
def test_subnetworks_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.compute_v1.services.subnetworks.transports.SubnetworksTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.SubnetworksTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/compute",
                "https://www.googleapis.com/auth/cloud-platform",
            ),
            quota_project_id="octopus",
        )


@requires_google_auth_lt_1_25_0
def test_subnetworks_base_transport_with_credentials_file_old_google_auth():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.compute_v1.services.subnetworks.transports.SubnetworksTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.SubnetworksTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=(
                "https://www.googleapis.com/auth/compute",
                "https://www.googleapis.com/auth/cloud-platform",
            ),
            quota_project_id="octopus",
        )


def test_subnetworks_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.compute_v1.services.subnetworks.transports.SubnetworksTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.SubnetworksTransport()
        adc.assert_called_once()


@requires_google_auth_gte_1_25_0
def test_subnetworks_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        SubnetworksClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/compute",
                "https://www.googleapis.com/auth/cloud-platform",
            ),
            quota_project_id=None,
        )


@requires_google_auth_lt_1_25_0
def test_subnetworks_auth_adc_old_google_auth():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        SubnetworksClient()
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/compute",
                "https://www.googleapis.com/auth/cloud-platform",
            ),
            quota_project_id=None,
        )


def test_subnetworks_http_transport_client_cert_source_for_mtls():
    cred = ga_credentials.AnonymousCredentials()
    with mock.patch(
        "google.auth.transport.requests.AuthorizedSession.configure_mtls_channel"
    ) as mock_configure_mtls_channel:
        transports.SubnetworksRestTransport(
            credentials=cred, client_cert_source_for_mtls=client_cert_source_callback
        )
        mock_configure_mtls_channel.assert_called_once_with(client_cert_source_callback)


def test_subnetworks_host_no_port():
    client = SubnetworksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="compute.googleapis.com"
        ),
    )
    assert client.transport._host == "compute.googleapis.com:443"


def test_subnetworks_host_with_port():
    client = SubnetworksClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="compute.googleapis.com:8000"
        ),
    )
    assert client.transport._host == "compute.googleapis.com:8000"


def test_common_billing_account_path():
    billing_account = "squid"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = SubnetworksClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "clam",
    }
    path = SubnetworksClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = SubnetworksClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "whelk"
    expected = "folders/{folder}".format(folder=folder,)
    actual = SubnetworksClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "octopus",
    }
    path = SubnetworksClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = SubnetworksClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "oyster"
    expected = "organizations/{organization}".format(organization=organization,)
    actual = SubnetworksClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "nudibranch",
    }
    path = SubnetworksClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = SubnetworksClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "cuttlefish"
    expected = "projects/{project}".format(project=project,)
    actual = SubnetworksClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "mussel",
    }
    path = SubnetworksClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = SubnetworksClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "winkle"
    location = "nautilus"
    expected = "projects/{project}/locations/{location}".format(
        project=project, location=location,
    )
    actual = SubnetworksClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "scallop",
        "location": "abalone",
    }
    path = SubnetworksClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = SubnetworksClient.parse_common_location_path(path)
    assert expected == actual


def test_client_withDEFAULT_CLIENT_INFO():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.SubnetworksTransport, "_prep_wrapped_messages"
    ) as prep:
        client = SubnetworksClient(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.SubnetworksTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = SubnetworksClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)
