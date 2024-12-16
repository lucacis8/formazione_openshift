# Gestione Resource Quotas

## Obiettivo dell'esercizio

In questo esercizio, abbiamo configurato una `ResourceQuota` per limitare le risorse a livello di namespace, come CPU, memoria e il numero di risorse come i pod e i servizi. L'obiettivo principale era osservare il comportamento di Kubernetes quando si cerca di superare tali limiti, in particolare il comportamento quando i pod non riescono a essere creati a causa del superamento delle soglie di quota.

## 1. Creazione di una ResourceQuota

La prima parte dell'esercizio consiste nel creare una `ResourceQuota` per il namespace `default`. La `ResourceQuota` impone dei limiti sulle risorse richieste e sui limiti massimi per CPU, memoria, e il numero di oggetti come pod, servizi e replication controllers.

### Manifesto della ResourceQuota

Il manifesto YAML della `ResourceQuota` creato è il seguente:

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: cpu-mem-quota
spec:
  hard:
    limits.cpu: "4"
    limits.memory: "8Gi"
    pods: "10"
    replicationcontrollers: "4"
    requests.cpu: "2"
    requests.memory: "4Gi"
    services: "5"
```

In questo manifesto:
- **limits.cpu**: Limite massimo di CPU per i pod nel namespace (4 CPU).
- **limits.memory**: Limite massimo di memoria per i pod nel namespace (8Gi).
- **pods**: Limite massimo di pod nel namespace (10).
- **replicationcontrollers**: Limite massimo di replication controllers (4).
- **requests.cpu**: Limite minimo di CPU richiesto per i pod (2 CPU).
- **requests.memory**: Limite minimo di memoria richiesta per i pod (4Gi).
- **services**: Limite massimo di servizi nel namespace (5).

Abbiamo applicato questo manifesto con il comando:

```bash
kubectl apply -f resourcequota.yaml
```

### Verifica della ResourceQuota

Dopo aver creato la `ResourceQuota`, abbiamo verificato la sua applicazione con il comando:

```bash
kubectl get resourcequota cpu-mem-quota --namespace=default
```

Il risultato mostrava i limiti imposti e le risorse attualmente utilizzate nel namespace.

## 2. Creazione di un Deployment per superare i limiti

Dopo aver creato la `ResourceQuota`, abbiamo provato a creare un `Deployment` con 11 repliche di un pod, usando l’immagine di `nginx`. Abbiamo usato il comando:

```bash
kubectl create deployment test-pod --image=nginx --replicas=11
```

### Problema del superamento delle soglie

Quando abbiamo cercato di creare il deployment con più di 10 repliche, Kubernetes ha impedito la creazione di nuovi pod a causa del superamento delle risorse disponibili, come definito nella `ResourceQuota`.

### Verifica degli eventi

Abbiamo eseguito il comando:

```bash
kubectl get events --namespace=default
```

Il risultato ha mostrato un errore di tipo `FailedCreate` per i pod, con il seguente messaggio:

```bash
Error creating: pods "test-pod-5d5589b8d9-kp5vq" is forbidden: failed quota: cpu-mem-quota: must specify limits.cpu for: nginx; limits.memory for: nginx; requests.cpu for: nginx; requests.memory for: nginx
```

Questo errore indica che non era possibile creare nuovi pod poiché non erano stati specificati i limiti e le richieste per CPU e memoria nel manifesto del `Deployment`, e la `ResourceQuota` ha impedito la creazione dei nuovi pod per il superamento delle risorse disponibili.

## 3. Risultati osservati

Quando le soglie di quota vengono superate, Kubernetes impedisce la creazione di nuove risorse, come i pod, e genera eventi che notificano l’errore specifico legato al superamento della quota. In questo caso, l’errore è stato causato dal tentativo di creare più pod di quelli consentiti dalla `ResourceQuota` e dall’assenza di specifiche relative a `limits` e `requests` per le risorse nei pod.

### Conclusioni

- La `ResourceQuota` è uno strumento utile per limitare l’utilizzo delle risorse in un namespace Kubernetes, garantendo che nessuna risorsa superi determinati limiti.
- Quando si cerca di superare i limiti definiti nella `ResourceQuota`, Kubernetes impedisce la creazione di nuove risorse, come i pod, e fornisce un messaggio di errore chiaro.
- È importante che i manifesti dei pod o dei deployment includano le specifiche di risorse appropriate (come `requests` e `limits`) per evitare che le operazioni vengano bloccate dalla `ResourceQuota`.
