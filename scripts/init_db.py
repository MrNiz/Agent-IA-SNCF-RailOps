# scripts/init_db.py

import sqlite3
import os

DB_PATH = "data/railops.db"
os.makedirs("data", exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS incidents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ligne TEXT,
    type_incident TEXT,
    niveau INTEGER,
    statut TEXT,
    date_heure TEXT,
    duree_minutes INTEGER,
    commentaire TEXT
)
""")

cur.executemany("""
INSERT INTO incidents (ligne, type_incident, niveau, statut, date_heure, duree_minutes, commentaire)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", [
    ('Ligne A', 'Panne signalisation', 1, 'cloturé', '2026-05-20 08:15', 25, 'Incident de niveau 1 résolu par intervention locale.'),
    ('Ligne B', 'Intempéries neige', 2, 'en cours', '2026-05-23 07:40', 60, 'Ralentissements liés aux conditions météo.'),
    ('Ligne A', 'Problème aiguillage', 1, 'cloturé', '2026-05-21 18:05', 40, 'Vérification sécurité avant reprise trafic.'),
    ('Ligne C', 'Défaut alimentation', 2, 'cloturé', '2026-05-22 14:30', 90, 'Coupure secteur, rétablissement sous 1h30.'),
    ('Ligne B', 'Obstacle sur voie', 1, 'cloturé', '2026-05-23 06:10', 15, 'Objet retiré rapidement sans impact passagers.'),
])

cur.execute("""
CREATE TABLE IF NOT EXISTS travaux (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ligne TEXT,
    type_travaux TEXT,
    statut TEXT,
    date_debut TEXT,
    date_fin TEXT,
    impact TEXT,
    commentaire TEXT
)
""")

cur.executemany("""
INSERT INTO travaux (ligne, type_travaux, statut, date_debut, date_fin, impact, commentaire)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", [
    ('Ligne A', 'Remplacement aiguillage', 'prévu', '2026-06-01', '2026-06-03', 'Interruption partielle nuit', 'Travaux programmés maintenance préventive.'),
    ('Ligne B', 'Réfection voie ballast', 'en cours', '2026-05-20', '2026-05-30', 'Ralentissement 30km/h', 'Travaux urgents suite détérioration.'),
    ('Ligne C', 'Inspection tunnel T3', 'prévu', '2026-06-15', '2026-06-16', 'Interruption totale nuit', 'Inspection réglementaire annuelle.'),
    ('Ligne A', 'Mise à jour signalisation', 'terminé', '2026-05-10', '2026-05-12', 'Aucun', 'Migration vers signalisation numérique.'),
])

conn.commit()
conn.close()
print(f"Base SQLite créée : {DB_PATH}")