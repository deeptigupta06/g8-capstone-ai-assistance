# Support Ticket Resolution Assistant

A read-only AI assistant that helps support analysts investigate recurring technical issues using hybrid retrieval and a controlled agent workflow.

## Project Overview

Support teams often receive similar application, authentication, access and configuration issues. Analysts may spend considerable time searching previous tickets and support documents for suitable resolutions.

This project searches resolved tickets, support documents and structured knowledge-base articles, then provides:

- Similar resolved tickets
- Relevant knowledge-base references
- Diagnostic steps
- Recommended resolution steps
- KB IDs and reference links
- Instructions for the support agent
- Document freshness warnings
- Confidence score
- Escalation guidance when evidence is insufficient

## Technology Stack

- Python
- Streamlit
- OpenAI API
- ChromaDB
- BM25 keyword search
- LangGraph
- Pydantic
- JSONL data files

## Architecture

The application follows this flow:

New support ticket
        |
        v
Application and problem selection
        |
        v
Semantic retrieval using Chroma
        +
Keyword retrieval using BM25
        |
        v
Evidence merging and reranking
        |
        v
Controlled LangGraph workflow
        |
        v
Pydantic response validation
        |
        v
Grounded recommendation or escalation

## Project Structure

app.py                         Streamlit application interface
requirements.txt               Python dependencies
.env.example                   Example API-key configuration
data/                          Tickets, documents and knowledge-base records
src/                           Retrieval, agent and response-model code
scripts/                       Data creation, indexing and evaluation scripts

## Installation

Create a virtual environment:

python -m venv .venv

Activate the environment on Windows:

.venv\\Scripts\\activate

Install the dependencies:

pip install -r requirements.txt

Create a file named .env in the project root:

OPENAI_API_KEY=your_api_key_here

Do not upload the .env file or expose the API key.

## Run the Project

Create the prototype knowledge base:

python scripts\\create_knowledge_base.py

Build the search index:

python -m scripts.build_index

Start the application:

streamlit run app.py

The application opens at:

http://localhost:8501

## Example Test Cases

Known issue:

Application: HR Leave Application
Problem: Leave request cannot be submitted
Additional details: The user receives an error after selecting the leave dates.

The system should return diagnostic steps, a recommended resolution, KB references, agent instructions and a confidence score.

Unknown issue:

Select Others and enter:

The payroll system shows an unknown error code that is not found in the knowledge base.

The system should recommend escalation rather than inventing a resolution.

## Evaluation

The system is evaluated using retrieval success in the top five results, evidence grounding, citation correctness, knowledge-base freshness warnings, escalation accuracy, response time and Pydantic output validation.

Recall@5 is calculated as:

Cases with a relevant result in the top five divided by total evaluation cases.

Run the evaluation:

python -m scripts.run_evaluation

## Scope and Limitations

The assistant is read-only. It does not update or close tickets, change user access, or make changes to enterprise applications.

The current knowledge-base records are synthetic prototype records created for demonstration. The ServiceNow-style links are placeholders and are not connected to a live ServiceNow instance. Production use would require approved organisational data, privacy controls, access permissions, monitoring and human approval.

## Future Improvements

- Connect to approved ServiceNow Knowledge articles.
- Use anonymised organisational support tickets.
- Add role-based access control.
- Add analyst feedback and rating.
- Add monitoring of retrieval and escalation accuracy.
- Deploy through an internal API.
- Add human approval before recommendations are used operationally.
