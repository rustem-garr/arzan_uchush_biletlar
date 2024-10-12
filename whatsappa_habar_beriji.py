from twilio.rest import Client  # Импортируем клиент Twilio для отправки сообщений
from auth_data import TWILIO_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_NUMBER, TWILIO_VERIFIED_NUMBER  # Импортируем учетные данные для Twilio

class HabarBeriji:
    # Класс для отправки сообщений через WhatsApp с помощью Twilio

    def __init__(self):
        # Инициализация клиента Twilio с учетными данными
        self.client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    def habar_ber_whatsappda(self, message_body):
        # Метод для отправки сообщения через WhatsApp
        self.client.messages.create(
            from_=f'whatsapp:{TWILIO_WHATSAPP_NUMBER}',  # Номер отправителя в формате WhatsApp
            body=message_body,  # Текст сообщения
            to=f'whatsapp:{TWILIO_VERIFIED_NUMBER}'  # Номер получателя в формате WhatsApp
        )
        print('Sizin whatsapp-nyza, arzan bahada tapan biletyn maglumatlaryny ugratdym!')  # Сообщение об успешной отправке