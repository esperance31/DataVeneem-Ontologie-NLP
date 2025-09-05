import spacy
from graph import g, ex
from rdflib.plugins.sparql import prepareQuery
import warnings

# Supprimer les warnings pour les vecteurs vides
warnings.filterwarnings("ignore", message=".*empty vectors.*")

# Charger le modèle NLP
try:
    nlp = spacy.load("fr_core_news_md")
    #print("✅ Modèle français avec vecteurs chargé.")
except:
    try:
        nlp = spacy.load("en_core_web_md")
        #print("✅ Modèle anglais avec vecteurs chargé.")
    except:
        #print("⚠️ Modèles avec vecteurs non trouvés.")
        nlp = spacy.load("fr_core_news_sm")

# MAPPING ALIGNÉ AVEC VOTRE GRAPHE RDF
mapping = {
    "revenus": {
        "keywords": [
            "revenu", "revenus", "chiffre", "affaires", "gains", "bénéfice", 
            "argent", "finances", "financier", "abonnement", "tarif", "prix",
            "combien", "coût", "coute", "montant"
        ],
        "query": """
            SELECT ?revenu WHERE {
                ex:DataVeneem ex:aPourRevenu ?revenu .
            }
        """,
        "description": "Informations sur les revenus de DataVeneem"
    },
    
    "clients": {
        "keywords": [
            "client", "clients", "clientèle", "utilisateur", "consommateur",
            "acheteur", "PME", "entreprise", "particulier", "qui", "cible"
        ],
        "query": """
            SELECT ?client WHERE {
                ex:DataVeneem ex:aPourClient ?client .
            }
        """,
        "description": "Types de clients de DataVeneem"
    },
    
    "services": {
        "keywords": [
            "service", "services", "prestation", "prestations", "offre", "offres",
            "produit", "produits", "activité", "activités", "que", "quoi", 
            "proposez", "faites", "collecte", "traitement", "sauvegarde"
        ],
        "query": """
            SELECT ?service WHERE {
                ex:DataVeneem ex:aPourService ?service .
            }
        """,
        "description": "Services proposés par DataVeneem"
    },
    
    "ressources": {
        "keywords": [
            "ressource", "ressources", "moyen", "moyens", "outil", "outils",
            "matériel", "infrastructure", "cloud", "serveur", "serveurs",
            "AWS", "API", "technologie", "comment"
        ],
        "query": """
            SELECT ?ressource WHERE {
                ex:DataVeneem ex:utiliseRessource ?ressource .
            }
        """,
        "description": "Ressources utilisées par DataVeneem"
    },
    
    "partenaires": {
        "keywords": [
            "partenaire", "partenaires", "collaborateur", "collaborateurs",
            "associé", "associés", "consultant", "consultants", "fournisseur",
            "fournisseurs", "avec", "ensemble"
        ],
        "query": """
            SELECT ?partenaire WHERE {
                ex:DataVeneem ex:aPourPartenaire ?partenaire .
            }
        """,
        "description": "Partenaires de DataVeneem"
    }
}

def has_vectors(doc_or_token):
    """Vérifier si un document/token a des vecteurs disponibles"""
    return doc_or_token.has_vector and doc_or_token.vector_norm > 0

def calculate_semantic_similarity(question_doc, category_data):
    """Calculer la similarité sémantique entre la question et une catégorie"""
    max_similarity = 0
    best_matches = []
    
    # Créer un document avec tous les mots-clés de la catégorie
    keywords_text = " ".join(category_data["keywords"])
    keywords_doc = nlp(keywords_text)
    
    # Similarité document vs document (approche globale)
    if has_vectors(question_doc) and has_vectors(keywords_doc):
        doc_similarity = question_doc.similarity(keywords_doc)
        if doc_similarity > max_similarity:
            max_similarity = doc_similarity
    
    # Similarité token par token (approche fine)
    for q_token in question_doc:
        if not q_token.is_stop and not q_token.is_punct and has_vectors(q_token):
            for keyword in category_data["keywords"]:
                keyword_doc = nlp(keyword)
                if has_vectors(keyword_doc):
                    token_similarity = q_token.similarity(keyword_doc)
                    if token_similarity > 0.6:  # Seuil pour match individuel
                        best_matches.append((q_token.text, keyword, token_similarity))
                    if token_similarity > max_similarity:
                        max_similarity = token_similarity
    
    return max_similarity, best_matches

def question_to_sparql_hybrid(question):
    """Version hybride: matching exact + similarité sémantique"""
    question_lower = question.lower()
    question_doc = nlp(question_lower)
    
    results = []
    
    
    # Pour chaque catégorie, calculer le score
    for category, data in mapping.items():
        exact_matches = []
        semantic_score = 0
        semantic_matches = []
        
        # 1. Vérification des matches exacts
        for keyword in data["keywords"]:
            if keyword in question_lower:
                exact_matches.append(keyword)
        
        # 2. Calcul de similarité sémantique
        if nlp.meta.get('vectors', {}).get('width', 0) > 0:
            semantic_score, semantic_matches = calculate_semantic_similarity(question_doc, data)
        
        # 3. Score final combiné
        final_score = 0
        if exact_matches:
            final_score = 1.0  # Match exact = priorité maximale
        elif semantic_score > 0.5:
            final_score = semantic_score
        
        
        
        if final_score > 0.5:
            results.append((category, final_score, data))
    
    # Retourner la meilleure catégorie
    if results:
        results.sort(key=lambda x: x[1], reverse=True)
        best_category, best_score, best_data = results[0]
        #print(f"\n✅ CATÉGORIE SÉLECTIONNÉE: {best_category.upper()} (score: {best_score:.3f})")
        return best_data["query"]
    
    return None

def poser_question_amelioree(question):
    """Version améliorée du traitement des questions"""
    if not question.strip():
        return ["Veuillez poser une question."]
    
    sparql_query = question_to_sparql_hybrid(question)
    
    if sparql_query:
        try:
            print(f"\n Requête SPARQL:")
            print(sparql_query.strip())
            
            q = prepareQuery(sparql_query, initNs={"ex": ex})
            results = g.query(q)
            reponses = [str(row[0]) for row in results]
            
            if not reponses:
                return ["Aucun résultat trouvé dans la base de connaissances."]
            
            return reponses
            
        except Exception as e:
            return [f"Erreur lors de l'exécution de la requête : {e}"]
    else:
        suggestions = []
        #print(f"\n💡 SUGGESTIONS basées sur votre graphe:")
        for category, data in mapping.items():
            suggestions.append(f"• {category.title()}: {data['description']}")
        
        return [
            "Je n'ai pas compris la question.",
            "Voici ce que je peux vous dire sur DataVeneem:",
            *suggestions,
            "",
            "Exemple de questions:",
            "• 'Quels sont vos revenus ?'",
            "• 'Qui sont vos clients ?'", 
            "• 'Que proposez-vous comme services ?'"
        ]

def tester_exemples():
    """Tester avec des exemples basés sur votre graphe - Mode sélection"""
    exemples = {
        1: "Quels sont vos gains financiers ?",
        2: "Combien coûtent vos services ?", 
        3: "Qui sont vos clients ?",
        4: "Que proposez-vous comme prestations ?",
        5: "Quelles ressources utilisez-vous ?",
        6: "Avec qui travaillez-vous ?",
        7: "Montrez-moi vos revenus",
        8: "Liste des partenaires",
        9: "Vos prestations disponibles",
        10: "Montrez-moi la clientèle"
    }
    
    while True:
        print("\n" + "="*60)
        print("🧪 MENU DES QUESTIONS DE TEST")
        print("="*60)
        
        # Afficher le menu
        for num, question in exemples.items():
            print(f"  {num:2d}. {question}")
        
        print("\n  Options supplémentaires:")
        print("  99. Tester toutes les questions")
        print("   0. Retour au menu principal")
        
        # Demander le choix
        try:
            choix = input("\n🎯 Choisissez une question à tester (numéro) : ").strip()
            
            if choix == "0":
                print("↩️ Retour au menu principal")
                break
            
            elif choix == "99":
                # Tester toutes les questions
                print("\n" + "🚀 EXÉCUTION DE TOUS LES TESTS")
                print("="*60)
                
                for i, question in exemples.items():
                    print(f"\n🔸 Test {i}: '{question}'")
                    print("-" * 50)
                    reponses = poser_question_amelioree(question)
                    print("\n🎯 Réponses:")
                    for j, reponse in enumerate(reponses, 1):
                        print(f"   {j}. {reponse}")
                    print("-" * 50)
                    
                    # Pause entre les tests
                    input("\n⏸️ Appuyez sur Entrée pour continuer...")
                
                print("\n✅ Tous les tests terminés!")
            
            else:
                choix_num = int(choix)
                if choix_num in exemples:
                    question_choisie = exemples[choix_num]
                    
                    print(f"\n🔸 Test sélectionné: '{question_choisie}'")
                    print("-" * 50)
                    
                    # Exécuter la question
                    reponses = poser_question_amelioree(question_choisie)
                    
                    print("\n🎯 Réponses:")
                    for j, reponse in enumerate(reponses, 1):
                        print(f"   {j}. {reponse}")
                    print("-" * 50)
                    
                    # Demander si on veut continuer
                    continuer = input("\n❓ Voulez-vous tester une autre question ? (o/N) : ").strip().lower()
                    if continuer not in ['o', 'oui', 'y', 'yes']:
                        break
                else:
                    print(f"❌ Numéro {choix_num} invalide. Choisissez entre 1 et {len(exemples)}")
        
        except ValueError:
            print("❌ Veuillez entrer un numéro valide")
        except KeyboardInterrupt:
            print("\n\n⚠️ Interruption par l'utilisateur")
            break

        

# === Interface principale ===
def main():
    print("               SYSTÈME DATAVENEEM                ")
    print("="*50)
    
   
    while True:
        
        choix = input("Choisir: [1] Question interactive [2] Tests exemples [3] Quitter : ").strip()
        
        if choix == "1":
            while True:
                question = input("\n❓ Votre question (ou 'retour') : ").strip()
                if question.lower() == 'retour':
                    break
                if question:
                    reponses = poser_question_amelioree(question)
                    print("\n✅ Réponse(s): ")
                    for i, r in enumerate(reponses, 1):
                        print(f"  {i}. {r}")
        
        elif choix == "2":
            tester_exemples()
        
        elif choix == "3":
            print("👋 Au revoir !")
            break
        
        else:
            print("⚠️ Choix invalide")

if __name__ == "__main__":
    main()