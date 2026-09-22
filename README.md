# f1-monitored
F1 Monitored — Backend

Real motorsport data → analysis → simulation → strategy

The backend of F1 Monitored is a Python-based motorsport analytics and simulation system designed to process Formula 1 race data and transform it into meaningful race, tyre, strategy and performance insights.

It provides the data-processing, analysis, simulation and API infrastructure that powers the F1 Monitored platform.

⸻

Overview

F1 Monitored combines publicly available Formula 1 data with data-processing and modelling techniques to reconstruct and analyse race events.

The backend is responsible for transforming raw session data into structured information that can be used to investigate questions such as:

* How did tyre performance evolve throughout a stint?
* How did pit stops affect race position and race time?
* How did race pace change throughout an event?
* How did different strategies influence race outcomes?
* What could have happened under alternative strategy decisions?
* How can race data be transformed into information suitable for simulation and optimisation?

The backend is designed as a modular system so that individual components can be developed, tested and improved independently.

⸻

System Architecture

The backend follows a processing pipeline in which raw motorsport data is progressively transformed into higher-level analysis and simulation outputs.

                    Formula 1 Session Data
                             │
                             ▼
                       Data Ingestion
                             │
                             ▼
                    Data Processing
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
        Lap Analysis    Pit & Stint     Tyre Analysis
                           Analysis
              │              │              │
              └──────────────┼──────────────┘
                             ▼
                       Race Dynamics
                             │
                             ▼
                       Strategy Engine
                             │
                             ▼
                         Simulation
                             │
                             ▼
                    Analysis / Optimisation
                             │
                             ▼
                      API / Frontend

The exact implementation and module structure are documented within the repository.

⸻

Core Capabilities

🏁 Race Data Processing

The backend retrieves and processes Formula 1 session data to create structured datasets suitable for analysis.

This includes information such as:

* Lap times
* Lap numbers
* Driver and team information
* Tyre compounds
* Stint information
* Pit stops
* Race position
* Sector performance
* Session information
* Other available race telemetry and timing data

The processing layer provides a consistent foundation for the analysis modules.

⸻

🛞 Tyre Analysis

The tyre-analysis system investigates how tyre performance changes throughout a stint.

The analysis can be used to examine relationships between:

* Tyre compound
* Tyre age
* Lap time
* Stint length
* Race pace
* Degradation

The purpose is to convert observed race data into information that can be used by higher-level race and strategy models.

⸻

🔧 Pit Stop & Stint Analysis

Pit stops and tyre stints are reconstructed from race data to provide a representation of how teams managed their tyres throughout a race.

This allows the system to investigate:

* Pit-stop timing
* Stint lengths
* Compound selections
* Strategy sequences
* Position changes associated with pit stops
* Race progression between strategic decisions

⸻

📈 Race Dynamics

Race-dynamics analysis combines lap-level and race-level information to examine how a race developed over time.

This can include:

* Pace evolution
* Gaps between drivers
* Position changes
* Stint behaviour
* Strategic interactions
* Race-state changes

The goal is to provide the information required to understand why the race developed the way it did, rather than simply reporting the final classification.

⸻

♟️ Strategy Engine

The strategy engine uses processed race information to investigate alternative strategic decisions.

Depending on the scenario being analysed, the system can consider factors such as:

* Tyre compounds
* Stint lengths
* Pit-stop timing
* Race pace
* Tyre behaviour
* Current race state

The strategy layer provides the foundation for evaluating alternative race scenarios.

⸻

🔬 Simulation

The backend can use processed race information and strategy assumptions to simulate alternative scenarios.

Instead of only analysing what actually happened, the simulation layer allows the system to investigate:

What might the race have looked like if a different decision had been made?

Simulation outputs can then be compared with observed race behaviour.

⸻

🤖 AI Context Generation

F1 Monitored also includes an AI-context generation component.

Rather than treating AI as the source of the underlying race data, the backend prepares structured race information and analytical context that can be supplied to AI-powered features.

This creates a separation between:

Raw Data
   ↓
Engineering Analysis
   ↓
Structured Context
   ↓
AI Interpretation

This allows the analytical components to remain grounded in the underlying race data.

⸻

🌐 API

The backend exposes functionality through an API layer so that the frontend can interact with the underlying data-processing and analysis systems.

The API acts as the interface between the backend’s analytical systems and the F1 Monitored frontend.

⸻

Data Pipeline

The general data flow is:

FastF1
  │
  ▼
Session Data
  │
  ▼
Data Cleaning & Processing
  │
  ▼
Lap / Pit / Stint Data
  │
  ├──────────────► Tyre Analysis
  │
  ├──────────────► Race Dynamics
  │
  └──────────────► Strategy Analysis
                         │
                         ▼
                     Simulation
                         │
                         ▼
                   API Responses
                         │
                         ▼
                      Frontend

This separation allows raw data processing, analytical models and API functionality to be developed independently.

⸻

Technology Stack

The backend is primarily built using:

Technology	Purpose
Python	Core backend and analytical development
FastF1	Formula 1 data access and session analysis
Pandas	Data processing and analysis
FastAPI	Backend API
NumPy	Numerical computation
[Add other libraries used by the project]	[Purpose]

The technology list should be updated as the backend develops.

⸻

Project Structure

The backend is organised into separate components according to their responsibilities.

backend/
│
├── [data / ingestion modules]
├── [analysis modules]
├── [tyre analysis]
├── [race dynamics]
├── [strategy]
├── [simulation]
├── [AI / context generation]
├── [API]
├── tests/
├── requirements.txt
└── README.md

The structure above represents the intended separation of responsibilities. The actual directory structure of the repository should be kept as the source of truth.

⸻

Getting Started

Requirements

* Python 3.11+
* Git
* Internet connection for retrieving available Formula 1 session data

Additional dependencies are listed in the project’s dependency file.

⸻

Installation

Clone the repository:

git clone <REPOSITORY_URL>
cd backend

Create a virtual environment:

python -m venv .venv

Activate it.

macOS / Linux

source .venv/bin/activate

Windows

.venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

⸻

Environment Variables

If environment variables are required, create a local .env file based on the project’s example configuration:

.env.example

Do not commit API keys, credentials or other secrets to the repository.

⸻

Running the Backend

Start the API using the project’s configured FastAPI entry point.

For example:

uvicorn <module>:app --reload

The exact command should match the current backend entry point.

Once running, the API documentation can be accessed through the FastAPI documentation interface.

⸻

API

The API provides the interface through which the frontend communicates with the backend.

It exposes functionality for retrieving and processing the analytical outputs generated by the backend.

As the API develops, endpoint documentation should include:

Endpoint	Method	Purpose
/...	GET	…
/...	POST	…

Endpoint documentation should be kept synchronized with the implemented API.

⸻

Testing

Tests are used to verify important components of the backend and reduce the risk of changes affecting existing functionality.

Run the project’s test suite using the configured testing framework.

Example:

pytest

Testing should cover critical areas such as:

* Data processing
* Tyre analysis
* Strategy calculations
* Simulation logic
* API behaviour

⸻

Validation

Because F1 Monitored works with real-world motorsport data, model validation is an important part of the project.

Where possible, simulated and analytical outputs should be compared against observed race data.

Validation can be used to investigate:

* Whether reconstructed race states match the observed race
* Whether tyre behaviour is represented reasonably
* Whether strategy simulations produce plausible outcomes
* Where model assumptions introduce differences from reality

Detailed validation studies will be documented as the project develops.

⸻

Limitations

F1 Monitored is built using publicly available motorsport data and therefore does not have access to the complete datasets, models or internal information available to Formula 1 teams.

Consequently, the system may simplify or approximate aspects of real-world race modelling.

Potential limitations include:

* Limited access to proprietary telemetry
* Simplified tyre-degradation modelling
* Simplified traffic and overtaking behaviour
* Uncertainty in estimating race-state variables
* Simplifications in strategy simulation
* Differences between publicly available timing data and a team’s internal datasets

Documenting these limitations is an important part of evaluating the system’s results.

⸻

Frontend

The F1 Monitored frontend provides the user-facing interface for the analytical capabilities developed by this backend.

The frontend and backend are maintained as separate repositories within the F1 Monitored GitHub Organization.

Frontend:
<FRONTEND_REPOSITORY_URL>

⸻

Development Philosophy

F1 Monitored is being developed around the principle:

Real motorsport data → engineering analysis → simulation → optimisation

The project aims to combine software engineering, data analysis and motorsport modelling into a single system capable of investigating real race scenarios.

The focus is not simply on displaying historical Formula 1 statistics, but on building a system in which data can be processed, analysed and used to investigate alternative race scenarios.

⸻

Project Status

F1 Monitored is an actively developed project.

The backend is being continuously improved through:

* Additional analysis capabilities
* Model refinement
* Testing and validation
* API development
* Documentation
* Integration with the frontend

⸻

Contributors

F1 Monitored is developed collaboratively by its project team.

See the repository’s contributor history for individual contributions.

⸻

License

[Add project license here]
