Airbnb Price Prediction 🏠
Objectif
L'objectif de ce projet est de prédire le logarithme du prix des annonces Airbnb en utilisant des techniques de machine learning supervisé. Ce projet a été réalisé dans le cadre du cours de Data Science (Master Big Data & IA).

🗂 Données utilisées
airbnb_train.csv : données d'entraînement (avec la variable cible log_price)

airbnb_test.csv : données de test (sans la variable cible)

prediction.csv : fichier de prédictions à soumettre

Chaque ligne correspond à une annonce Airbnb avec des informations sur le logement, l'hôte, les équipements, la localisation, etc.

Étapes du projet

1. Exploration des Données (EDA)
Analyse des types de variables (numériques, catégorielles, booléennes)

Visualisation de la distribution de la variable cible log_price

Identification des valeurs manquantes et des variables non pertinentes pour la prédiction

2. Prétraitement des Données
Suppression des colonnes textuelles inutilisables directement (name, description, amenities)

Encodage des variables catégorielles avec One-Hot Encoding

Remplissage des valeurs manquantes avec des valeurs par défaut ('Missing' pour les catégories)

Alignement des colonnes entre les jeux d'entraînement et de test

3. Modélisation
Modèle utilisé : Random Forest Regressor (scikit-learn)

Séparation du jeu d'entraînement en train/validation (80%/20%)

Évaluation avec la métrique Root Mean Squared Error (RMSE)

Résultat obtenu : RMSE ≈ 0,41

4. Optimisation des Paramètres
Plusieurs tests ont été réalisés pour optimiser les hyperparamètres du modèle :

Nombre d'arbres (n_estimators)

Profondeur maximale (max_depth)

Nombre de caractéristiques (max_features)

Constat important : Malgré ces tentatives d'optimisation, le RMSE reste bloqué autour de 0,41.

Cela s’explique probablement par :

La qualité et la richesse des variables : beaucoup de colonnes textuelles ou peu informatives n'ont pas été exploitées.

La nature du problème : certaines informations clés pour prédire le prix (photos, appréciation qualitative des logements) ne sont pas présentes dans les données structurées.

5. Prédictions & Soumission
Génération du fichier prediction.csv contenant les prédictions pour le jeu de test au bon format.

