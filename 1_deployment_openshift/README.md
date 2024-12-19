# Deployment OpenShift

Questo esercizio dimostra come creare e gestire un **Deployment** di Nginx su un cluster Kubernetes locale usando **Minikube**.

---

## Istruzioni

### 1. Creazione del Deployment

Definire un deployment di Nginx con il seguente file YAML:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:latest
        ports:
        - containerPort: 80
```

Salva il file come `nginx-deployment.yaml`.

**Comando:**

```bash
kubectl apply -f nginx-deployment.yaml
```

Verifica il deployment e i pod associati:

```bash
kubectl get deployments
kubectl get pods
```

### 2. Esposizione del Servizio

Esporre il deployment come servizio di tipo **NodePort** per consentire l’accesso all’applicazione:

**Comando:**

```bash
kubectl expose deployment nginx-deployment --type=NodePort --port=80
```

Verifica il servizio creato:
```bash
kubectl get svc
```

### 3. Accesso all’Applicazione

Utilizzare il comando Minikube per aprire il servizio nel browser:

```bash
minikube service nginx-deployment
```

Minikube genererà un URL (ad esempio `http://192.168.x.x:xxxxx`) che punta all’applicazione.

---

## Comandi principali usati

1. **Creare il deployment:**

```bash
kubectl apply -f nginx-deployment.yaml
```

2. **Esporre il servizio:**

```bash
kubectl expose deployment nginx-deployment --type=NodePort --port=80
```

3. **Accedere al servizio:**

```bash
minikube service nginx-deployment
```

---

## Stato finale atteso

### Deployment:

```bash
kubectl get deployments
NAME               READY   UP-TO-DATE   AVAILABLE   AGE
nginx-deployment   2/2     2            2           3m
```

### Pod:

```bash
kubectl get pods
NAME                              READY   STATUS    RESTARTS   AGE
nginx-deployment-xxxxxxx-xxxxx    1/1     Running   0          30s
nginx-deployment-xxxxxxx-xxxxx    1/1     Running   0          30s
```

### Servizio:

```bash
kubectl get svc
NAME               TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
nginx-deployment   NodePort    10.97.140.158   <none>        80:30914/TCP   3m
```

---

## Autore

Questo esercizio è stato svolto come attività didattica per comprendere l’uso di **Deployment**, **Service** e **Minikube** in un cluster Kubernetes locale.
