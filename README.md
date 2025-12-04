Ce README est en français. Pour la version anglaise, voir [README_en.md](README_en.md).

# Système Intelligente de Gestion Logistique

Un système prédictif de bout en bout pour la gestion logistique utilisant **Apache Spark**, **Machine Learning**, **FastAPI**, **Airflow**, **PostgreSQL**, **MongoDB** et **Streamlit**.

---

## **Présentation du projet**

Ce projet a pour objectif de **prédire et suivre les opérations logistiques en temps réel**. Il traite des données de commandes en streaming, applique un modèle ML pré-entraîné pour prédire les délais de livraison et fournit un tableau de bord interactif.

**Fonctionnalités principales :**
- **Streaming de données en temps réel** avec Spark Structured Streaming
- **Prédictions ML** utilisant un pipeline GBT entraîné
- **Orchestration** avec Apache Airflow
- **Stockage des données** dans PostgreSQL et MongoDB
- **Tableau de bord interactif** avec Streamlit, incluant l’actualisation automatique

---

## **Technologies utilisées**

- **Python :** 3.11  
- **Traitement des données & ML :** `pyspark`, `scikit-learn`, `numpy`, `pandas`  
- **Streaming & API :** `fastapi`, `uvicorn`, `websockets`  
- **Orchestration :** `apache-airflow`  
- **Bases de données :** `postgresql`, `pymongo`  
- **Tableau de bord & visualisation :** `streamlit`, `streamlit-autorefresh`, `matplotlib`, `seaborn`

---

## **Installation**

### **1. Cloner le dépôt**

```bash
git clone https://github.com/anass17/Systeme-Predictif-Intelligent-de-Gestion-Logistique
cd Systeme-Predictif-Intelligent-de-Gestion-Logistique
```

### **2. Créer un environnement Python**

```bash
py -m venv venv
venv\Scripts\activate   # Windows
# ou
source venv/bin/activate # Linux / Mac
```

### **3. Installer les dépendances**

```bash
pip install -r requirements.txt
```

### **4. Configurer PostgreSQL et MongoDB**

- **PostgreSQL** : créer la base `logistiques_db` et la table `predictions_logistique`.

- **MongoDB** : s'assurer qu’il fonctionne localement.

### **5. Lancer le serveur FastAPI (API simulée)**

```bash
uvicorn src.api:app --host 127.0.0.1 --port 8000
```

### **6. Lancer Spark Streaming + Pipeline ML**

```bash
py spark.py
```

### **7. Lancer le tableau de bord Streamlit**

```bash
streamlit run dashboard.py
```

Le tableau de bord se mettra à jour automatiquement avec les nouvelles prédictions.

### **8. (Optionnel) Lancer les DAGs Airflow**

**Note Windows :** les daemons Airflow (-D) ne sont pas supportés.

```bash
# Terminal 1
airflow db init
airflow scheduler
```

```bash
# Terminal 2
airflow webserver
```

## **Structure du projet**

```
├─ data/                    
├─ models/                  # Modèles ML entraînés
│  ├─ gbt_cv_pipeline       # Le Modèle GBT utiliser
├─ notebooks/               # Jupyter Notebooks utiliser pour le traitement
│  ├─ data-loading.ipynb    # Chargement de données brutes et selectionne de colonnes
│  ├─ data-cleaning.ipynb   # Pre-traitement de données 
│  ├─ pipeline.ipynb        # Entrainement de pipelines (GBT, Logistic Regression et Random Forest) et choix du meilleur modèle
│  └─ analyse.ipynb         # Visualisation
├─ dags/                    # DAGs Airflow
├─ main.py                  # Serveur FastAPI simulé + websocket
├─ bridge_ws_tcp.py            
├─ spark.py                 # Spark streaming & pipeline ML
├─ dashboard.py             # Tableau de bord Streamlit
├─ requirements.txt
└─ README.md
```

## **Utilisation**

1. Démarrer le serveur FastAPI pour générer les données en streaming.

2. Lancer le script Spark pour consommer les données, appliquer le modèle ML et stocker les prédictions.

3. Ouvrir le tableau de bord Streamlit pour visualiser les prédictions en temps réel.

4. Optionnel : utiliser Airflow pour orchestrer des tâches ETL ou batch.

## **Remarques**

- Utiliser `Python 3.11` pour compatibilité avec `PySpark 3.5.1`

- Installer `winutils.exe` sur Windows pour les opérations Hadoop locales.

- La connexion PostgreSQL nécessite `psycopg2-binary`.

- L’actualisation automatique du tableau de bord utilise `streamlit-autorefresh`.

---

## Visualisations du projet

### Interface Airflow
![Airflow UI](https://github.com/user-attachments/assets/981a9138-8b79-4456-83f2-6e8b2fb81e8d)

### Interface Streamlit
![Streamlit UI](https://github.com/user-attachments/assets/5266fc01-b3ee-4dd2-b698-95f2a0cfa231)