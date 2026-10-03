import allure
import pytest
import requests
from core.clients.endpoints import Endpoints
from pydantic import ValidationError
from core.models.booking import BookingResponse


@allure.feature('Test creating Booking')
@allure.story('Positive: creating booking with custom data')
def test_create_booking_with_custom_data(api_client):
    booking_data = {
        "firstname" : "Ivan",
        "lastname": "Ivanovich",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2025-02-01",
            "checkout": "2025-02-10"
        },
        "additionalneeds": "Dinner"
    }
    response = api_client.create_booking(booking_data)
    try:
        BookingResponse(**response)
    except ValidationError as e:
        raise ValidationError(f"Response validation failed: {e}")

    assert response["booking"]["firstname"] == booking_data["firstname"]
    assert response["booking"]["lastname"] == booking_data["lastname"]
    assert response["booking"]["totalprice"] == booking_data["totalprice"]
    assert response["booking"]["depositpaid"] == booking_data["depositpaid"]
    assert response["booking"]["bookingdates"]["checkin"] == booking_data["bookingdates"]["checkin"]
    assert response["booking"]["bookingdates"]["checkout"] == booking_data["bookingdates"]["checkout"]
    assert response["booking"]["additionalneeds"] == booking_data["additionalneeds"]


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


# Создание двух бронирований подряд и проверка, что у них разные ID
@allure.feature('Booking')
@allure.story('Create multiple bookings')
def test_create_multiple_bookings(api_client, generate_random_booking_data):
    booking_data_1 = generate_random_booking_data
    booking_data_2 = generate_random_booking_data.copy()

    booking_data_2["firstname"] = "Alex"
    booking_data_2["lastname"] = "Smith"

    booking_1 = api_client.create_booking(booking_data_1)

    assert booking_1["bookingid"] > 0
    assert booking_1["booking"]["firstname"] == booking_data_1["firstname"]
    assert booking_1["booking"]["lastname"] == booking_data_1["lastname"]
    assert booking_1["booking"]["totalprice"] == booking_data_1["totalprice"]
    assert booking_1["booking"]["depositpaid"] == booking_data_1["depositpaid"]
    assert booking_1["booking"]["bookingdates"] == booking_data_1["bookingdates"]
    assert booking_1["booking"]["additionalneeds"] == booking_data_1["additionalneeds"]

    booking_2 = api_client.create_booking(booking_data_2)
    assert booking_2["bookingid"] > 0
    assert booking_2["booking"]["firstname"] == booking_data_2["firstname"]
    assert booking_2["booking"]["lastname"] == booking_data_2["lastname"]
    assert booking_2["booking"]["totalprice"] == booking_data_2["totalprice"]
    assert booking_2["booking"]["depositpaid"] == booking_data_2["depositpaid"]
    assert booking_2["booking"]["bookingdates"] == booking_data_2["bookingdates"]
    assert booking_2["booking"]["additionalneeds"] == booking_data_2["additionalneeds"]

    assert booking_1["bookingid"] != booking_2["bookingid"]


#Проверка создания бронирования при отсутствии необязательного поля additionalneeds
@allure.feature('Booking')
@allure.story('Create booking without additionalneeds')
def test_create_booking_without_additionalneeds(api_client, generate_random_booking_data):
    booking_data = generate_random_booking_data.copy()
    booking_data.pop("additionalneeds")
    booking_1 = api_client.create_booking(booking_data)
    assert booking_1["bookingid"] > 0
    assert booking_1["booking"]["firstname"] == booking_data["firstname"]
    assert booking_1["booking"]["lastname"] == booking_data["lastname"]
    assert booking_1["booking"]["totalprice"] == booking_data["totalprice"]
    assert booking_1["booking"]["depositpaid"] == booking_data["depositpaid"]
    assert booking_1["booking"]["bookingdates"] == booking_data["bookingdates"]


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


# Отправка запроса с некорректным типом данных для поля "totalprice" (string)
# Restful Booker принимает string и преобразует значение в integer. Проверка, что пришел именно int при отправке str
@allure.feature('Booking')
@allure.story('Create booking with incorrect totalprice')
def test_create_booking_with_incorrect_totalprice(api_client,generate_random_booking_data):
    booking_data = generate_random_booking_data.copy()
    booking_data["totalprice"] = "500"
    booking = api_client.create_booking(booking_data)
    assert booking["bookingid"] > 0
    assert booking["booking"]["totalprice"] == 500
    assert isinstance(booking["booking"]["totalprice"], int)


# Проверка обработки неправильного status code
@allure.feature('Booking')
@allure.story('Unexpected status code')
def test_create_booking_unexpected_status_code(api_client, generate_random_booking_data, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 201
    mocker.patch.object(api_client.session, 'post', return_value=mock_response)
    with pytest.raises(Exception, match="Expected status code 200 but got 201"):
        api_client.create_booking(generate_random_booking_data)