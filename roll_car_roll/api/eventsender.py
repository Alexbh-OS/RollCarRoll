
import pika
import json
import os


class EventSender:
    def __init__(self):
        self.host = os.environ.get('RABBITMQ_HOST', 'localhost') # Адрес RabbitMQ
        self.exchange = 'cars_events_exchange'
        self.queue = 'cars_events_queue'

    def send(self, event_type, car_data):
        try:
            # Создаем соединение с сервером RabbitMQ
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
            # Создаем канал в соединении
            channel = connection.channel()

            # Объявляем exchange и очередь
            channel.exchange_declare(exchange=self.exchange, exchange_type='fanout', durable=True) # Создание точки обмена
            channel.queue_declare(queue=self.queue, durable=True) # Создание очереди
            channel.queue_bind(exchange=self.exchange, queue=self.queue) # Связывание точки и очереди

            payload = {
                "eventType": event_type,  # "CREATE", "UPDATE" или "DELETE"
                "car": car_data
            }

            channel.basic_publish(
                exchange=self.exchange, # имя точки обмена, в которую будет опубликовано сообщение
                routing_key='', # ключ маршрутизации, с которым будет опубликовано сообщение
                body=json.dumps(payload) # Тело сообщения
            )
            print(f" [x] Событие {event_type} отправлено в RabbitMQ")
            connection.close()
        except Exception as e:
            print(f" [!] Ошибка отправки в RabbitMQ: {e}")


event_sender = EventSender()