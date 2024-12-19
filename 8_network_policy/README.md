# Verifica e creazione Network Policy (Hard)

Questo progetto dimostra come utilizzare Kubernetes per gestire un'applicazione composta da tre componenti principali: un **frontend**, un **backend** e un **database MySQL**. Include l'implementazione dei manifest YAML, la configurazione di NetworkPolicies e la verifica del funzionamento.

---

## **Struttura del Progetto**

Il progetto è suddiviso nei seguenti componenti principali:

- **Frontend**:
  - Deployment (`frontend-deployment.yaml`)
  - Service (`frontend-service.yaml`)
  - NetworkPolicy (`frontend-networkpolicy.yaml`)
  
- **Backend**:
  - Deployment (`backend-deployment.yaml`)
  - Service (`backend-service.yaml`)
  - NetworkPolicy (`backend-networkpolicy.yaml`)

- **Database (MySQL)**:
  - Deployment (`database-deployment.yaml`)
  - Service (`database-service.yaml`)
  - NetworkPolicy (`database-networkpolicy.yaml`)

---

## **Passaggi Eseguiti**

### **1. Configurazione dei Manifest**

#### **Frontend**
1. Creazione di un deployment per il frontend.
2. Creazione di un service per esporre il frontend.
3. Configurazione di una NetworkPolicy per controllare il traffico in ingresso.

#### **Backend**
1. Creazione di un deployment per il backend.
2. Creazione di un service per esporre il backend.
3. Configurazione di una NetworkPolicy per consentire solo il traffico dal frontend.

#### **Database**
1. Creazione di un deployment per il database MySQL.
2. Creazione di un service per esporre il database al backend.
3. Configurazione di una NetworkPolicy per limitare l'accesso al database al solo backend.

---

### **2. Applicazione dei Manifest**
I seguenti comandi sono stati utilizzati per applicare tutti i manifest YAML:
```bash
kubectl apply -f frontend-deployment.yaml
kubectl apply -f frontend-service.yaml
kubectl apply -f backend-deployment.yaml
kubectl apply -f backend-service.yaml
kubectl apply -f database-deployment.yaml
kubectl apply -f database-service.yaml
kubectl apply -f frontend-networkpolicy.yaml
kubectl apply -f backend-networkpolicy.yaml
kubectl apply -f database-networkpolicy.yaml
```

---

### 3. Verifica dello Stato dei Componenti

#### Controllo delle NetworkPolicies

Comando:
   ```bash
   kubectl get networkpolicies
   ```

Output:
   ```bash
   NAME              POD-SELECTOR   AGE
   frontend-policy   app=frontend   14s
   backend-policy    app=backend    14s
   database-policy   app=database   14s
   ```

#### Controllo dei Pod

Comando:
   ```bash
   kubectl get pods
   ```

Output:
```bash
NAME                           READY   STATUS      RESTARTS   AGE
frontend-xxxxxxxxx-xxxxx       1/1     Running     0          100s
frontend-xxxxxxxxx-xxxxx       1/1     Running     0          100s
backend-xxxxxxxxxx-xxxxx       1/1     Running     0          99s
backend-xxxxxxxxxx-xxxxx       1/1     Running     0          99s
database-xxxxxxxxxx-xxxxx      1/1     Running     0          99s
```

---

### 4. Test di Comunicazione

#### Test del Frontend verso il Backend

Comando:
   ```bash
   kubectl exec -it <frontend-pod> -- curl backend:5000
   ```

Output:
```bash
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>Directory listing for /</title>
</head>
<body>
<h1>Directory listing for /</h1>
<hr>
<ul>
<li><a href=".dockerenv">.dockerenv</a></li>
<li><a href="bin/">bin@</a></li>
<li><a href="boot/">boot/</a></li>
<li><a href="dev/">dev/</a></li>
<li><a href="etc/">etc/</a></li>
<li><a href="home/">home/</a></li>
<li><a href="lib/">lib@</a></li>
<li><a href="lib64/">lib64@</a></li>
<li><a href="media/">media/</a></li>
<li><a href="mnt/">mnt/</a></li>
<li><a href="opt/">opt/</a></li>
<li><a href="proc/">proc/</a></li>
<li><a href="root/">root/</a></li>
<li><a href="run/">run/</a></li>
<li><a href="sbin/">sbin@</a></li>
<li><a href="srv/">srv/</a></li>
<li><a href="sys/">sys/</a></li>
<li><a href="tmp/">tmp/</a></li>
<li><a href="usr/">usr/</a></li>
<li><a href="var/">var/</a></li>
</ul>
<hr>
</body>
</html>
```

#### Test del Backend verso il Database

Comando:
   ```bash
   kubectl exec -it <backend-pod> -- mysql -h database -u root -proot
   ```

Output:
```bash
mysql: [Warning] Using a password on the command line interface can be insecure.
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 10
Server version: 8.0.33 MySQL Community Server - GPL

Copyright (c) 2000, 2023, Oracle and/or its affiliates. All rights reserved.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql>
```

---

## Note Importanti

1. **Immagini Docker**: Assicurarsi che le immagini del backend e del frontend siano configurate correttamente per la connessione.
2. **NetworkPolicies**: Limitano il traffico tra i pod, migliorando la sicurezza.
3. **Testing**: I test sono stati eseguiti con successo tra i vari componenti.

---

## Comandi Utili

- Verifica dei servizi:
   ```bash
   kubectl get svc
   ```

- Accesso a un pod:
   ```bash
   kubectl exec -it <pod-name> -- /bin/bash
   ```

- Logs di un pod:
   ```bash
   kubectl logs <pod-name>
   ```

---

## Autore

Progetto realizzato da Luca Cisotto per dimostrare l’uso di Kubernetes con un’applicazione multi-componente.
