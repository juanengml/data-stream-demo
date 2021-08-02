
#import dataset 
from pymongo import MongoClient
from kombu import Connection, Exchange, Queue
from kombu.mixins import ConsumerMixin
from datetime import datetime as dt
import json
from console_logging.console import Console

console = Console()
console.log("CONSUMER STARTING....")
rabbit_url = "amqp://guest:guest@ec2-3-139-68-72.us-east-2.compute.amazonaws.com:5672//"
endpoint_db = "mongodb://ec2-3-139-68-72.us-east-2.compute.amazonaws.com:49153/"

client = MongoClient(endpoint_db)
db = client['users_database']
tabela = db['users_tabela']

class Worker(ConsumerMixin):
    def __init__(self, connection, queues):
        self.connection = connection
        self.queues = queues

    def get_consumers(self, Consumer, channel):
        return [Consumer(queues=self.queues,
                         callbacks=[self.on_message], accept=['json', 'pickle', 'msgpack', 'yaml'] )]

    def on_message(self, body, message):
           console.log(body)
           console.info(tabela.insert_one(body).inserted_id)
           message.ack()

def run():
    console.log("[*] CONSUMER APP rabbitMQ ")
    exchange = Exchange("data-adress-exchange", type="direct")
    queues = [Queue("data-adress-queue", exchange,routing_key="routing-key-adress")]
    console.log("[*] WORKER RUNNING  ")
    with Connection(rabbit_url, heartbeat=40) as conn:
            worker = Worker(conn, queues)
            print("[*] WORKER RUN RABBIT LOADING...")
            worker.run()

if __name__ == "__main__":
    run()
