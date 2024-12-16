# Gestione CSR per la richiesta di un nuovo certificato

Questo esercizio dimostra come generare una Root Certificate Authority (CA) e utilizzarla per firmare un certificato SSL per un server. Di seguito sono elencati i passaggi seguiti e i comandi utilizzati.

## Prerequisiti
- OpenSSL installato sul sistema.
- Un terminale o shell per eseguire i comandi.

---

## Passaggi

### 1. Generazione della chiave privata per la Root CA
Per creare una Root CA, è necessario generare una chiave privata. Questa chiave sarà utilizzata per firmare il certificato della Root CA stessa.

```bash
openssl genrsa -out rootCA.key 2048
```

- `genrsa`: Genera una chiave privata RSA.
- `-out rootCA.key`: Specifica il nome del file in cui salvare la chiave privata.
- `2048`: Lunghezza della chiave RSA in bit.

---

### 2. Creazione del certificato Root CA

Con la chiave privata appena generata, creiamo un certificato autofirmato per la Root CA.

```bash
openssl req -x509 -new -nodes -key rootCA.key -sha256 -days 3650 -out rootCA.crt -subj "/C=IT/ST=Italy/L=Rome/O=Sourcesense/CN=RootCA"
```

- `req -x509`: Crea un certificato X.509.
- `-new`: Genera una nuova richiesta di certificato.
- `-nodes`: Evita di crittografare la chiave privata con una password.
- `-key rootCA.key`: Specifica la chiave privata da usare per firmare il certificato.
- `-sha256`: Algoritmo di hash usato per la firma.
- `-days 3650`: Validità del certificato in giorni (10 anni).
- `-out rootCA.crt`: Nome del file per il certificato generato.
- `-subj`: Specifica le informazioni del certificato (Paese, Stato, Località, Organizzazione, Nome Comune).

---

### 3. Controllo del certificato Root CA

È possibile verificare i dettagli del certificato Root CA appena creato.

```bash
openssl x509 -in rootCA.crt -text -noout
```

- `x509`: Permette di gestire i certificati X.509.
- `-in rootCA.crt`: Specifica il file del certificato da analizzare.
- `-text`: Mostra i dettagli del certificato.
- `-noout`: Evita di mostrare l’output binario del certificato.

---

### 4. Generazione della chiave privata per il server

Ora generiamo una chiave privata per il server.

```bash
openssl genrsa -out server.key 2048
```

Il comando è simile a quello usato per la Root CA, ma questa chiave sarà utilizzata per il certificato del server.

---

### 5. Creazione della richiesta di firma del certificato (CSR)

Con la chiave privata del server, generiamo una richiesta di firma del certificato (Certificate Signing Request o CSR). Questa richiesta contiene le informazioni che vogliamo includere nel certificato del server.

```bash
openssl req -new -key server.key -out server.csr -subj "/C=IT/ST=Italy/L=Rome/O=Sourcesense/CN=example.com"
```

- `-new`: Genera una nuova richiesta CSR.
- `-key server.key`: Specifica la chiave privata del server.
- `-out server.csr`: Nome del file per la richiesta CSR.
- `-subj`: Specifica le informazioni del certificato del server (Paese, Stato, Località, Organizzazione, Nome Comune).

---

### 6. Controllo della richiesta CSR

Per verificare i dettagli della richiesta CSR, utilizziamo il comando:

```bash
openssl req -in server.csr -text -noout
```

- `-in server.csr`: Specifica il file CSR da analizzare.
- `-text`: Mostra i dettagli della richiesta.
- `-noout`: Evita di mostrare l’output binario.

---

### 7. Firma del certificato del server con la Root CA

Con la CSR del server e il certificato Root CA, possiamo generare il certificato del server firmato dalla Root CA.

```bash
openssl x509 -req -in server.csr -CA rootCA.crt -CAkey rootCA.key -CAcreateserial -out server.crt -days 365 -sha256
```

- `-req`: Indica che stiamo firmando una richiesta CSR.
- `-in server.csr`: Specifica la richiesta CSR da firmare.
- `-CA rootCA.crt`: Certificato della Root CA utilizzato per firmare.
- `-CAkey rootCA.key`: Chiave privata della Root CA.
- `-CAcreateserial`: Crea un nuovo numero seriale per il certificato.
- `-out server.crt`: Nome del file per il certificato firmato.
- `-days 365`: Validità del certificato in giorni (1 anno).
- `-sha256`: Algoritmo di hash usato per la firma.

---

### 8. Controllo del certificato del server

Infine, verifichiamo i dettagli del certificato del server generato.

```bash
openssl x509 -in server.crt -text -noout
```

---

## File generati

- `rootCA.key`: Chiave privata della Root CA.
- `rootCA.crt`: Certificato della Root CA.
- `server.key`: Chiave privata del server.
- `server.csr`: Richiesta CSR del server.
- `server.crt`: Certificato del server firmato dalla Root CA.

---

## Conclusione

Seguendo questi passaggi, abbiamo creato una Root CA, generato un certificato autofirmato per essa e utilizzato la CA per firmare un certificato per un server. Questo processo è fondamentale per comprendere come funziona l’infrastruttura PKI (Public Key Infrastructure) e come i certificati SSL/TLS vengono utilizzati per garantire la sicurezza delle comunicazioni.

