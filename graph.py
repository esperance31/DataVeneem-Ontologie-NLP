from rdflib import Graph, URIRef, Literal, RDF, Namespace

# Définir le namespace
ex = Namespace("http://example.org/")

# Créer le graphe
g = Graph()

# Ajouter les entités
g.add((ex.DataVeneem, RDF.type, ex.ModeleAffaire))
g.add((ex.Clients_PME, RDF.type, ex.Entite))
g.add((ex.Clients_GrandeEntreprise, RDF.type, ex.Entite))
g.add((ex.Particulier, RDF.type, ex.Entite))
g.add((ex.Revenus, RDF.type, ex.Entite))
g.add((ex.Couts, RDF.type, ex.Entite))
g.add((ex.Ressources, RDF.type, ex.Entite))
g.add((ex.Service, RDF.type, ex.Entite))
g.add((ex.Partenaires, RDF.type, ex.Entite))

# Ajouter les relations
g.add((ex.DataVeneem, ex.aPourRevenu, Literal("Abonnement PME : 300000 Fr / mois")))
g.add((ex.DataVeneem, ex.aPourRevenu, Literal("Services ponctuels : 20000 Fr / tâche")))
g.add((ex.DataVeneem, ex.aPourClient, Literal("PME, Grandes entreprises")))
g.add((ex.DataVeneem, ex.utiliseRessource, Literal("Cloud AWS")))
g.add((ex.DataVeneem, ex.utiliseRessource, Literal("API Big Data")))
g.add((ex.DataVeneem, ex.utiliseRessource, Literal("Materiel physique")))
g.add((ex.DataVeneem, ex.utiliseRessource, Literal("Serveurs de calcul")))
g.add((ex.DataVeneem, ex.aPourService, Literal("Collecte de données")))
g.add((ex.DataVeneem, ex.aPourService, Literal("Traitement de données")))
g.add((ex.DataVeneem, ex.aPourService, Literal("Sauvegarde sécurisée de données")))
g.add((ex.DataVeneem, ex.aPourPartenaire, Literal("Consultants data, Fournisseurs Cloud")))

#print("Graphe RDF startup DataVeneem créé avec succès !")
# --- Exporter en fichier Turtle (.ttl) ---
g.serialize(destination="dataveneem.ttl", format="turtle")
print("Fichier dataveneem.ttl créé avec succès !")