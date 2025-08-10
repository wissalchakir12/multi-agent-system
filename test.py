import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.mistral import MistralChat
from agno.team.team import Team
from agno.tools.yfinance import YFinanceTools
from agno.tools.reasoning import ReasoningTools

# Charger les variables d'environnement depuis .env
load_dotenv()

# Récupération de la clé API Mistral
api_key = os.getenv("MISTRAL_API_KEY")
if not api_key:
    raise ValueError("⚠️ La variable d'environnement MISTRAL_API_KEY n'est pas définie dans le fichier .env")

# Agent 1 : collecte des données financières
data_agent = Agent(
    name="Data Agent",
    role="Fetch stock data and key financial metrics",
    model=MistralChat(id="mistral-medium", api_key=api_key),
    tools=[YFinanceTools(stock_price=True, stock_fundamentals=True)],
    instructions="Fetch current stock price and fundamentals for the requested symbol using markdown tables.",
    add_datetime_to_instructions=True,
)

# Agent 2 : analyse et conseil
analysis_agent = Agent(
    name="Analysis Agent",
    role="Analyze financial data and provide investment insights",
    model=MistralChat(id="mistral-medium", api_key=api_key),
    instructions="Analyze the financial data provided and give clear, concise investment recommendations.",
    add_datetime_to_instructions=True,
)

# Création de la team pour coordonner les agents
finance_team = Team(
    name="Finance Team",
    mode="coordinate",
    model=MistralChat(id="mistral-medium", api_key=api_key),
    members=[data_agent, analysis_agent],
    tools=[ReasoningTools(add_instructions=True)],
    instructions=[
        "Collaborate to provide a brief, actionable financial summary.",
        "Use tables when presenting financial data.",
        "Present the final consolidated analysis only.",
    ],
    markdown=True,
    show_members_responses=False,
    enable_agentic_context=True,
    add_datetime_to_instructions=True,
)

if __name__ == "__main__":
    finance_team.print_response(
        "Please provide a brief financial summary for Apple (AAPL).",
        stream=False,
        show_full_reasoning=False,
        stream_intermediate_steps=False,
    )
