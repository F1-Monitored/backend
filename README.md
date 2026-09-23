F1 Monitored — Backend

From race data to race strategy.

F1 Monitored is a motorsport analytics and simulation system built around a simple question:

Given what we know about a race, can we reconstruct its changing state, evaluate alternative strategic decisions, and simulate what could have happened?

The backend turns publicly available Formula 1 data into the analytical foundation required to investigate that question.

REAL RACE DATA
      ↓
RECONSTRUCT THE RACE
      ↓
UNDERSTAND TYRES, STINTS & PACE
      ↓
MODEL THE RACE STATE
      ↓
GENERATE STRATEGIES
      ↓
SIMULATE ALTERNATIVES
      ↓
COMPARE & OPTIMISE

⸻

What we’re building

A Formula 1 race is not simply a sequence of laps.

Every lap changes the strategic situation.

Tyres age.
Gaps open and close.
Pit windows appear and disappear.
Traffic changes the value of an undercut.
A safety car can completely change the strategic landscape.

F1 Monitored is designed to turn the available race data into a representation of these changing conditions.

The backend therefore sits at the centre of the project:

                    FORMULA 1 DATA
                          │
                          ▼
                 ┌─────────────────┐
                 │ Data Processing │
                 └────────┬────────┘
                          │
             ┌────────────┼────────────┐
             ▼            ▼            ▼
          TYRES        STINTS        PIT STOPS
             │            │            │
             └────────────┼────────────┘
                          ▼
                   RACE DYNAMICS
                          │
                          ▼
                  STRATEGY ENGINE
                          │
                          ▼
                     SIMULATION
                          │
                          ▼
                    OPTIMISATION
                          │
                          ▼
                       API
                          │
                          ▼
                      FRONTEND

⸻

Motorsport Analysis

🛞 Tyre behaviour

Tyre performance is one of the fundamental inputs into race strategy.

F1 Monitored analyses available race data to investigate how lap performance changes with:

* compound
* tyre age
* stint length
* race pace
* degradation
* driver
* race conditions where available

The output is not treated as an isolated graph.

Tyre behaviour becomes an input to the wider race model and strategy system.

Lap Performance
       ↓
Tyre Age
       ↓
Stint Behaviour
       ↓
Degradation
       ↓
Strategic Consequences

⸻

🔧 Stints & pit stops

A strategy is ultimately a sequence of decisions.

The backend reconstructs the tyre stints and pit stops that formed the actual race, allowing the system to analyse:

* when a car stopped
* which compound was fitted
* how long each stint lasted
* how race position changed
* how the race evolved around the pit stop

This creates the historical race state against which alternative strategies can be investigated.

⸻

📈 Race dynamics

Race strategy cannot be evaluated independently from what is happening on track.

The race-dynamics layer combines information such as:

* lap pace
* driver gaps
* race position
* tyre state
* stint progression
* pit stops
* strategic decisions

The objective is to represent how the race was changing, not simply what the final classification looked like.

⸻

Strategy & Simulation

♟️ Strategy engine

The strategy engine takes the reconstructed race state and investigates possible strategic decisions.

Depending on the scenario, this can involve variables such as:

* compound selection
* stint length
* pit-stop timing
* number of stops
* tyre condition
* race pace
* current race state

The important distinction is that the system is not limited to analysing the strategy that actually happened.

It can investigate alternatives.

⸻

🔬 Simulation

Simulation is where the project moves from:

“What happened?”

to:

“What could have happened?”

A strategy can be altered and evaluated against the reconstructed race conditions.

For example:

Observed Race
     │
     ├── Actual Strategy
     │
     ├── Alternative Strategy A
     │
     ├── Alternative Strategy B
     │
     └── Alternative Strategy C
              │
              ▼
          SIMULATION
              │
              ▼
       Compare Outcomes

This provides the foundation for strategic what-if analysis.

⸻

⚙️ Optimisation

The optimisation layer builds on simulation.

Instead of evaluating one predefined strategy, the system can explore multiple possible strategies and compare their simulated outcomes.

Conceptually:

RACE STATE
    ↓
STRATEGY SEARCH SPACE
    ↓
┌────────┬────────┬────────┐
│ Strat A│ Strat B│ Strat C│ ...
└───┬────┴───┬────┴───┬────┘
    │        │        │
    └────────┼────────┘
             ↓
         SIMULATION
             ↓
       OUTCOME METRICS
             ↓
         COMPARISON
             ↓
       OPTIMISATION

The optimisation layer therefore depends on the quality of the preceding data processing, modelling and simulation stages.

⸻

Data

Data source

F1 Monitored uses FastF1 to access publicly available Formula 1 session data.

The backend processes available information including:

* lap timing
* sector timing
* tyre compounds
* tyre stints
* pit stops
* race position
* driver information
* team information
* session information
* available telemetry

The data pipeline is designed so that raw session information can be transformed into consistent inputs for the analytical modules.

⸻

AI Context

AI functionality is built on top of the analytical pipeline, rather than replacing it.

The backend prepares structured race information that can be passed to AI-powered features.

RAW DATA
   ↓
DATA PROCESSING
   ↓
RACE ANALYSIS
   ↓
STRATEGY / SIMULATION
   ↓
STRUCTURED CONTEXT
   ↓
AI

This separation keeps the underlying race analysis grounded in the actual processed data.

⸻

Engineering Approach

F1 Monitored is built around several principles.

Data before conclusions

Race insights should originate from processed race data rather than unsupported assumptions.

Models should be explainable

Where the system estimates a quantity or makes a strategic comparison, the underlying assumptions should be inspectable.

Simulation should reflect its assumptions

A simulated outcome is only as meaningful as the model behind it. The project therefore documents the assumptions and limitations of its models.

Results should be validated

Where possible, simulated or reconstructed results are compared against observed race behaviour.

Modular development

Data processing, analysis, strategy, simulation and API functionality are separated so individual components can be developed and tested independently.

⸻

Validation & Limitations

F1 Monitored works with publicly available data.

A Formula 1 team has access to substantially more information than is available through public sources, including proprietary telemetry, vehicle models, tyre models and internal race-engineering systems.

F1 Monitored therefore does not attempt to claim the fidelity of a professional team’s internal simulator.

Instead, the project treats these limitations as part of the engineering problem.

Areas requiring approximation may include:

* tyre degradation
* traffic
* overtaking
* car performance
* race-state estimation
* strategic interactions
* effects that cannot be directly observed from public data

Validation is used to understand where the models reproduce observed behaviour and where they diverge.

⸻

Backend Architecture

The backend is divided into several logical stages:

                    FASTF1
                      │
                      ▼
               DATA INGESTION
                      │
                      ▼
              DATA PROCESSING
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
        LAPS        STINTS      PIT STOPS
          │           │           │
          └───────────┼───────────┘
                      ▼
                TYRE ANALYSIS
                      │
                      ▼
                RACE DYNAMICS
                      │
                      ▼
               STRATEGY ENGINE
                      │
                      ▼
                  SIMULATION
                      │
                      ▼
                OPTIMISATION
                      │
              ┌───────┴───────┐
              ▼               ▼
        AI CONTEXT          FASTAPI
                              │
                              ▼
                          FRONTEND

⸻

Technology

Technology	Purpose
Python	Backend development and analytical modelling
FastF1	Formula 1 data access
Pandas	Data processing and analysis
NumPy	Numerical computation
FastAPI	API layer
[Other project dependencies]	Supporting functionality

⸻

Project Structure

The repository separates the major responsibilities of the backend into modular components.

backend/
│
├── data/
├── analysis/
├── strategy/
├── simulation/
├── ai/
├── api/
├── tests/
│
├── requirements.txt
└── README.md

The directory structure shown here should be kept synchronized with the actual repository.

⸻

Getting Started

Requirements

* Python 3.11+
* Git
* Internet connection for retrieving Formula 1 session data

Installation

git clone <BACKEND_REPOSITORY_URL>
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

For Windows:

.venv\Scripts\activate

⸻

Environment Variables

If the backend requires environment variables, create a local .env file based on:

.env.example

Never commit credentials, API keys or other sensitive configuration to the repository.

⸻

Running the API

The backend uses FastAPI as its API layer.

The application can be started using the project’s configured entry point.

Example:

uvicorn <module>:app --reload

Once running, the API documentation provided by FastAPI can be used to inspect and test available endpoints.

⸻

Testing

Testing is used to verify the behaviour of important backend components.

Areas of interest include:

* data processing
* tyre analysis
* race analysis
* strategy calculations
* simulation
* API functionality

Where configured:

pytest

⸻

Frontend

The backend is part of the wider F1 Monitored GitHub Organization.

The frontend is maintained separately and communicates with this backend through the API.

Frontend repository:
<FRONTEND_REPOSITORY_URL>

⸻

Project Status

F1 Monitored is an actively developed project.

Current development focuses on improving the complete pipeline from:

motorsport data → analysis → modelling → simulation → optimisation

while maintaining and expanding the existing functionality of the platform.

⸻

Team

F1 Monitored is a collaborative project developed by its project team.

Individual contributions can be inspected through the Git history and repository contribution records.

⸻

The objective

The project is ultimately built around one idea:

Use real motorsport data to understand the race, model the decisions, and investigate what could have happened differently.

⸻
