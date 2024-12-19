from kafka import KafkaProducer
import time

producer = KafkaProducer(bootstrap_servers='localhost:9092')

# Invio di messaggi al topic 'foobar'
for i in range(10):
    message = f'Message {i}'
    producer.send('foobar', value=message.encode('utf-8'))
    print(f'Produced: {message}')
    time.sleep(1)

producer.flush()
producer.close()
