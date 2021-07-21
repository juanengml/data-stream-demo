import streamlit as st 
from requests import get 
import pandas as pd 
from kombu import Connection
from kombu import Exchange
from kombu import Producer
from kombu import Queue
from console_logging.console import Console
console = Console()

console.log("PRODUCER APP....")

rabbit_url =  'amqp://guest:guest@192.168.0.17:5672//'

conn = Connection(rabbit_url)
channel = conn.channel()

_exchange = "data-adress-exchange"
_queue = "data-adress-queue"
_routing_key = "routing-key-adress"

exchange = Exchange(_exchange, type="direct", delivery_mode=1)
producer = Producer(exchange=exchange, channel=channel, routing_key=_routing_key)
queue = Queue(name=_queue, exchange=exchange, routing_key=_routing_key)

queue.maybe_bind(conn)
queue.declare()
	
endpoint = "https://random-data-api.com/api/address/random_address"

data = {"size":100}

def main():
    while True:
           try:
              r = get(endpoint,data,verify=True).json() 
              for i in r:
                #console.info(i)
                print(i['id'])
                producer.publish(i,serializer='pickle', compression='bzip2', routing_key=_routing_key)
           except:
              pass 


if __name__ == "__main__":
    main()

