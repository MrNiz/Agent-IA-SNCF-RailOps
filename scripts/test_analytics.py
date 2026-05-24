# scripts/test_analytics.py

from app.tools.analytics import run_incident_query

# Test 1 : tous les incidents
print("=== Tous les incidents ===")
print(run_incident_query.invoke("SELECT ligne, type_incident, niveau, statut, duree_minutes FROM incidents"))

# Test 2 : incidents de niveau 1 seulement
print("\n=== Incidents niveau 1 ===")
print(run_incident_query.invoke("SELECT ligne, type_incident, duree_minutes FROM incidents WHERE niveau = 1"))

# Test 3 : durée moyenne par ligne
print("\n=== Durée moyenne par ligne ===")
print(run_incident_query.invoke("SELECT ligne, AVG(duree_minutes) as duree_moy FROM incidents GROUP BY ligne"))