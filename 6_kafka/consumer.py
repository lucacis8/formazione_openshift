from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'foobar',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    group_id='my-group'
)

# Lettura dei messaggi dal topic
for message in consumer:
    print(f'Consumed: {message.value.decode("utf-8")}')
