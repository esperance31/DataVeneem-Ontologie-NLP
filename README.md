# DataVeneem-Ontologie-NLP
DataVeneem-Ontologie-NLP est un système d’interrogation basé sur la connaissance d’un graphe RDF (ontologie), utilisant le NLP en français avec spaCy pour répondre aux questions sur DataVeneem, une startup virtuelle spécialisée dans le traitement de données.



## 📌 Fonctionnalités
- Compréhension de questions en français grâce à des calculs de simirilités avec **spaCy**
- Interrogation d’une **base de connaissances RDF** avec **SPARQL**
- Interaction simple en ligne de commande sur un terminal

## 📚 Base de connaissances
La base de connaissances est représentée sous forme de graphe RDF dans `graph.py` et dataveneem.ttl.  
Elle contient les informations clés sur les entités de DataVeneem :
- Services proposés
- Ressources utilisées
- Clients
- Partenaires
- Modèle économique (sources de revenus)

## DataVeneem-Ontologie-NLP
│
├─ graph.py              # Définition du graphe RDF de DataVeneem (entités et relations)
├─ dataveneem.ttl        # Fichier TTL représentant le graphe RDF
├─ query.py              # Script principal pour interroger la base de connaissances avec NLP
├─ inferrenceSpacy.py    # code python utilisant spacy pour demander les questions utilisateurs à travers un système de menu et mapper les mots clés afin de construire la requête SPARQL et afficher la réponse 
└─ requirements.txt      # Dépendances Python (spacy, rdflib, etc.)


