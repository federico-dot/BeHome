🏠 BeHome – Odoo Product Import Automation

📌 Overview

BeHome è uno script Python progettato per automatizzare l’importazione massiva di prodotti in Odoo, partendo da un file CSV.

Il sistema gestisce automaticamente:
	•	creazione prodotti
	•	generazione varianti
	•	gestione attributi
	•	collegamento fornitori

👉 Riduce drasticamente il lavoro manuale e gli errori di inserimento.

⸻

⚙️ Tech Stack
	•	Python 3
	•	XML-RPC API di Odoo
	•	CSV processing

⸻

🚀 Features

🔐 Connessione a Odoo
	•	Autenticazione via XML-RPC
	•	Accesso ai modelli Odoo
	•	Operazioni CRUD remote

⸻

📄 Import da CSV
	•	Lettura file CSV strutturato
	•	Normalizzazione dati
	•	Raggruppamento prodotti per:
	•	default_code
	•	name

⸻

📦 Creazione Product Template
	•	Controllo duplicati
	•	Creazione automatica prodotti
	•	Mapping completo dei campi:
	•	prezzo vendita
	•	costo
	•	categoria
	•	unità di misura
	•	descrizioni

⸻

🧩 Gestione Varianti
	•	Creazione dinamica di:
	•	attributi (es. colore, materiale)
	•	valori (rosso, blu, ecc.)
	•	Generazione combinazioni automatiche

⸻

🔢 Codici prodotto automatici

Ogni variante ha un codice univoco:
BASECODE-VALORE1-VALORE2

Esempio:
SEDIA-Rosso-Legno
SEDIA-Blu-Plastica

⸻

🏭 Gestione Fornitori
	•	Creazione automatica supplier
	•	Collegamento al prodotto
	•	Evita duplicazioni

⸻

⚠️ Controlli intelligenti
	•	Skip prodotti già esistenti
	•	Riutilizzo template esistenti
	•	Aggiornamento varianti

⸻

📂 Project Structure
behome-odoo-import/
│
├── main.py        # Script principale
├── config.py      # Configurazione (NON versionare)
├── utils.py       # Funzioni helper
├── data/          # CSV input
└── README.md

📈 Output generato
	•	Product Template creati
	•	Varianti generate automaticamente
	•	Attributi collegati
	•	Fornitori associati

⸻

🧠 Concetti chiave
	•	Data normalization
	•	Deduplication logic
	•	Dynamic variant generation
	•	ERP automation

⸻

🔧 Possibili miglioramenti
	•	Logging strutturato
	•	Gestione errori avanzata
	•	Interfaccia web per upload CSV
	•	Dockerizzazione
	•	API REST wrapper

⸻

👨‍💻 Autore

Federico Cresci
