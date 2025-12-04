This README is in English. For the French version, see [README.md](README.md).

# Intelligent Logistics Management System

An end-to-end predictive system for logistics management using **Apache Spark**, **Machine Learning**, **FastAPI**, **Airflow**, **PostgreSQL**, **MongoDB**, and **Streamlit**.

---

## **Project Overview**

This project aims to **predict and monitor logistics operations in real time**. It processes streaming order data, applies a pre-trained ML model to predict delivery times, and provides an interactive dashboard.

## **Key Features:**
- **Real-time data streaming** with Spark Structured Streaming
- **ML predictions** using a trained GBT pipeline
- **Workflow orchestration** with Apache Airflow
- **Data storage** with PostgreSQL and MongoDB
- **Interactive dashboard** built with Streamlit, including auto-refresh

---

## **Technologies Used**

- **Python:** 3.11
- **Data Processing & ML**: `pyspark`, `scikit-learn`, `numpy`, `pandas`
- **Streaming & API**: `fastapi`, `uvicorn`, `websockets`
- **Orchestration**: `apache-airflow`
- **Databases**: `postgresql`, `pymongo`
- **Dashboard & Visualization**: `streamlit`, `streamlit-autorefresh`, `matplotlib`, `seaborn`

---

## **Installation**

### **1. Clone the repository**

```bash
git clone https://github.com/anass17/Systeme-Predictif-Intelligent-de-Gestion-Logistique
cd Systeme-Predictif-Intelligent-de-Gestion-Logistique
```

### **2. Create a Python environment**

```bash
py -m venv venv
venv\Scripts\activate   # Windows
# ou
source venv/bin/activate # Linux / Mac
```

### **3. Install dependencies**

```bash
pip install -r requirements.txt
```

### **4. Configure PostgreSQL and MongoDB**

- **PostgreSQL**: create the database logistiques_db and the table predictions_logistique.

- **MongoDB**: ensure it is running locally.

### **5. Start the FastAPI server (simulated API)**

```bash
uvicorn src.api:app --host 127.0.0.1 --port 8000
```

### **6. Run Spark Streaming + ML Pipeline**

```bash
py spark.py
```

### **7. Start the Streamlit dashboard**
```bash
streamlit run dashboard.py
```

The dashboard will automatically refresh with new predictions.

### **8. (Optional) Run Airflow DAGs**

**Windows Note:** Airflow daemons (-D) are not supported.

```bash
# Terminal 1
airflow db init
airflow scheduler
```


```bash
# Terminal 2
airflow webserver
```

## **Project Structure**

```
├─ data/                    
├─ models/                  # Trained ML models
│  ├─ gbt_cv_pipeline       # Selected GBT model
├─ notebooks/               # Jupyter notebooks for data preparation
│  ├─ data-loading.ipynb    # Raw data loading & column selection
│  ├─ data-cleaning.ipynb   # Data preprocessing
│  ├─ pipeline.ipynb        # Training pipelines (GBT, LR, RF) & model selection
│  └─ analyse.ipynb         # Visualizations
├─ dags/                    # Airflow DAG files
├─ main.py                  # Simulated FastAPI server + websocket
├─ bridge_ws_tcp.py            
├─ spark.py                 # Spark streaming & ML pipeline
├─ dashboard.py             # Streamlit dashboard
├─ requirements.txt
└─ README.md
```

## **Usage**

1. Start the FastAPI server to generate streaming data.

2. Run the Spark script to consume data, apply the ML model, and store predictions.

3. Open the Streamlit dashboard to visualize predictions in real time.

4. (Optional) Use Airflow to orchestrate ETL or batch workflows.

## **Notes**

- Use `Python 3.11` for compatibility with `PySpark 3.5.1`.

- Install `winutils.exe` on Windows for local Hadoop operations.

- PostgreSQL connection requires `psycopg2-binary`.

- Dashboard auto-refresh is enabled via `streamlit-autorefresh`.

---

## Visualisations

### Airflow Interface
![Airflow UI](https://github.com/user-attachments/assets/981a9138-8b79-4456-83f2-6e8b2fb81e8d)

### Streamlit Interface
![Streamlit UI](https://github.com/user-attachments/assets/5266fc01-b3ee-4dd2-b698-95f2a0cfa231)