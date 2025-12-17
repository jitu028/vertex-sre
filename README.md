# Vertex SRE - Autonomous Incident Response Agent

**Vertex SRE** is an autonomous AI agent designed to mimic the capabilities of a Site Reliability Engineer (SRE) on Google Cloud Platform. Unlike passive chatbots, this system proactively monitors your infrastructure, discovers topology, correlates signals (Logs, Traces, Deployments), and uses Vertex AI (Gemini) to determine root causes and suggest remediations.

![Vertex SRE](https://www.gstatic.com/cloud/images/social/cloud-console-social.png)

## 🚀 Key Features

*   **Autonomous Discovery**: Uses Cloud Asset Inventory to build a dynamic graph of your infrastructure dependencies.
*   **Event-Driven Architecture**: Reacts to Pub/Sub events from Cloud Monitoring alerts in real-time.
*   **AI-Powered Analysis**: Leverages Google's **Gemini 2.5 Pro** model (`gemini-2.5-pro`) on Vertex AI to analyze error logs, topology contexts, and recent deployments.
*   **Deployment Correlation**: Automatically links incidents to recent Cloud Build deployments to identify bad code changes.
*   **Mission Control UI**: A dedicated Streamlit dashboard for operators to visualize incidents, view AI analysis, and trigger remediations.

## 🏗️ Architecture

The system consists of three main components:

1.  **Ingest & Analysis (Backend)**: Fast API service running on Cloud Run. It handles Pub/Sub payloads, queries Cloud APIs, and prompts Vertex AI.
2.  **Operator Console (Frontend)**: Streamlit application running on Cloud Run. Provides the human-in-the-loop interface.
3.  **Event Bus**: Google Cloud Pub/Sub topic (`sre-incident-bus`) that decouples alert sources from the analysis engine.

## 🛠️ Tech Stack

*   **Compute**: Google Cloud Run (Serverless)
*   **AI**: Vertex AI (Gemini 2.5 Pro)
*   **Backend**: Python, FastAPI, Pydantic
*   **Frontend**: Streamlit
*   **Infrastructure**: Terraform
*   **Data Sources**: Cloud Logging, Cloud Asset Inventory, Cloud Build

## 📋 Prerequisites

*   Google Cloud Platform Project
*   `gcloud` CLI installed and authenticated
*   Docker installed
*   Terraform >= 1.0

## ⚡ Quick Deployment

A helper script is provided to automate the build and deployment process to your GCP project.

1.  Clone the repository:
    ```bash
    git clone https://github.com/jitu028/vertex-sre.git
    cd vertex-sre
    ```

2.  Run the deployment script:
    ```bash
    ./deployment.sh <YOUR_PROJECT_ID> [REGION]
    ```
    *Example:* `./deployment.sh my-gcp-project us-central1`

    This script will:
    *   Enable necessary Google Cloud APIs.
    *   Build and push Docker images for Backend and Frontend.
    *   Provision all infrastructure using Terraform.

## 💻 Local Development

You can run the agent locally for testing and development.

1.  **Setup Environment**:
    Inside `backend/`, create a `.env` file:
    ```bash
    PROJECT_ID=<YOUR_PROJECT_ID>
    REGION=us-central1
    ```

2.  **Start the Backend**:
    ```bash
    cd backend
    pip install -r requirements.txt
    uvicorn main:app --reload --port 8000
    ```

3.  **Start the Frontend**:
    ```bash
    cd frontend
    pip install -r requirements.txt
    streamlit run app.py
    ```

4.  **Simulate an Incident**:
    We provide a script to mimic a Pub/Sub alert push to the local backend.
    ```bash
    python3 scripts/simulate.py
    ```
    Check the Streamlit dashboard (default: `http://localhost:8501`) to see the incident analysis.

## 📂 Project Structure

```
.
├── backend/            # FastAPI Application (Analysis Engine)
├── frontend/           # Streamlit Application (Dashboard)
├── terraform/          # Infrastructure as Code
├── scripts/            # Helper scripts (Simulation)
├── deployment.sh       # Automation script
```

## 📄 License

[MIT](LICENSE)
