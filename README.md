# Formazione Sourcesense - DevOps Academy - Track 4  

Questo repository contiene una raccolta di esercizi pratici progettati per approfondire le competenze nella gestione di Kubernetes e OpenShift.  
Ogni esercizio è pensato per affrontare specifici scenari reali, coprendo tematiche come il deploy di applicazioni, la gestione dei certificati, le quote di risorse, il monitoring, Kafka, le network policy e molto altro.

## Struttura della Repository  

La repository è suddivisa in directory corrispondenti agli esercizi proposti.  
Ogni directory include:  
- Un file `README.md` con la descrizione dettagliata dell'esercizio.  
- I file di configurazione YAML o script necessari per completare l'attività.  

---

## 1. Deployment OpenShift  

### Descrizione  
L'obiettivo di questo esercizio è comprendere come vengono definiti i Deployment e i DeploymentConfig all'interno di OpenShift e Kubernetes.  
Attraverso manifest YAML, verrà configurato un deployment per installare **Nginx** o un'applicazione con footprint minimale, verificandone il funzionamento nel cluster.  

---

## 2. Gestione CSR per Richieste di Certificati  

### Descrizione  
In questo esercizio, imparerai a gestire certificati utilizzando una **Certificate Authority (CA)** locale.  
Le attività includono:  
1. Creazione di una **ROOT CA** self-signed.  
2. Generazione di una **Certificate Signing Request (CSR)**.  
3. Emissione di certificati firmati dalla ROOT CA, utilizzabili per autenticazioni o connessioni sicure.  

---

## 3. Gestione Resource Quotas  

### Descrizione  
L'esercizio ti guiderà nella configurazione e nell'uso delle **ResourceQuotas** in Kubernetes.  
Le **ResourceQuotas** permettono di limitare l'utilizzo delle risorse (CPU, memoria, storage) per uno specifico namespace.  
L'attività include:  
- Configurazione di quote per un namespace.  
- Verifica del comportamento del cluster al superamento delle soglie definite.  

---

## 4. Gestione Prometheus Stack  

### Descrizione  
Questo esercizio introduce l'installazione e la configurazione dello stack **Prometheus** per il monitoring del cluster.  
Le attività includono:  
1. Installazione dello stack tramite Helm Chart ufficiali.  
2. Studio dei componenti principali:  
   - **Prometheus**: per la raccolta dei dati.  
   - **AlertManager**: per la gestione degli alert.  
   - **Grafana**: per la visualizzazione dei dati.  
   - **NodeExporter**: per monitorare i nodi del cluster.  
3. Configurazione e test del **BlackBox Exporter** per monitorare endpoint HTTP.  
4. Analisi delle dashboard predefinite di Grafana per ottenere insight dettagliati sul cluster.  

---

## 5. Gestione Secret  

### Descrizione  
In questo esercizio, scoprirai come creare e gestire **Secret** in Kubernetes.  
I Secret sono risorse utilizzate per archiviare informazioni sensibili come password, token o chiavi SSH.  
Le attività includono:  
1. Creazione di diversi tipi di Secret, tra cui:  
   - Secret generici.  
   - Secret di tipo **docker-registry**.  
   - Secret per certificati.  
2. Accesso e lettura dei Secret da un pod per verificare la corretta configurazione.  

---

## 6. Supporto Kafka  

### Descrizione  
Questo esercizio si concentra sull'utilizzo di **Apache Kafka** per la gestione di messaggi distribuiti.  
L'attività prevede lo sviluppo di due applicazioni Python:  
- **Producer**: un'applicazione che crea un topic denominato "foobar" e produce messaggi al suo interno.  
- **Consumer**: un'applicazione che legge i messaggi prodotti nel topic.  
Infine, verrà misurato il **lag** tra i messaggi prodotti e quelli consumati utilizzando strumenti di monitoring per Kafka.  

---

## 7. Supporto OpenShift Labels  

### Descrizione  
L'esercizio ti insegna come organizzare i deployment nel cluster utilizzando le **labels**.  
Le labels sono chiavi-valore assegnate agli oggetti di Kubernetes per classificarli e filtrarli facilmente.  
Le attività includono:  
1. Creazione di un deployment per un'applicazione web in ambiente **dev**, situata nella regione europea.  
   - Labels utilizzate: `environment=dev`, `app=web`, `region=EU`.  
2. Configurazione di un servizio **LoadBalancer** per esporre l'applicazione all'esterno.  
3. Creazione di un **ReplicaSet** per gestire le repliche dell'applicazione web.  
4. Configurazione di un **Ingress** per esporre l'applicazione tramite un dominio personalizzato.  
5. Creazione di un **DaemonSet** per eseguire un'applicazione di logging su tutti i nodi del cluster.  

---

## 8. Verifica e Creazione Network Policy  

### Descrizione  
In questo esercizio, configurerai le **Network Policy** per garantire la sicurezza delle comunicazioni tra le applicazioni nel cluster.  
Le applicazioni includono:  
- **Frontend**: un'applicazione che espone un servizio web.  
- **Backend**: un servizio che elabora richieste dal frontend.  
- **Database**: per la gestione dei dati.  

Le attività includono:  
1. Configurazione delle **labels**:  
   - Frontend: `app=frontend`.  
   - Backend: `app=backend`.  
   - Database: `app=database`.  
2. Creazione delle Network Policy:  
   - Consentire al **frontend** di comunicare solo con il **backend**.  
   - Consentire al **backend** di comunicare solo con il **database**.  
   - Negare tutto il traffico non autorizzato verso il **database**.  
3. Verifica delle policy configurate utilizzando strumenti come `kubectl exec` e comandi di rete per testare la connettività.  

---

## Esecuzione degli Esercizi  

1. Clona il repository sul tuo ambiente locale:  
   ```bash
   git clone https://github.com/lucacis8/formazione_openshift
   cd formazione_openshift
   ```

2. Segui le istruzioni nei file `README.md` all’interno di ciascuna directory per completare gli esercizi.

3. Applica i manifest YAML con:
   ```bash
   kubectl apply -f <file.yaml>
   ```
