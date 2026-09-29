import allure
import pytest
import requests
from core.clients.endpoints import Endpoints


# Проверка создания бронирования и тела ответа
@allure.feature('Booking')
@allure.story('Create booking')
def test_create_booking(api_client, generate_random_booking_data):
    booking = api_client.create_booking(generate_random_booking_data)
    assert booking["bookingid"] > 0
    assert booking["booking"]["firstname"] == generate_random_booking_data["firstname"]
    assert booking["booking"]["lastname"] == generate_random_booking_data["lastname"]
    assert booking["booking"]["totalprice"] == generate_random_booking_data["totalprice"]
    assert booking["booking"]["depositpaid"] == generate_random_booking_data["depositpaid"]
    assert booking["booking"]["bookingdates"] == generate_random_booking_data["bookingdates"]
    assert booking["booking"]["additionalneeds"] == generate_random_booking_data["additionalneeds"]


# Отправка пустого тела запроса
@allure.feature('Booking')
@allure.story('Create booking with empty body')
def test_create_booking_empty_body(api_client):
    booking_data = {}
    with pytest.raises(requests.HTTPError):
        api_client.create_booking(booking_data)


# Отправка запроса без обязательного поля "firstname"
@allure.feature('Booking')
@allure.story('Create booking without firstname')
def test_create_booking_without_firstname(api_client, generate_random_booking_data):
    booking_data = generate_random_booking_data.copy()
    booking_data.pop("firstname")
    with pytest.raises(requests.HTTPError):
        api_client.create_booking(booking_data)


# Проверка обработки неправильного status code
@allure.feature('Booking')
@allure.story('Unexpected status code')
def test_create_booking_unexpected_status_code(api_client, generate_random_booking_data, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 201
    mocker.patch.object(api_client.session, 'post', return_value=mock_response)
    with pytest.raises(Exception, match="Expected status code 200 but got 201"):
        api_client.create_booking(generate_random_booking_data)