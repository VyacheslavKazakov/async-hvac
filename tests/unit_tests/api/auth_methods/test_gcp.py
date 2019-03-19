import logging
from asynctest import TestCase

from parameterized import parameterized

from async_hvac.adapters import Request
from async_hvac.api.auth_methods import Gcp
from tests import utils
from tests.unit_tests import requests_mock


class TestGcp(TestCase):
    TEST_MOUNT_POINT = 'gcp-test'

    @parameterized.expand([
        ('success', dict(), None,),
    ])
    @requests_mock.Mocker()
    async def test_login(self, label, test_params, raises, requests_mocker):
        role_name = 'hvac'
        credentials = utils.load_config_file('example.jwt.json')
        test_policies = [
            "default",
            "dev",
            "prod",
        ]
        expected_status_code = 200
        mock_url = 'http://127.0.0.1:8200/v1/auth/{mount_point}/login'.format(
            mount_point=self.TEST_MOUNT_POINT,
        )
        mock_response = {
            "auth": {
                "client_token": "f33f8c72-924e-11f8-cb43-ac59d697597c",
                "accessor": "0e9e354a-520f-df04-6867-ee81cae3d42d",
                "policies": test_policies,
                "lease_duration": 2764800,
                "renewable": True,
            },
        }
        requests_mocker.register_uri(
            method='POST',
            url=mock_url,
            status_code=expected_status_code,
            json=mock_response,
        )
        async with Request() as adapter:
            gcp = Gcp(adapter=adapter)
            if raises is not None:
                with self.assertRaises(raises):
                    await gcp.login(
                        role=role_name,
                        jwt=credentials,
                        mount_point=self.TEST_MOUNT_POINT,
                        **test_params
                    )
            else:
                login_response = await gcp.login(
                    role=role_name,
                    jwt=credentials,
                    mount_point=self.TEST_MOUNT_POINT,
                    **test_params
                )
                logging.debug('login_response: %s' % login_response)
                self.assertEqual(
                    first=login_response['auth']['policies'],
                    second=test_policies,
                )