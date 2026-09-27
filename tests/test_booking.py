import allure
import pytest
import requests

# Тесты на создание бронирования

@allure.feature('Booking')
@allure.story('Create booking')
def test_create_booking(api_client, generate_random_booking_data):
    booking = api_client.create_booking(generate_random_booking_data)
    assert booking["bookingid"] > 0


@allure.feature('Booking')
@allure.story('Server unavailable')
def test_create_booking_server_unavailable(api_client, generate_random_booking_data, mocker):
    mocker.patch.object(api_client.session, 'post', side_effect=Exception("Server unavailable"))
    with pytest.raises(Exception, match="Server unavailable"):
        api_client.create_booking(generate_random_booking_data)


@allure.feature('Booking')
@allure.story('Incorrect Status-code')
def test_create_booking_incorrect_status_code(api_client, generate_random_booking_data, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 201
    mocker.patch.object(api_client.session, 'post', return_value=mock_response)
    with pytest.raises(Exception, match="Expected status code 200 but got 201"):
        api_client.create_booking(generate_random_booking_data)