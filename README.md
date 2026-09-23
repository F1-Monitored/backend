F1 Monitored — Backend

Motorsport data, analysis and strategy simulation

The F1 Monitored backend is the engineering and data-processing layer behind F1 Monitored.

Its purpose is to take publicly available Formula 1 race data and turn it into structured information that can be used to analyse races, investigate tyre and stint behaviour, evaluate strategic decisions, and simulate alternative race scenarios.

The core idea is simple:

Real race data → Analysis → Race modelling → Strategy → Simulation

The backend is therefore more than an API serving data to a frontend. It contains the data-processing and analytical pipeline that makes the rest of the system possible.

⸻

What the Backend Does

A Formula 1 race changes continuously.

Lap pace changes. Tyres age. Gaps develop. Cars enter and leave pit windows. Track position changes the value of an undercut or overcut. Safety cars and other race events can alter the strategic situation completely.

The backend is designed to represent these changes using race data.

It takes information from a race and progressively turns it into higher-level information:

* Raw Formula 1 session data
* Processed lap data
* Stint and pit-stop information
* Tyre behaviour
* Race dynamics
* Strategic possibilities
* Simulated outcomes
* Structured context for the frontend and AI systems

This creates a single pipeline from observed race data to strategic analysis.

⸻

Data Layer

The backend uses FastF1 to access publicly available Formula 1 data.

Depending on the session and data available, this can include:

* Lap times
* Sector times
* Tyre compounds
* Tyre stints
* Pit stops
* Race positions
* Driver information
* Team information
* Session information
* Available telemetry

The raw data is not treated as the final output.

It is processed into structures that can be consumed by the different analytical modules.

This separation is important because later stages of the system should work with consistent race information rather than repeatedly interpreting raw session data.

⸻

Race Data Processing

Before meaningful analysis can be performed, the race needs to be reconstructed from the available data.

The processing layer handles the transformation of raw session information into usable race-level information.

This provides the foundation for:

* Lap-by-lap analysis
* Stint reconstruction
* Pit-stop identification
* Tyre analysis
* Race-position tracking
* Pace comparisons
* Strategy analysis

The objective is to establish what happened during the race before attempting to explain why it happened.

⸻

Tyre Analysis

Tyre behaviour is one of the key inputs into Formula 1 strategy.

The backend analyses tyre information throughout a stint to understand how tyre age and compound relate to race performance.

Depending on the available data, the analysis can consider:

* Compound
* Tyre age
* Stint length
* Lap pace
* Degradation
* Driver
* Race conditions

The output of this analysis can then be used by other parts of the system.

This is important because tyre analysis should not exist as an isolated chart or statistic. Its value comes from how it contributes to understanding the changing strategic state of a race.

⸻

Stints and Pit Stops

A race strategy is largely expressed through tyre stints and pit-stop decisions.

The backend reconstructs these events from race data so that they can be analysed in the context of the race.

This includes information such as:

* When a pit stop occurred
* Which compound was used
* How long a stint lasted
* How pace changed throughout the stint
* Position before and after a stop
* Race conditions surrounding the stop

This allows pit stops to be analysed as strategic decisions rather than simply individual events in the timing data.

⸻

Race Dynamics

Race dynamics combines information from different parts of the analytical pipeline.

The backend can use factors such as:

* Lap pace
* Driver gaps
* Race position
* Tyre state
* Stint progression
* Pit stops
* Strategic decisions

The purpose is to understand how the race developed over time.

This matters because strategy cannot be evaluated from one variable alone.

For example, a theoretically faster tyre strategy may not produce a better race result if it sacrifices track position or creates an unfavourable pit window.

Race dynamics therefore provides the context required for the strategy and simulation layers.

⸻

Strategy Engine

The strategy engine uses the available race information to investigate possible strategic decisions.

Strategic variables can include:

* Tyre compound
* Stint length
* Pit-stop timing
* Number of stops
* Tyre condition
* Race pace
* Current race state

The purpose is to move beyond simply describing the strategy that was used.

Instead, the system can investigate alternative strategic decisions and determine how they interact with the modelled race state.

This creates the basis for questions such as:

What would have happened if the pit stop had happened earlier?

What if a different tyre compound had been selected?

What if the car had extended the current stint?

⸻

Simulation

Simulation takes the strategy analysis one step further.

Historical race data tells us what happened.

Simulation allows the system to investigate what could have happened under different assumptions.

An alternative strategy can be passed through the relevant race model to estimate how the race could evolve under that scenario.

This creates a progression from:

Observed race → Current race state → Alternative strategy → Simulated outcome

The simulation is therefore not intended to reproduce a professional F1 team’s proprietary simulator.

It is a modelling system built from publicly available data and explicitly defined assumptions.

⸻

Optimisation

Once alternative strategies can be simulated, they can be compared.

The optimisation layer is intended to explore strategic possibilities and identify strong candidates according to the assumptions and objectives defined by the model.

This creates the final analytical progression:

Data → Analysis → Strategy → Simulation → Comparison

The important part is that the result can be traced back through the underlying analysis rather than appearing as an unexplained recommendation.

⸻

AI Context Generation

The AI component sits downstream of the main engineering pipeline.

The backend first processes and analyses the race data before structured information is provided to the AI layer.

The intended relationship is:

Raw data → Processing → Analysis → Strategy/Simulation → Structured context → AI

This means the AI system is not responsible for determining the underlying race data.

Instead, it can use information already produced by the analytical system to generate higher-level explanations and contextual responses.

Keeping these stages separate also makes it easier to inspect and validate the underlying engineering calculations independently from the AI output.

⸻

Backend Architecture

The backend is organised around the progression from data processing to motorsport analysis and finally to strategy and simulation.

At a high level, the flow is:

FastF1 → Data Processing → Laps/Stints/Pit Stops → Tyre Analysis → Race Dynamics → Strategy Engine → Simulation → Optimisation → API

The API then exposes the relevant backend functionality to the separate F1 Monitored frontend.

This separation allows the backend to focus on the underlying data and engineering models while the frontend focuses on presenting the results.

⸻

Engineering Principles

Data before conclusions

The system starts from race data and builds its conclusions from the available evidence.

Modular analysis

Different parts of the race-analysis process are separated into individual modules so they can be developed and tested independently.

Explainable results

Where possible, analytical results should be understandable from the underlying variables and calculations rather than being treated as black-box outputs.

Explicit assumptions

Simulation results depend on the assumptions used by the model. Those assumptions should therefore be recognised when interpreting results.

Validation

Analytical and simulation outputs should be compared against known race behaviour wherever possible.

⸻

Validation and Limitations

F1 Monitored uses publicly available Formula 1 data.

It does not have access to the proprietary datasets, vehicle models, simulation tools or strategic information available to professional Formula 1 teams.

As a result, parts of the system may simplify areas such as:

* Tyre degradation
* Traffic
* Overtaking
* Car performance
* Race-state estimation
* Safety-car effects
* Environmental conditions
* Interactions between competing strategies

These limitations are important when interpreting simulation results.

The purpose of the project is not to claim that it reproduces a professional team’s internal race simulator.

The purpose is to demonstrate how real motorsport data can be transformed into an engineering system capable of analysing races and investigating alternative strategic decisions.

⸻

Technology

The backend is primarily built using:

* Python — Core backend and analytical development
* FastF1 — Formula 1 data access
* Pandas — Data processing and analysis
* NumPy — Numerical computation
* FastAPI — API layer
* Pytest — Testing
* Git / GitHub — Version control and collaboration

Additional dependencies are listed in requirements.txt.

⸻

Repository Structure

The backend is divided according to the different stages of the processing and analysis pipeline.

backend/
├── data/
├── analysis/
├── strategy/
├── simulation/
├── ai/
├── api/
├── tests/
├── requirements.txt
└── README.md

The structure may evolve as the system develops.

⸻

Getting Started

Requirements

* Python 3.11+
* Git
* Internet connection for retrieving Formula 1 data

Clone the repository

git clone <repository-url>
cd backend

Create a virtual environment

python -m venv .venv

Activate it on macOS/Linux:

source .venv/bin/activate

On Windows:

.venv\Scripts\activate

Install dependencies

pip install -r requirements.txt

Environment Variables

If environment variables are required, create a local .env file using the project’s example configuration.

Do not commit private credentials, tokens or API keys to the repository.

⸻

Running the Backend

Start the FastAPI application using the project’s configured entry point.

For example:

uvicorn <api-entry-point>:app --reload

The exact entry point depends on the current API structure of the repository.

Once running, the backend provides the API endpoints consumed by the F1 Monitored frontend.

⸻

Testing

Run the test suite with:

pytest

Tests are used to verify individual components of the backend and reduce the risk of changes affecting existing functionality.

As the analytical models develop, validation against known race behaviour will also become increasingly important.

⸻

Relationship with the Frontend

F1 Monitored is split into separate backend and frontend repositories.

The backend is responsible for:

* Data access
* Data processing
* Motorsport analysis
* Strategy logic
* Simulation
* Optimisation
* AI context
* API services

The frontend is responsible for:

* User interface
* Data visualisation
* Interactive dashboards
* Presenting analytical results
* User interaction with the backend

This separation allows both sides of the system to be developed independently while communicating through the API.

⸻

Project Status

F1 Monitored is an actively developed collaborative project.

The backend currently covers the main stages of the intended analytical pipeline, including:

* Formula 1 data ingestion
* Race data processing
* Lap analysis
* Stint analysis
* Pit-stop analysis
* Tyre analysis
* Race dynamics
* Strategy generation
* Simulation
* Optimisation
* AI context generation
* API development

The system is continuing to evolve as the models, validation methods and API integration are developed.

⸻

Why We Built It

Formula 1 produces an enormous amount of data.

The interesting engineering problem is what can be done with that data.

F1 Monitored focuses on the transition from raw information to useful engineering insight.

Rather than stopping at:

“What happened?”

the system is designed to progress towards:

“Why did it happen?”

and eventually:

“What could have happened if the strategy had been different?”

That progression — from data to analysis to simulation — is the central idea behind the F1 Monitored backend.

⸻

Team

F1 Monitored is a collaborative project developed by a student engineering team.

The project involves work across:

* Backend engineering
* Frontend development
* Data analysis
* Motorsport modelling
* API development
* Documentation
* Testing

Individual contributions can be viewed through the GitHub repository history and contribution records.
