# Supporto OpenShift Labels (Hard)

In questo esercizio abbiamo creato un ambiente Kubernetes con vari oggetti e configurazioni, tra cui Deployment, Service, ReplicaSet, Ingress e DaemonSet, organizzati tramite l'uso delle labels. L'esercizio è stato svolto in vari passaggi, come descritto qui sotto.

## 1. Creazione di un Deployment

Abbiamo creato un deployment per un'applicazione web in ambiente di sviluppo, localizzata nella regione europea. Il deployment è stato etichettato con le seguenti labels:
- `environment=dev`
- `app=web`
- `region=EU`

Il comando per creare il deployment:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app-dev
spec:
  replicas: 2
  selector:
    matchLabels:
      app: web
      environment: dev
      region: EU
  template:
    metadata:
      labels:
        app: web
        environment: dev
        region: EU
    spec:
      containers:
      - name: web-app
        image: nginx:latest
        ports:
        - containerPort: 80
```

## 2. Creazione di un Servizio

Abbiamo creato un servizio di tipo LoadBalancer per esporre l’applicazione web all’esterno del cluster, selezionando tutti i pod con le labels `app=web` e `environment=dev`.

Il comando per creare il servizio:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: web-app-service
spec:
  selector:
    app: web
    environment: dev
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
  type: ClusterIP
```

## 3. Creazione di un ReplicaSet

Abbiamo creato un ReplicaSet per gestire le repliche del nostro deployment dell’applicazione web. Il ReplicaSet ha le stesse labels del deployment, assicurando che solo i pod con le labels corrette vengano gestiti.

Il comando per creare il ReplicaSet:
```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: web-app-replicaset
spec:
  replicas: 2
  selector:
    matchLabels:
      app: web
      environment: dev
      region: EU
  template:
    metadata:
      labels:
        app: web
        environment: dev
        region: EU
    spec:
      containers:
      - name: web-app
        image: nginx:latest
        ports:
        - containerPort: 80
```

## 4. Creazione di un Ingress

Abbiamo creato un Ingress per esporre l’applicazione web tramite un nome di dominio personalizzato `web-app.dev.local`. L’Ingress instrada il traffico verso il servizio `web-app-service`, selezionato dalle labels.

Il comando per creare l’Ingress:
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: web-app-ingress
spec:
  rules:
  - host: web-app.dev.local
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: web-app-service
            port:
              number: 80
```

## 5. Creazione di un DaemonSet

Abbiamo creato un DaemonSet per eseguire un’applicazione di logging su tutti i nodi del cluster. Questo assicura che ogni nodo esegua un’istanza del logging app, etichettato con `app=logging`.

Il comando per creare il DaemonSet:
```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: logging-app
spec:
  selector:
    matchLabels:
      app: logging
  template:
    metadata:
      labels:
        app: logging
    spec:
      containers:
      - name: logging-app
        image: busybox:latest
```

## 6. Verifica degli Oggetti Kubernetes

Abbiamo verificato che tutti gli oggetti siano stati creati correttamente usando il comando:
   ```bash
   kubectl get deployments,services,replicasets,ingress,daemonsets -o wide
   ```
Abbiamo anche verificato i pod associati all’applicazione web tramite le labels specifiche:
   ```bash
   kubectl get pods -l app=web,environment=dev
   ```

## 7. Accesso all’Applicazione

Dopo aver configurato correttamente l’Ingress e il file `/etc/hosts`, abbiamo potuto accedere all’applicazione web tramite il nome di dominio `web-app.dev.local`.

## Conclusioni

Abbiamo creato con successo vari oggetti Kubernetes come Deployment, Service, ReplicaSet, Ingress e DaemonSet, organizzandoli con le labels per gestirli facilmente in base all’ambiente, tipo di applicazione e regione geografica. L’applicazione web è stata esposta all’esterno tramite un Ingress, con traffico instradato tramite il servizio di tipo LoadBalancer.
