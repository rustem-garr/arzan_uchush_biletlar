import time  # Импортируем модуль time для работы со временем
from datetime import datetime, timedelta  # Импортируем datetime и timedelta для работы с датами
from sheety_api import GoogleSheetMaglumatymyz  # Импортируем класс GoogleSheetMaglumatymyz из модуля sheety_api
from uchush_gozlegi import UchushGozlegi  # Импортируем класс UchushGozlegi из модуля uchush_gozlegi
from uchush_maglumatlar import arzan_uchushlary_tap  # Импортируем функцию поиска самого дешевого рейса
from whatsappa_habar_beriji import HabarBeriji  # Импортируем класс HabarBeriji для уведомлений

# ==================== Настройка поиска рейсов ====================
google_sheetymyz = GoogleSheetMaglumatymyz()  # Создаем экземпляр GoogleSheetMaglumatymyz для работы с данными
maglumatlar = google_sheetymyz.barmaly_shaher_maglumatlary()  # Получаем данные о направлениях из Google Sheets
uchushGozlegi = UchushGozlegi()  # Создаем экземпляр UchushGozlegi для поиска рейсов
habar_beriji = HabarBeriji()  # Создаем экземпляр HabarBeriji для отправки уведомлений

# Устанавливаем код IATA для аэропорта отправления
NIRDEN_UCHMALY = "ASB"  # Код IATA аэропорта вылета

# ==================== Обновляем коды аэропортов в Google Sheets ====================
for setir in maglumatlar:  # Проходим по всем строкам с данными о направлениях
    if setir["iataCode"] == "":  # Если код IATA отсутствует
        setir["iataCode"] = uchushGozlegi.get_destination_code(setir["barmalyShaheriniz"])  # Получаем код IATA для города назначения
        time.sleep(2)  # Задержка на 2 секунды, чтобы избежать превышения лимита запросов
print(f"Googlesheet maglumatlar:\n {maglumatlar}")  # Выводим обновленные данные на экран

google_sheetymyz.barmaly_yer_maglumatlar = maglumatlar  # Обновляем данные о направлениях в экземпляре google_sheetymyz
google_sheetymyz.iata_codes_tazele()  # Обновляем коды аэропортов в Google Sheets

# ==================== Поиск рейсов и отправка уведомлений ====================
ertir = datetime.now() + timedelta(days=1)  # Определяем дату завтрашнего дня
uch_aylykda = datetime.now() + timedelta(days=(3 * 30))  # Определяем дату через 3 месяцев

for barmaly_yer in maglumatlar:  # Проходим по каждому направлению в данных
    print(f"{barmaly_yer} uchushlary barlayarys")  # Выводим информацию о текущем направлении
    uchushlar = uchushGozlegi.uchushlary_barla(
        NIRDEN_UCHMALY,
        barmaly_yer["iataCode"],
        from_time=ertir,
        to_time=uch_aylykda
    )  # Ищем рейсы из аэропорта отправления в город назначения в указанный период
    arzanBahaUchush = arzan_uchushlary_tap(uchushlar)  # Находим самый дешевый рейс среди найденных
    if arzanBahaUchush.price != "N/A" and arzanBahaUchush.price < barmaly_yer["arzanBaha"]:
        # Если цена рейса доступна и она ниже самой низкой цены в данных
        print(f"Arzan baha bilet tapyldy {barmaly_yer['barmalyShaheriniz']}!")  # Выводим сообщение о нахождении дешевого рейса

        habar_beriji.habar_ber_whatsappda(
            message_body=f"Arzan baha bilet! Bahasy ${arzanBahaUchush.price} "
                         f"{arzanBahaUchush.origin_airport} aeroportdan {arzanBahaUchush.destination_airport} aeroporta, "
                         f"sene {arzanBahaUchush.out_date} chenli {arzanBahaUchush.return_date}."
        )  # Отправка уведомления через WhatsApp с информацией о дешёвом рейсе