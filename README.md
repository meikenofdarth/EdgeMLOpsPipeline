# Miniature IoT MLOps Pipeline (Containerized)

This project is a fully functional, miniature MLOps system for an IoT use case. It is fully containerized with Docker, making it portable, reproducible, and easy to run.

The system demonstrates a complete, automated loop: data ingestion, edge inference, model drift detection, automated retraining, and live monitoring.

### Core Features
- **Containerized Services:** All components (broker, publisher, inference, dashboard, MLflow) run as isolated services managed by Docker Compose.
- **Resilient Startup:** Services use healthchecks to ensure they start in the correct order, preventing race conditions.
- **Real-time Inference:** An edge service subscribes to sensor data via MQTT, makes predictions, and monitors its own performance (RMSE).
- **Automated Drift Detection & Retraining:** If model performance degrades, the system automatically triggers a training script to create and deploy a new model.
- **Experiment Tracking:** MLflow tracks training runs, parameters, metrics, and models.
- **Live Dashboard:** A Streamlit dashboard provides a real-time view of the pipeline's health and live sensor data.

---

### Prerequisites
- **Docker Desktop:** Must be installed and running.
- **Git:** For cloning the repository.
- A terminal or command prompt.

---

### Setup Instructions

**1. Clone the Repository**
```bash
git clone https://github.com/YOUR_USERNAME/edge-mlops-mini.git
cd edge-mlops-mini
```

**2. Create the Mosquitto Configuration**
The MQTT broker requires a configuration file to allow connections from other containers.

*   Create a new folder named `mosquitto` in the project root.
*   Inside the `mosquitto` folder, create a new file named `mosquitto.conf`.
*   Add the following two lines to `mosquitto.conf`:
    ```
    listener 1883 0.0.0.0
    allow_anonymous true
    ```

**Your setup is complete!** The project is now ready to run.

---

### How to Run the System

The entire application is managed by Docker Compose.

**Step 1: Launch All Services**

Run the following command in your terminal from the project's root directory. The first time you run this, it will build the Docker image, which may take a few minutes.

```bash
docker-compose up --build
```

You will see logs from all five services starting up.

**Step 2: Train the First Model**

The `edge_infer` service will not start making predictions until a model exists.

1.  Let the main system run for about **30-60 seconds** so the publisher can generate some initial data in `data/raw.csv`.
2.  Open a **second, new terminal window**.
3.  In this new terminal, run the training script as a one-off task:
    ```bash
    docker-compose run --rm edge_infer python cloud/train.py
    ```
4.  This command will start a temporary container, run the training script, save a model to the `models/` directory, and then exit.

**Step 3: Observe the Running System**

Go back to your first terminal. You will see the `edge_infer` service logs change. It will detect the new model, load it, and begin printing real-time predictions.

*   **Live Dashboard:** Open your browser to **`http://localhost:8501`**
*   **MLflow UI:** Open another browser tab to **`http://localhost:5001`**

**To Stop Everything:**
1. Press `Ctrl+C` in the terminal where the services are running.
2. Run `docker-compose down` for a clean shutdown.

---