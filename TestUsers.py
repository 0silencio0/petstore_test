import json
from endpoints import USER
from assertions import ApiAssertions
import pytest
import requests
import random
import string
import logging as logger


class TestUser:
    URL = r'https://petstore.swagger.io/v2'
    USERNAME = f'username_{random.randint(0, 100)}'
    EMAIL = f'username{random.randint(0, 100)}@email.com'
    PHONE = f'+7{"".join(random.choices(string.digits, k=10))}'
    PASSWORD = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=12))
    DEFAULT_HEADERS = {'Content-Type': 'application/json'}

    @classmethod
    def new_username(cls):
        cls.USERNAME = f'username_{random.randint(0, 100)}'
        return cls.USERNAME

    @classmethod
    def new_email(cls):
        cls.EMAIL = f'username{random.randint(0, 100)}@email.com'
        return cls.EMAIL

    @classmethod
    def new_phone(cls):
        cls.PHONE = f'+7{random.choices(string.digits, k=10)}'
        return cls.PHONE

    def request_url(self, endpoint):
        return f'{self.URL}{endpoint}'

    @pytest.fixture
    def user_setup(self):
        data = {
            "username": self.USERNAME,
            "firstName": self.USERNAME,
            "lastName": self.USERNAME,
            "email": self.EMAIL,
            "password": self.PASSWORD,
            "phone": self.PHONE,
            "userStatus": 1
        }
        create_url = self.request_url(USER['create'])
        resp = requests.post(url=create_url, data=json.dumps(data), headers=self.DEFAULT_HEADERS)
        delete_url = self.request_url(USER['delete'].replace('{username}', self.USERNAME))
        yield resp
        requests.delete(url=delete_url, headers=self.DEFAULT_HEADERS)

    @pytest.mark.create_user
    def test_create_user(self):
        data = {
            "username": self.USERNAME,
            "firstName": self.USERNAME,
            "lastName": self.USERNAME,
            "email": self.EMAIL,
            "password": self.PASSWORD,
            "phone": self.PHONE,
            "userStatus": 1
        }
        request_url = self.request_url(USER['create'])
        resp = requests.post(url=request_url, data=json.dumps(data), headers=self.DEFAULT_HEADERS)

        assertion = ApiAssertions(resp)

        assertion.assert_status_code_is(200)
        assertion.assert_attributes_in_response('code', 'type', 'message')

    @pytest.mark.get_user
    @pytest.mark.parametrize('attribute,value', [('username', USERNAME),
                                                 ('firstName', USERNAME),
                                                 ('lastName', USERNAME),
                                                 ('email', EMAIL),
                                                 ('password', PASSWORD),
                                                 ('phone', PHONE)])
    def test_get_user(self, user_setup, attribute, value):
        request_url = self.request_url(USER['get_by_username']).replace('{username}', self.USERNAME)
        resp = requests.get(url=request_url, headers=self.DEFAULT_HEADERS)
        assertion = ApiAssertions(resp)
        assertion.assert_status_code_is(200)
        assertion.assert_value_type_is(attribute, value_type=str)
        assertion.assert_attribute_equal(attribute, value)

    @pytest.mark.login
    def test_login(self, user_setup):
        request_url = self.request_url(USER['login'])
        params = {
            'username': self.USERNAME,
            'password': self.PASSWORD
        }
        resp = requests.get(url=request_url, headers=self.DEFAULT_HEADERS, params=params)
        assertion = ApiAssertions(resp)
        assertion.assert_status_code_is(200)
        assertion.assert_attributes_in_response('code', 'type', 'message')

    @pytest.mark.logout
    def test_logout(self, user_setup):
        request_url = self.request_url(USER['logout'])
        resp = requests.get(url=request_url, headers=self.DEFAULT_HEADERS)
        assertion = ApiAssertions(resp)
        assertion.assert_status_code_is(200)
        assertion.assert_attributes_in_response('code', 'type', 'message')

    @pytest.mark.update_user_data
    def test_logout(self, user_setup):
        request_url = self.request_url(USER['update']).replace('{username}', self.USERNAME)
        data = {
            "username": self.new_username(),
            "email": self.new_email(),
            "phone": self.new_phone(),
            "userStatus": 1
        }
        resp = requests.put(url=request_url, headers=self.DEFAULT_HEADERS, data=data)
        assertion = ApiAssertions(resp)
        assertion.assert_status_code_is(200)
        assertion.assert_attribute_equal('username', self.USERNAME)
        assertion.assert_attribute_equal('email', self.EMAIL)
        assertion.assert_attribute_equal('phone', self.PHONE)
