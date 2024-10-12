import requests  # Импортируем requests для выполнения HTTP-запросов
from auth_data import AMADEUS_API_KEY, AMADEUS_SECRET  # Импортируем учетные данные для API Amadeus

# Константы для API Amadeus
IATA_ENDPOINT = "https://test.api.amadeus.com/v1/reference-data/locations/cities"  # URL для поиска городов и аэропортов
FLIGHT_ENDPOINT = "https://test.api.amadeus.com/v2/shopping/flight-offers"  # URL для поиска предложений по рейсам
TOKEN_ENDPOINT = "https://test.api.amadeus.com/v1/security/oauth2/token"  # URL для получения токена доступа

class UchushGozlegi:

    def __init__(self):
        # Инициализация ключей API для аутентификации
        self._api_key = AMADEUS_API_KEY
        self._api_secret = AMADEUS_SECRET
        # Получение нового токена каждый раз при запуске программы.
        # Можно повторно использовать токены, пока они не истекли.
        self._token = self._get_new_token()

    def _get_new_token(self):
        # Заголовок с типом контента, как указано в документации Amadeus
        header = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        body = {
            'grant_type': 'client_credentials',
            'client_id': self._api_key,  # Идентификатор клиента Amadeus
            'client_secret': self._api_secret  # Секретный ключ клиента Amadeus
        }
        # Запрос на получение токена
        response = requests.post(url=TOKEN_ENDPOINT, headers=header, data=body)

        # Выводим новый токен. Обычно истекает через 1799 секунд (30 минут)
        print(f"Sizin token-ynyz {response.json()['access_token']}")
        print(f"Sizin token mohletininiz {response.json()['expires_in']} sekuntdan gutaryar")
        return response.json()['access_token']  # Возвращаем полученный токен

    def get_destination_code(self, city_name):
        # Метод для получения кода IATA города по его названию
        headers = {"Authorization": f"Bearer {self._token}"}  # Заголовок с токеном авторизации
        query = {
            "keyword": city_name,  # Ключевое слово для поиска (название города)
            "max": "2",  # Максимальное количество возвращаемых результатов
            "include": "AIRPORTS",  # Включить в результаты аэропорты
        }
        # Отправка запроса на получение кода IATA для города
        response = requests.get(
            url=IATA_ENDPOINT,
            headers=headers,
            params=query
        )
        print(f"Status code {response.status_code}. Airport IATA: {response.text}")
        try:
            code = response.json()["data"][0]['iataCode']  # Получение кода IATA
        except IndexError:
            print(f"IndexError: Bular yaly airport code tapylmady bu shaherde {city_name}.")
            return "N/A"  # Возвращаем "N/A", если код не найден
        except KeyError:
            print(f"KeyError: Bular yaly airport code tapylmady bu shaherde  {city_name}.")
            return "Not Found"  # Возвращаем "Not Found", если структура ответа некорректна

        return code

    def uchushlary_barla(self, origin_city_code, destination_city_code, from_time, to_time):
        # Метод для проверки рейсов между двумя городами с использованием токена
        headers = {"Authorization": f"Bearer {self._token}"}  # Заголовок с токеном авторизации
        query = {
            "originLocationCode": origin_city_code,  # Код IATA города отправления
            "destinationLocationCode": destination_city_code,  # Код IATA города назначения
            "departureDate": from_time.strftime("%Y-%m-%d"),  # Дата вылета
            "returnDate": to_time.strftime("%Y-%m-%d"),  # Дата возврата
            "adults": 1,  # Количество взрослых пассажиров
            "nonStop": "true",  # Только прямые рейсы
            "currencyCode": "USD",  # Код валюты для отображения цены
            "max": "10",  # Максимальное количество возвращаемых рейсов
        }

        # Запрос на получение предложений по рейсам
        response = requests.get(
            url=FLIGHT_ENDPOINT,
            headers=headers,
            params=query,
        )

        # Проверка кода состояния ответа на запрос
        if response.status_code != 200:
            print(f"uchushlary_barla() jogap code: {response.status_code}")
            print("Gozlegde problema chykdy.\n"
                  "API documentation:\n"
                  "https://developers.amadeus.com/self-service/category/flights/api-doc/flight-offers-search/api"
                  "-reference")
            print("Response body:", response.text)
            return None  # Возвращаем None, если запрос не удался

        return response.json()  # Возвращаем данные JSON с предложениями рейсов