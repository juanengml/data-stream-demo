import streamlit as st 
from requests import get 
import pandas as pd 
from kombu import Connection
from kombu import Exchange
from kombu import Producer
from kombu import Queue

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
   st.write("""
     # Data Pipeline - Pulicador de Mesanges 
     Demo usando RabbitMQ de Brokcer 
""")
   if st.button('PUBLICANDO 100 de mensagens na fila - FROM API RANDOM DATA API ^_^'):
        st.write('Why hello there')
        for tentativa in range(10000):
           try:
              print("TENTATIVA - " ,tentativa)
              r = get(endpoint,data,verify=True).json() 
              # st.write(len(r))
              for i in r:
                print(i)
                producer.publish(i,serializer='pickle', compression='bzip2', routing_key=_routing_key)
           except:
              pass 


if __name__ == "__main__":
    main()

