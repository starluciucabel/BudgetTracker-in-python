# BudgetTracker - Gestione Spese Personali

**Progetto Scolastico**
**Scuola:** Istituto Tecnico Superiore "ITS ICT"
**Anno scolastico:** 2025/2026
**Materia:** Informatica
**Docente:** Prof. Papa Massimo
**Studente:** Cattano Lorenzo

---

## Descrizione

BudgetTracker è un'applicazione desktop sviluppata in Python per la gestione delle finanze personali. L'applicazione permette di:

- Registrare entrate e uscite con categorizzazione
- Visualizzare il saldo mensile in tempo reale
- Analizzare le spese per categoria tramite grafici
- Consultare lo storico delle transazioni
- Creare backup del database
- Esportare grafici in formato PNG/PDF

## Scopo del Progetto

In un contesto in cui la gestione finanziaria personale è spesso trascurata, BudgetTracker si propone come strumento pratico e funzionale per:

- Tenere traccia delle spese quotidiane
- Monitorare le entrate mensili
- Pianificare il risparmio
- Visualizzare l'andamento economico nel tempo
- Prevenire la disorganizzazione finanziaria

## Tecnologie Utilizzate

- **Linguaggio:** Python 3.x
- **Interfaccia Grafica:** tkinter
- **Database:** SQLite3
- **Grafici:** matplotlib
- **Gestione Date:** datetime

## Struttura del Progetto

Il progetto è organizzato in moduli separati seguendo i principi della programmazione ad oggetti:

```
BudgetTracker/
│
├── main.py              # File principale per avviare l'applicazione
├── database.py          # Modulo gestione database SQLite
├── logica.py           # Modulo logica di business e validazione
├── gui.py              # Modulo interfaccia grafica (tkinter)
├── grafici.py          # Modulo generazione grafici (matplotlib)
├── requirements.txt    # Dipendenze Python
├── README.md           # Documentazione
└── budgettracker.db   # Database SQLite (generato automaticamente)
```

### Moduli

#### 1. **database.py** - Gestione Database
Gestisce tutte le operazioni sul database SQLite:
- Creazione e inizializzazione tabelle
- Inserimento, modifica ed eliminazione transazioni
- Query per recupero dati e statistiche
- Funzionalità di backup

**Classi principali:**
- `Database`: Gestione completa del database

#### 2. **logica.py** - Logica di Business
Contiene la logica applicativa, validazione e calcoli:
- Validazione degli input utente
- Formattazione dati (valute, date, percentuali)
- Calcoli statistici avanzati
- Classi modello per transazioni e bilancio

**Classi principali:**
- `Transazione`: Rappresenta una singola transazione
- `Bilancio`: Gestione del bilancio con calcoli
- `Validatore`: Validazione completa degli input
- `Formattatore`: Formattazione dati per visualizzazione
- `CalcolatoreStatistiche`: Calcoli statistici avanzati

#### 3. **grafici.py** - Generazione Grafici
Gestisce la creazione di visualizzazioni grafiche:
- Grafici a torta per distribuzione spese
- Grafici a barre per confronti
- Grafici di andamento temporale
- Esportazione grafici in vari formati

**Classi principali:**
- `GeneratoreGrafici`: Creazione di tutti i tipi di grafici

#### 4. **gui.py** - Interfaccia Grafica
Implementa l'interfaccia utente completa:
- Layout responsive con tkinter
- Form per inserimento transazioni
- Visualizzazione lista transazioni
- Riepilogo finanziario
- Tab per grafici e statistiche

**Classi principali:**
- `InterfacciaGrafica`: Gestione completa dell'interfaccia

## Installazione

### Requisiti
- Python 3.8 o superiore
- pip (gestore pacchetti Python)

### Procedura

1. **Clona o scarica il progetto**
   ```bash
   cd BudgetTracker
   ```

2. **Installa le dipendenze**
   ```bash
   pip install -r requirements.txt
   ```

3. **Avvia l'applicazione**
   ```bash
   python main.py
   ```

## Utilizzo

### Inserimento Transazione

1. Seleziona il tipo (Entrata/Uscita)
2. Inserisci l'importo in euro
3. Seleziona la categoria dal menu a tendina
4. Inserisci la data (formato YYYY-MM-DD o DD/MM/YYYY)
5. Aggiungi una descrizione opzionale
6. Clicca su "Aggiungi Transazione"

### Visualizzazione Dati

- **Riepilogo:** Visualizza entrate, uscite e saldo del mese selezionato
- **Transazioni:** Lista completa di tutte le transazioni con filtri per categoria
- **Grafici:** Tre tipi di visualizzazione (torta, barre, confronto)

### Funzionalità Aggiuntive

- **Backup:** Menu File → Backup Database
- **Elimina:** Seleziona una transazione e clicca "Elimina Selezionata"
- **Salva Grafico:** Esporta il grafico corrente in PNG o PDF
- **Filtri:** Filtra transazioni per mese e categoria

## Categorie Predefinite

### Uscite
- Alimentari
- Trasporti
- Svago
- Bollette
- Salute
- Abbigliamento
- Istruzione
- Casa
- Altro

### Entrate
- Stipendio
- Bonus
- Investimenti
- Altro

## Caratteristiche Tecniche

### Validazione Input
- Controllo formato importi (supporta virgola e punto)
- Validazione date con formati multipli
- Verifica categorie valide
- Limite lunghezza descrizioni
- Gestione errori con messaggi informativi

### Sicurezza Dati
- Database SQLite con vincoli di integrità
- Check constraints sui campi
- Transazioni atomiche
- Backup manuale del database

### Interfaccia
- Design responsive e intuitivo
- Tema personalizzato con colori coerenti
- Supporto per finestre ridimensionabili
- Feedback visivo per azioni utente

## Programmazione ad Oggetti

Il progetto implementa i principi OOP:

- **Incapsulamento:** Dati e metodi organizzati in classi
- **Separazione responsabilità:** Ogni modulo ha un compito specifico
- **Riusabilità:** Classi utilizzabili in contesti diversi
- **Manutenibilità:** Codice organizzato e documentato

## Architettura MVC

Il progetto segue parzialmente il pattern Model-View-Controller:

- **Model (Modello):** `database.py`, `logica.py` - Gestione dati e logica
- **View (Vista):** `gui.py` - Interfaccia utente
- **Controller:** Integrato in `gui.py` - Coordinamento tra model e view

## Possibili Estensioni Future

- Supporto multi-utente con login
- Grafici di andamento temporale avanzati
- Budget mensile per categoria con alert
- Esportazione dati in CSV/Excel
- Sincronizzazione cloud
- App mobile companion
- Importazione estratti conto bancari
- Notifiche per scadenze pagamenti
- Report PDF automatici mensili
- Categorizzazione automatica con ML

## Screenshot

*(Nota: Aggiungere screenshot dell'applicazione in uso)*

## Problemi Noti

- Su alcune installazioni Python potrebbe essere necessario installare tkinter separatamente
- I grafici potrebbero richiedere qualche secondo per generarsi con molti dati

## Risoluzione Problemi

### tkinter non trovato
Su Ubuntu/Debian:
```bash
sudo apt-get install python3-tk
```

Su Fedora:
```bash
sudo dnf install python3-tkinter
```

### matplotlib non si installa
Prova con:
```bash
pip install --upgrade pip
pip install matplotlib
```

## Licenza

Progetto scolastico - Uso educativo

## Contatti

**Studente:** Cattano Lorenzo
**Scuola:** ITS ICT
**Docente:** Prof. Papa Massimo
**Anno:** 2025/2026

---

## Note per il Docente

### Obiettivi Didattici Raggiunti

1. **Programmazione ad Oggetti**
   - Utilizzo di classi e oggetti
   - Incapsulamento e separazione responsabilità
   - Ereditarietà (potenziale per estensioni)

2. **Gestione Database**
   - Progettazione schema relazionale
   - Query SQL complesse
   - Transazioni e integrità dati

3. **Interfaccia Grafica**
   - Layout responsive con tkinter
   - Gestione eventi
   - Integrazione widget complessi

4. **Visualizzazione Dati**
   - Grafici con matplotlib
   - Integrazione grafici in GUI
   - Esportazione immagini

5. **Best Practices**
   - Codice documentato
   - Gestione errori
   - Validazione input
   - Struttura modulare

### Competenze Acquisite

- Python avanzato
- Database relazionali (SQLite)
- GUI design e sviluppo
- Data visualization
- Software architecture
- Version control (potenziale con Git)
- Documentation

---

**Data Creazione:** Gennaio 2025
**Versione:** 1.0
