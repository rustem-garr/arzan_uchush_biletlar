class UhushMaglumatlar:
    # Класс для хранения информации о рейсах

    def __init__(self, price, origin_airport, destination_airport, out_date, return_date):
        # Инициализация атрибутов класса
        self.price = price  # Сохраняем стоимость рейса
        self.origin_airport = origin_airport  # Сохраняем код IATA аэропорта отправления
        self.destination_airport = destination_airport  # Сохраняем код IATA аэропорта назначения
        self.out_date = out_date  # Сохраняем дату вылета
        self.return_date = return_date  # Сохраняем дату обратного рейса

def arzan_uchushlary_tap(data):
    # Функция для поиска самых дешевых рейсов
    if data is None or not data['data']:
        print("Bu tarapa uchush maglumat tapylmady")  # Сообщение о том, что данных о рейсах нет
        return UhushMaglumatlar("N/A", "N/A", "N/A", "N/A", "N/A")  # Возвращаем объект с "N/A"

    # Данные о первом рейсе в json
    first_flight = data['data'][0]  # Получаем данные о первом рейсе
    lowest_price = float(first_flight["price"]["grandTotal"])  # Извлекаем общую стоимость рейса
    origin = first_flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]  # Код IATA аэропорта отправления
    destination = first_flight["itineraries"][0]["segments"][0]["arrival"]["iataCode"]  # Код IATA аэропорта назначения
    out_date = first_flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]  # Дата вылета
    return_date = first_flight["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]  # Дата возврата

    # Инициализация объекта UhushMaglumatlar для сравнения с первым рейсом
    cheapest_flight = UhushMaglumatlar(lowest_price, origin, destination, out_date, return_date)

    for flight in data["data"]:  # Проходим по всем рейсам в данных
        price = float(flight["price"]["grandTotal"])  # Получаем цену текущего рейса
        if price < lowest_price:  # Если текущая цена меньше, чем самая низкая найденная
            lowest_price = price  # Обновляем значение самой низкой цены
            origin = flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]  # Обновляем аэропорт отправления
            destination = flight["itineraries"][0]["segments"][0]["arrival"]["iataCode"]  # Обновляем аэропорт назначения
            out_date = flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]  # Обновляем дату вылета
            return_date = flight["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]  # Обновляем дату возврата
            cheapest_flight = UhushMaglumatlar(lowest_price, origin, destination, out_date, return_date)  # Обновляем данные о самом дешевом рейсе
            print(f"Lowest price to {destination} is £{lowest_price}")  # Выводим сообщение о самой низкой цене

    return cheapest_flight  # Возвращаем данные о самом дешевом рейсе