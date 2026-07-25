# 🏎️ F1 Monitored

An end-to-end Formula 1 analytics pipeline built with **FastAPI** and **FastF1**.

## Prerequisites

- Python 3.11 or later
- Git

## Installation

### Clone the repository

```bash
git clone <repository-url>
cd f1-monitored
```

### Create a virtual environment

```bash
python -m venv .venv
```

### Activate the environment

**Windows**

```cmd
.venv\Scripts\activate
```

**macOS/Linux**

```bash
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the server

```bash
uvicorn app.main:app --reload
```

Visit:

- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs

Expected response:

```json
{
  "status": "green"
}
```