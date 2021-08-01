import streamlit as st 
from requests import get 
import pandas as pd
from random import choice
from kombu import Connection, Exchange, Producer, Queue
from console_logging.console import Console

console = Console()

console.log("PRODUCER APP....")

conn = Connection('amqp://guest:guest@192.168.0.17:5672//')
channel = conn.channel()

_routing_key = "routing-key-adress"

exchange = Exchange("data-adress-exchange", type="direct", delivery_mode=1)
producer = Producer(exchange=exchange, channel=channel, routing_key=_routing_key)
queue = Queue(name="data-adress-queue", exchange=exchange, routing_key=_routing_key)

queue.maybe_bind(conn)
queue.declare()
	
df = pd.read_csv("https://gist.githubusercontent.com/curran/a08a1080b88344b0c8a7/raw/0e7a9b0a5d22642a06d3d5b9bcbad9890c8ee534/iris.csv")

def data_iris():
    
  data = {"sepal_length": choice(df['sepal_length'].tolist()),
          "sepal_width":  choice(df['sepal_width'].tolist()), 
          "petal_length": choice(df['petal_length'].tolist()),
          "petal_width":  choice(df['petal_width'].tolist())
       }
  return data


def main():
    while True:
	  for p in range(10000000): 
	      data = data_iris()
              producer.publish(data,serializer='pickle', compression='bzip2', routing_key=_routing_key)
              console.info(data)
	  console.log("DELAY...")
	  sleep(5*60)	# delay de 5 mins 

if __name__ == "__main__":
    main()

