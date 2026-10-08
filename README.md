# GLPI Jev Ticket Triage

## Français

Ce service reçoit des webhooks de tickets GLPI et crée un dossier de triage Jev `incident`, `service_request`, `access_request` ou `review`. Il ne change ni ticket, ni équipe, ni SLA. `GET /decisions` fournit la file de décisions pour une revue humaine. SQLite conserve les identifiants et les décisions, pas le titre ni la description. Un changement du ticket crée une nouvelle décision ; les répétitions exactes sont dédupliquées. Les adresses courriel et les formes courantes de secrets sont masquées avant l'appel à Jev, mais ce masquage reste partiel.

Installez avec `python3 -m pip install -r requirements.txt`. Définissez en privé `TYPESAFE_API_KEY` et `JEV_INGEST_TOKEN` (chaîne aléatoire d'au moins 16 caractères), puis lancez `python3 app.py --serve`. Configurez un webhook GLPI sur la création ou la modification d'un ticket, avec un en-tête personnalisé `Authorization: Bearer <jeton>` et un payload JSON de forme `{"event":"ticket.created","ticket":{"id":42,"title":"...","description":"..."}}`. Utilisez `ticket.updated` pour les modifications. Les champs du modèle GLPI doivent être mappés dans son éditeur de payload. Le serveur écoute par défaut sur `127.0.0.1:8097` ; placez-le derrière une entrée HTTPS authentifiée si GLPI est distant.

Démo : `python3 app.py --demo`. Tests : `python3 -m unittest discover -s tests -v`. L'API Jev est testée avec des données synthétiques ; aucune instance GLPI réelle n'a été reliée. Les webhooks et les règles GLPI sont décrits dans la [documentation officielle](https://help.glpi-project.org/documentation/modules/configuration/webhook).

## English

This service receives GLPI ticket webhooks and creates a Jev triage dossier: `incident`, `service_request`, `access_request`, or `review`. It changes no ticket, team, or SLA. `GET /decisions` exposes decisions for human review. SQLite keeps identifiers and decisions, not ticket titles or descriptions. A ticket edit creates a new decision; exact retries are deduplicated. Email addresses and common secret patterns are masked before the Jev call, but masking is best effort.

Install with `python3 -m pip install -r requirements.txt`. Set `TYPESAFE_API_KEY` and a random `JEV_INGEST_TOKEN` of at least 16 characters privately, then run `python3 app.py --serve`. Configure a GLPI webhook for ticket creation or update with the custom header `Authorization: Bearer <token>` and a JSON payload shaped as `{"event":"ticket.created","ticket":{"id":42,"title":"...","description":"..."}}`. Use `ticket.updated` for edits. Map GLPI fields in its payload editor. The server binds to `127.0.0.1:8097` by default; use an authenticated HTTPS ingress when GLPI is remote.

Demo: `python3 app.py --demo`. Tests: `python3 -m unittest discover -s tests -v`. The Jev API was tested with synthetic input; no live GLPI instance was connected. See the [official webhook documentation](https://help.glpi-project.org/documentation/modules/configuration/webhook).

## Español

Este servicio recibe webhooks de tickets GLPI y crea un expediente de triaje Jev: `incident`, `service_request`, `access_request` o `review`. No modifica tickets, equipos ni SLA. `GET /decisions` muestra las decisiones para revisión humana. SQLite guarda identificadores y decisiones, pero no títulos ni descripciones. Una edición del ticket genera otra decisión; los reintentos idénticos se deduplican. Antes de llamar a Jev se ocultan correos y patrones habituales de secretos, aunque el filtrado es parcial.

Instale con `python3 -m pip install -r requirements.txt`. Defina en privado `TYPESAFE_API_KEY` y un `JEV_INGEST_TOKEN` aleatorio de al menos 16 caracteres y ejecute `python3 app.py --serve`. Configure un webhook GLPI para crear o actualizar tickets, con el encabezado personalizado `Authorization: Bearer <token>` y un JSON como `{"event":"ticket.created","ticket":{"id":42,"title":"...","description":"..."}}`. Use `ticket.updated` para cambios. Asocie los campos de GLPI en su editor de payload. El servidor escucha en `127.0.0.1:8097` por defecto; use una entrada HTTPS autenticada si GLPI es remoto.

Demostración: `python3 app.py --demo`. Pruebas: `python3 -m unittest discover -s tests -v`. La API Jev se probó con datos sintéticos; no se conectó una instancia GLPI real. Véase la [documentación oficial de webhooks](https://help.glpi-project.org/documentation/modules/configuration/webhook).

MIT. Tag: `v0.1.0`.
