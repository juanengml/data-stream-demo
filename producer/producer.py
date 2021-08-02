import schedule ,time
import pandas as pd
from random import choice
from kombu import Connection, Exchange, Producer, Queue
from console_logging.console import Console
from requests import get 

console = Console()

## conecta com rabbit 
conn = Connection('amqp://guest:guest@ec2-3-139-68-72.us-east-2.compute.amazonaws.com:5672//')

# define nosso canal
channel = conn.channel()

_routing_key = "routing-key-adress"

# define nossa exchange e producer e fila 
exchange = Exchange("data-adress-exchange", type="direct", delivery_mode=1)
producer = Producer(exchange=exchange, channel=channel, routing_key=_routing_key)
queue = Queue(name="data-adress-queue", exchange=exchange, routing_key=_routing_key)

# declara nossa fila na conexão
queue.maybe_bind(conn)
queue.declare()

# le nosso endpoint 
endpoint = "https://random-data-api.com/api/users/random_user"
data = {"size":100}

## função que gera pega os dados das colunas da base  
def data_iris():
  return get(endpoint,data).json()
## funcao que pega os dados da funcao e publica no rabbit
def job():
  for p in range(1000): 
         data = data_iris()
         producer.publish(data,serializer='pickle',compression='bzip2',routing_key=_routing_key)
         console.info(data)


## a cada 5 min dispara o job
schedule.every(1).minutes.do(job)

## função main 
def main():
    while True:
        schedule.run_pending()
        time.sleep(1)
        console.info("aguardando...")

if __name__ == "__main__":
    main()

