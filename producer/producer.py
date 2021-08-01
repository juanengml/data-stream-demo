import schedule ,time
import pandas as pd
from random import choice
from kombu import Connection, Exchange, Producer, Queue
from console_logging.console import Console

console = Console()

## conecta com rabbit 
conn = Connection('amqp://guest:guest@http://ec2-3-139-68-72.us-east-2.compute.amazonaws.com/:5672//')

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

# le nossa dataset 
df = pd.read_csv("https://gist.githubusercontent.com/curran/a08a1080b88344b0c8a7/raw/0e7a9b0a5d22642a06d3d5b9bcbad9890c8ee534/iris.csv")

## função que gera pega os dados das colunas da base iris.csv
def data_iris():
  return  {"sepal_length": choice(df['sepal_length'].tolist()),
          "sepal_width":  choice(df['sepal_width'].tolist()), 
          "petal_length": choice(df['petal_length'].tolist()),
          "petal_width":  choice(df['petal_width'].tolist())
       }

## funcao que pega os dados da funcao e publica no rabbit
def job():
    for p in range(10000000): 
	            data = data_iris()
              producer.publish(data,
                               serializer='pickle', 
                               compression='bzip2',
                               routing_key=_routing_key)
              console.info(data)


## a cada 5 min dispara o job
schedule.every(5).minutes.do(job)

## função main 
def main():
    while True:
        schedule.run_pending()
        time.sleep(1)
        console.info("aguardando...")

if __name__ == "__main__":
    main()

