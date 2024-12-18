# Esercizio: Supporto Kafka

Questo esercizio guida nella configurazione di un sistema Kafka locale utilizzando Docker, lo sviluppo di due applicazioni Python (producer e consumer), e il monitoraggio del lag tra i messaggi prodotti e consumati.

## **Obiettivi**

1. Studiare Kafka e la sua architettura (producer, consumer, broker, zookeeper, topic, partition, offset).
2. Creare due applicazioni Python:
   - **Producer**: invia messaggi a un topic Kafka.
   - **Consumer**: legge i messaggi dal topic Kafka.
3. Monitorare il lag tra i messaggi prodotti e consumati utilizzando strumenti di monitoring o i comandi nativi di Kafka.

---

## **Prerequisiti**

1. Docker e Docker Compose installati.
2. Python 3.x installato e configurato.
3. Pacchetto `kafka-python` installato:
   ```bash
   pip install kafka-python
   ```

---

## Configurazione

### 1. Configurazione di Kafka con Docker Compose

Crea un file `docker-compose.yml` con il seguente contenuto per avviare Kafka e Zookeeper:
```bash
version: '3.8'

services:
  zookeeper:
    image: confluentinc/cp-zookeeper:latest
    container_name: zookeeper
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
    ports:
      - "2181:2181"

  kafka:
    image: confluentinc/cp-kafka:latest
    container_name: kafka
    depends_on:
      - zookeeper
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
      KAFKA_LISTENERS: PLAINTEXT://0.0.0.0:9092
    ports:
      - "9092:9092"
```

Avvia i container:
   ```bash
   docker-compose up -d
   ```

---

### 2. Creazione dello script Python del Producer

Crea un file `producer.py`:
```bash
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
```

---

### 3. Creazione dello script Python del Consumer

Crea un file `consumer.py`:
```bash
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
```

---

## Esecuzione

### 1. Verifica dell’ambiente Kafka

Controlla i container in esecuzione:
   ```bash
   docker ps
   ```

Crea il topic foobar (se non è stato già creato):
   ```bash
   docker exec -it kafka kafka-topics.sh --create --topic foobar --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
   ```

---

### 2. Avvio delle applicazioni

1. **Avvia lo script del Producer**:
   ```bash
   python3 producer.py
   ```

Questo script invierà 10 messaggi al topic `foobar`.

2. **Avvia lo script del Consumer** (in un altro terminale):
   ```bash
   python3 consumer.py
   ```

Questo script leggerà i messaggi dal topic `foobar`.

---

### 3. Monitoraggio del Lag

Puoi monitorare il lag dei consumer utilizzando i comandi nativi di Kafka:
   ```bash
   docker exec -it kafka kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group my-group --describe
   ```

Oppure utilizza strumenti di monitoring come **Burrow** o exporter di Prometheus configurati con Kafka.

---

## Strumenti Utilizzati

1. **Kafka**: per gestire il flusso di messaggi.
2. **Python**: per sviluppare le applicazioni Producer e Consumer.
3. **Kafka-CLI**: per gestire topic e monitorare i gruppi consumer.

---

## Risultati Attesi

1. Il producer invia i messaggi al topic `foobar` e il consumer li legge in tempo reale.
2. Puoi monitorare il lag tra i messaggi prodotti e consumati utilizzando i comandi di Kafka o strumenti di monitoring esterni.

---

## Conclusioni

Questo esercizio dimostra il flusso base di Kafka (producer, consumer e topic) e introduce i concetti di offset e lag monitoring, fondamentali per gestire sistemi distribuiti affidabili.
