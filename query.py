from rdflib.plugins.sparql import prepareQuery
from graph import ex, g

# --- Requête SPARQL pour lister les services ---
q_services = prepareQuery("""
SELECT ?service WHERE {
  ex:DataVeneem ex:aPourService ?service .
}
""", initNs={"ex": ex})

print("--- Services proposés par DataVeneem ---")
for row in g.query(q_services):
    print(row.service)

# --- Requête SPARQL pour lister toutes les ressources ---
q_ressources = prepareQuery("""
SELECT ?ressource WHERE {
  ex:DataVeneem ex:utiliseRessource ?ressource .
}
""", initNs={"ex": ex})

print("\n--- Ressources utilisées par DataVeneem ---")
for row in g.query(q_ressources):
    print(row.ressource)

# --- Requête SPARQL pour lister tous les revenus ---
q_revenus = prepareQuery("""
SELECT ?revenu WHERE {
  ex:DataVeneem ex:aPourRevenu ?revenu .
}
""", initNs={"ex": ex})

print("\n--- Revenus de DataVeneem ---")
for row in g.query(q_revenus):
    print(row.revenu)
    
# Lister les partenaires
q_partenaires = prepareQuery("""
SELECT ?partenaire WHERE {
  ex:DataVeneem ex:aPourPartenaire ?partenaire .
}
""", initNs={"ex": ex})

print("\n--- Partenaires de DataVeneem ---")
for row in g.query(q_partenaires):
    print(row.partenaire)
