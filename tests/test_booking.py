import allure
import pytest
import requests

# Тесты на создание бронирования

@allure.feature('Booking')
@allure.story('Create booking')
def test_create_booking(api_client, generate_random_booking_data):
    booking = api_client.create_booking(generate_random_booking_data)

    assert booking["bookingid"] > 0


# При прямом requests.post() на POST /booking получаю 200.
# Через мой APIClient.create_booking() получаю 418.
# Перед этим fixture вызывает client.auth(), после чего я добавляю Bearer token в session.headers.



# Проверка полноты json
# статус код 200, после создания бронирования

# мокирование с помощью мокера