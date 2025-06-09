# Hello World Integration

Una semplice integrazione custom per Home Assistant che aggiunge un sensore "Hello World".

## Installazione

### HACS (Raccomandata)

1. Aggiungi questo repository come repository custom in HACS
2. Installa l'integrazione "Hello World"
3. Riavvia Home Assistant

### Installazione Manuale

1. Copia la cartella `hello_world` nella cartella `custom_components` della tua configurazione Home Assistant
2. Riavvia Home Assistant

## Configurazione

1. Vai in **Impostazioni** > **Dispositivi e servizi**
2. Clicca su **+ Aggiungi integrazione**
3. Cerca "Hello World"
4. Segui la procedura guidata di configurazione

## Utilizzo

Dopo l'installazione, l'integrazione creerà un sensore che mostra "Hello, World! 👋" come stato e include attributi aggiuntivi con informazioni sull'integrazione.

Il sensore apparirà nella tua dashboard Home Assistant e potrà essere utilizzato in automazioni, script e template.

## Funzionalità

- ✅ Sensore semplice con messaggio "Hello World"
- ✅ Attributi aggiuntivi informativi
- ✅ Configurazione tramite interfaccia utente
- ✅ Icona personalizzata
- ✅ Supporto per rimozione integrazione
- ✅ **Notifiche automatiche aggiornamenti** - Home Assistant ti avviserà quando ci sono nuove versioni disponibili

## Setup Notifiche Aggiornamenti

Per ricevere notifiche automatiche degli aggiornamenti in Home Assistant:

1. **Modifica il repository GitHub** nel file `update.py`:
   ```python
   GITHUB_REPO = "tuousername/hello_world_integration"  # Cambia con il tuo repo
   ```

2. **Crea releases su GitHub** quando aggiorni l'integrazione:
   - Vai su GitHub → Releases → Create a new release
   - Tag version: `v1.0.2` (incrementa la versione)
   - Release title: `Version 1.0.2`
   - Descrivi le modifiche nelle note di rilascio

3. **Home Assistant mostrerà automaticamente** la notifica di aggiornamento disponibile!

## Sviluppo

Questa integrazione è un esempio base per iniziare a sviluppare integrazioni custom per Home Assistant.

## Licenza

MIT License
