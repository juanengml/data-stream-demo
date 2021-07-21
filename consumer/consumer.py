
#import dataset 
from pymongo import MongoClient
from kombu import Connection, Exchange, Queue
from kombu.mixins import ConsumerMixin
from datetime import datetime as dt
import json
from console_logging.console import Console
console = Console()

console.log("CONSUMER STARTING....")


rabbit_url = "amqp://guest:guest@192.168.0.17:5672//"

_exchange = "data-adress-exchange"
_queue = "data-adress-queue"
_routing_key = "routing-key-adress"

#endpoint_db  = "mysql://root:asdqwe123@192.168.0.17:49153/clients"

endpoint_db = "mongodb://192.168.0.17:49154/"

#db = dataset.connect(endpoint_db)

client = MongoClient(endpoint_db)

class Worker(ConsumerMixin):
    def __init__(self, connection, queues):
        self.connection = connection
        self.queues = queues

    def get_consumers(self, Consumer, channel):
        return [Consumer(queues=self.queues,
                         callbacks=[self.on_message], accept=['json', 'pickle', 'msgpack', 'yaml'] )]

    def on_message(self, body, message):
        #print(body)
        try:
           db = client['user-address-database']
           posts = db.posts
           console.info(posts.insert_one(body).inserted_id)
           #tabela  = db['user_address']
           #tabela.insert(body)
           console.success("INSERT DATA")
           message.ack()
        except:
           pass

def run():
    print("[*] CONSUMER APP rabbitMQ ")

    exchange = Exchange(_exchange, type="direct")

    queues = [Queue(_queue, exchange, routing_key="video")]

    print("[*] WORKER RUNNING  ")

    with Connection(rabbit_url, heartbeat=40) as conn:
            worker = Worker(conn, queues)
            print("[*] WORKER RUN RABBIT LOADING...")
            worker.run()

if __name__ == "__main__":
    run()