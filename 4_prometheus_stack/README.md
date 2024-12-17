# Gestione Prometheus Stack

Questo esercizio ha l'obiettivo di esplorare la gestione della Prometheus Stack su un cluster Kubernetes. Comprende l'installazione della stack, la comprensione dei suoi componenti principali, l'utilizzo del **BlackBox Exporter** per il monitoraggio di endpoint HTTP e l'analisi delle dashboard integrate.

---

## 1. Installazione della Prometheus Stack

La **Prometheus Stack** è un insieme di strumenti per il monitoraggio delle risorse Kubernetes e non solo. Si utilizza l'Helm chart ufficiale `kube-prometheus-stack`, che include:
- **Prometheus**: per la raccolta e il salvataggio delle metriche.
- **AlertManager**: per la gestione degli allarmi.
- **Grafana**: per la visualizzazione grafica delle metriche.
- **NodeExporter**: per raccogliere metriche delle macchine (CPU, RAM, disco, ecc.).

### Passaggi:

1. Aggiungi il repository Helm ufficiale:
   ```bash
   helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
   helm repo update
   ```

2. Crea un namespace dedicato:
   ```bash
   kubectl create namespace monitoring
   ```

3. Installa la stack:
   ```bash
   helm install prometheus-stack prometheus-community/kube-prometheus-stack --namespace monitoring
   ```

4. Controlla lo stato dei pod:
   ```bash
   kubectl get pods --namespace monitoring
   ```

---

## 2. Comprensione dei componenti della Prometheus Stack

### Componenti principali:

- **Prometheus**:
  - Raccolta delle metriche dai componenti del cluster e da applicazioni esterne.
  - Utilizzo di **scrape jobs** definiti nel file di configurazione.

- **AlertManager**:
  - Gestione e invio di notifiche basate su regole definite.
  - Supporta vari canali di notifica: email, Slack, PagerDuty, ecc.

- **Grafana**:
  - Dashboard preconfigurate per visualizzare metriche raccolte da Prometheus.
  - Supporta query avanzate con PromQL.

- **NodeExporter**:
  - Raccolta delle metriche a livello di nodo, come utilizzo di CPU, RAM, spazio su disco.

### Comandi utili:

- Accedi a Prometheus:
   ```bash
   minikube service prometheus-stack-kube-prom-prometheus --namespace monitoring
   ```

- Accedi a Grafana:
   ```bash
   minikube service prometheus-stack-grafana --namespace monitoring
   ```

Credenziali di default:
- Username: `admin`
- Password: `prom-operator`

---

## 3. Utilizzo del BlackBox Exporter

Il **BlackBox Exporter** consente il monitoraggio di endpoint esterni (HTTP, HTTPS, TCP, ICMP). Simula richieste agli endpoint e registra metriche come:
- Disponibilità (successo o fallimento).
- Tempo di risposta.

### Configurazione del BlackBox Exporter:

1. Crea un file di configurazione `blackbox-config.yaml` con moduli di monitoraggio:
```bash
modules:
  http_2xx:
    prober: http
    timeout: 5s
    http:
      method: GET
      fail_if_ssl: false
      valid_http_versions: ["HTTP/1.1", "HTTP/2"]
```

2. Aggiungi il file come ConfigMap nel cluster:
   ```bash
   kubectl create configmap blackbox-exporter-config --from-file=blackbox-config.yaml --namespace blackbox-exporter
   ```

3. Crea un Deployment per il BlackBox Exporter:
```bash
apiVersion: apps/v1
kind: Deployment
metadata:
  name: blackbox-exporter
  namespace: blackbox-exporter
spec:
  replicas: 1
  selector:
    matchLabels:
      app: blackbox-exporter
  template:
    metadata:
      labels:
        app: blackbox-exporter
    spec:
      containers:
      - name: blackbox-exporter
        image: prom/blackbox-exporter:latest
        ports:
        - containerPort: 9115
        volumeMounts:
        - name: config-volume
          mountPath: /etc/blackbox-exporter
          readOnly: true
        args:
        - "--config.file=/etc/blackbox-exporter/blackbox-config.yaml"
      volumes:
      - name: config-volume
        configMap:
          name: blackbox-exporter-config
```

Applica il Deployment:
   ```bash
   kubectl apply -f blackbox-exporter-deployment.yaml
   ```

4. Configura Prometheus per interrogare il BlackBox Exporter. Aggiorna la configurazione aggiungendo un nuovo **scrape job**:
```bash
scrape_configs:
  - job_name: 'blackbox'
    metrics_path: /probe
    params:
      module: [http_2xx]
    static_configs:
      - targets:
        - http://example.com
        - https://my-website.com
    relabel_configs:
      - source_labels: [__address__]
        target_label: __param_target
      - source_labels: [__param_target]
        target_label: instance
      - target_label: __address__
        replacement: blackbox-exporter.blackbox-exporter.svc.cluster.local:9115
```

Dopo aver aggiornato la configurazione, ricarica Prometheus.

5. Controlla lo stato del monitoraggio:
- Metriche disponibili: `probe_success`, `probe_duration_seconds`.

---

## 4. Comprensione delle dashboard preinstallate

Le dashboard integrate in Grafana forniscono una visualizzazione delle metriche raccolte da Prometheus. Ecco alcune delle più utili:

### Dashboard principali:

1. **Node Exporter Full**:
  - Stato delle risorse di ciascun nodo: CPU, RAM, disco, I/O.

2. **Kubernetes/Compute Resources**:
  - Metriche relative ai pod e ai nodi del cluster.

3. **Kubernetes/Networking Resources**:
  - Stato delle interfacce di rete, traffico e pacchetti persi.

4. **Prometheus**:
  - Stato delle metriche raccolte da Prometheus stesso.

### Accesso:
1. Accedi a Grafana con le credenziali di default.
2. Cerca le dashboard preinstallate nella sezione **Dashboard**.
3. Personalizza le query se necessario.

---

## Conclusione

Questo esercizio consente di:
- Installare e configurare una Prometheus Stack in Kubernetes.
- Comprendere l’integrazione tra i componenti (Prometheus, AlertManager, Grafana, NodeExporter).
- Usare il BlackBox Exporter per monitorare endpoint esterni.
- Esplorare dashboard avanzate per analizzare le metriche raccolte.

Se il tuo ambiente locale è limitato, puoi replicare questi esercizi su un cluster Kubernetes ospitato su cloud per prestazioni migliori.
