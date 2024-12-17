# **Esercizio: Gestione dei Secret in Kubernetes**

Questo esercizio illustra come creare e gestire diversi tipi di Secret in Kubernetes e come utilizzarli all'interno di un cluster.

---

## **Obiettivi**
1. Creare vari tipi di Secret supportati da Kubernetes.
2. Utilizzare i Secret nei Pod come variabili d'ambiente o come volume montato.
3. Leggere e decodificare i Secret tramite comandi diretti.

---

## **1. Creazione di Secret**

### **a. Secret Generico (Key-Value)**
Un Secret generico memorizza coppie chiave-valore.

1. Creazione del Secret tramite `kubectl`:
   ```bash
   kubectl create secret generic my-generic-secret \
     --from-literal=username=my-user \
     --from-literal=password=my-password
   ```

2. Verifica del Secret:
   ```bash
   kubectl get secret my-generic-secret -o yaml
   ```

---

### **b. Secret da File**

Puoi creare un Secret a partire da file contenenti valori sensibili.

1. Crea due file:

- `username.txt`:
   ```bash
   my-user
   ```

- `password.txt`:
   ```bash
   my-password
   ```

2. Creazione del Secret:
   ```bash
   kubectl create secret generic my-file-secret \
     --from-file=username=username.txt \
     --from-file=password=password.txt
   ```

3. Verifica del Secret:
   ```bash
   kubectl describe secret my-file-secret
   ```

---

### **c. Secret per Docker Registry**

Questo tipo di Secret memorizza credenziali per l’accesso a un Docker Registry privato.

1. Creazione del Secret:
   ```bash
   kubectl create secret docker-registry my-docker-secret \
     --docker-server=https://index.docker.io/v1/ \
     --docker-username=my-docker-username \
     --docker-password=my-docker-password \
     --docker-email=my-email@example.com
   ```

2. Verifica del Secret:
   ```bash
   kubectl get secret my-docker-secret -o yaml
   ```

---

### **d. Secret TLS**

Un Secret TLS viene utilizzato per memorizzare certificati e chiavi private.

1. Creazione di un certificato e una chiave privata:
   ```bash
   openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
     -keyout tls.key -out tls.crt \
     -subj "/CN=my-example.com"
   ```

2. Creazione del Secret:
   ```bash
   kubectl create secret tls my-tls-secret \
     --key tls.key --cert tls.crt
   ```

3. Verifica del Secret:
   ```bash
   kubectl describe secret my-tls-secret
   ```

---

### **e. Secret Bootstrap Token**

Questo tipo di Secret viene utilizzato per autenticare i nodi al cluster.

1. Creazione del Secret con token bootstrap:
```bash
apiVersion: v1
kind: Secret
metadata:
  name: bootstrap-token-secret
  namespace: kube-system
type: bootstrap.kubernetes.io/token
data:
  token-id: YmFzaWMtZXhhbXBsZQ==    # Base64 di "basic-example"
  token-secret: ZW5jb2RlLXRva2Vu    # Base64 di "encode-token"
```

2. Applicazione del Secret:
   ```bash
   kubectl apply -f bootstrap-token-secret.yaml
   ```

---

## **2. Utilizzo dei Secret nei Pod**

### **a. Montare un Secret come Volume**

Un Secret può essere montato come file all’interno di un container.

1. File `pod-with-secret-volume.yaml`:
```bash
apiVersion: v1
kind: Pod
metadata:
  name: secret-volume-pod
spec:
  containers:
  - name: app
    image: busybox
    command: ["sleep", "3600"]
    volumeMounts:
    - name: secret-volume
      mountPath: "/etc/secret"
      readOnly: true
  volumes:
  - name: secret-volume
    secret:
      secretName: my-generic-secret
```

2. Creazione del Pod:
   ```bash
   kubectl apply -f pod-with-secret-volume.yaml
   ```

3. Lettura dei valori montati:
   ```bash
   kubectl exec -it secret-volume-pod -- cat /etc/secret/username
   kubectl exec -it secret-volume-pod -- cat /etc/secret/password
   ```

---

### **b. Esporre un Secret come Variabile d’Ambiente**

Un Secret può essere utilizzato per impostare variabili d’ambiente.

1. File `pod-with-secret-env.yaml`:
```bash
apiVersion: v1
kind: Pod
metadata:
  name: secret-env-pod
spec:
  containers:
  - name: app
    image: busybox
    command: ["sh", "-c", "echo $SECRET_USERNAME && echo $SECRET_PASSWORD && sleep 3600"]
    env:
    - name: SECRET_USERNAME
      valueFrom:
        secretKeyRef:
          name: my-generic-secret
          key: username
    - name: SECRET_PASSWORD
      valueFrom:
        secretKeyRef:
          name: my-generic-secret
          key: password
```

2. Creazione del Pod:
   ```bash
   kubectl apply -f pod-with-secret-env.yaml
   ```

3. Verifica dei log del Pod:
   ```bash
   kubectl logs secret-env-pod
   ```

---

### **c. Lettura Diretta di un Secret**

Puoi leggere direttamente i Secret utilizzando comandi `kubectl`.

1. Visualizza i dati dei Secret in Base64:
   ```bash
   kubectl get secret my-generic-secret -o yaml
   ```

2. Decodifica i valori con base64:
   ```bash
   kubectl get secret my-generic-secret -o jsonpath='{.data.username}' | base64 --decode
   kubectl get secret my-generic-secret -o jsonpath='{.data.password}' | base64 --decode
   ```

---

## Conclusione

In questo esercizio abbiamo:
1. Creato diversi tipi di Secret, tra cui generici, da file, Docker Registry e TLS.
2. Utilizzato i Secret in Pod come volumi o variabili d’ambiente.
3. Esplorato e letto i Secret tramite comandi diretti.

Queste competenze ti permettono di gestire informazioni sensibili in modo sicuro all’interno di un cluster Kubernetes.
