import logging as logger


class ApiAssertions:

    def __init__(self, response):
        self.response = response
        self.json_data = response.json()

    def assert_status_code_is(self, status_code):
        assert self.response.status_code == int(status_code), \
            f'User was not created. Current status code is {self.response.status_code}, but {status_code} expected'
        logger.info('Status code is correct')

    def assert_attributes_in_response(self, *attribute_names):
        for i in attribute_names:
            assert self.json_data[i], f'There is no parameter named "{i}" in response'
        logger.info(f'{attribute_names[0]} exist in response')

    def assert_attribute_equal(self, attribute_name, value):
        assert self.json_data[attribute_name] == value, f'Attribute named {attribute_name} not equal {value}. ' \
                                                        f'Current value is {self.json_data[attribute_name]}'
        logger.info(f'{attribute_name} is as expected')

    def assert_value_type_is(self, *attributes, value_type):
        for i in attributes:
            self.assert_attributes_in_response(i)
            assert isinstance(i, value_type), f'Type of "{i}" is {type(i)}'
        logger.info(f'value type of {attributes[0]} is correct')

