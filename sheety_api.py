import requests  # Импортируем requests для выполнения HTTP-запросов
from requests.auth import HTTPBasicAuth  # Импортируем HTTPBasicAuth для базовой аутентификации
from auth_data import SHEETY_USRERNAME, SHEETY_PASSWORD  # Импортируем учетные данные для Sheety API

# URL-адрес Sheety API для работы с таблицей цен
SHEETY_PRICES_ENDPOINT = 'https://api.sheety.co/18f6eb88ac98cb50597846c9ab813a11/uchushlar/bahalar'

class GoogleSheetMaglumatymyz:

    def __init__(self):
        self._user = SHEETY_USRERNAME  # Имя пользователя для аутентификации Sheety
        self._password = SHEETY_PASSWORD  # Пароль для аутентификации Sheety
        self._authorization = HTTPBasicAuth(self._user, self._password)  # Настройка базовой аутентификации
        self.barmaly_yer_maglumatlar = {}  # Инициализация пустого словаря для хранения данных о направлениях

    def barmaly_shaher_maglumatlary(self):
        # Используем Sheety API для выполнения GET-запроса и получения всех данных из таблицы.
        response = requests.get(url=SHEETY_PRICES_ENDPOINT)  # Выполняем GET-запрос
        data = response.json()  # Преобразуем ответ в JSON-формат
        self.barmaly_yer_maglumatlar = data["bahalar"]  # Сохраняем данные о направлениях в атрибуте класса
        return self.barmaly_yer_maglumatlar  # Возвращаем данные о направлениях
    
    def iata_codes_tazele(self):
        # Обновляем коды IATA для каждого города в данных
        for shaher in self.barmaly_yer_maglumatlar:
            new_data = {
                "bahalar": {
                    "iataCode": shaher["iataCode"]  # Обновляем код IATA для текущего города
                }
            }
            # Выполняем PUT-запрос для обновления кода IATA в таблице через Sheety API
            response = requests.put(
                url=f"{SHEETY_PRICES_ENDPOINT}/{shaher['id']}",
                json=new_data
            )
            print(response.text)  # Выводим ответ на запрос для проверки результата
