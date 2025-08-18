import os
import asyncio
from dotenv import load_dotenv

from openai import AsyncAzureOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel, set_default_openai_client, set_tracing_disabled

from app.models import CareProblems


# Load environment variables
load_dotenv()

# Create OpenAI client using Azure OpenAI
azure_open_ai_client = AsyncAzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT")
)

# Set the default OpenAI client for the Agents SDK
set_default_openai_client(azure_open_ai_client)
set_tracing_disabled(disabled=True) # Prevent any data from being sent to OpenAI


INSTRUCTIONS = """
Je bent een ervaren verpleegkundige in een verpleeghuis die zorgdossiers analyseert. Je spreekt en schrijft vloeiend Nederlands.

Je taak is om uit een clientdossier de drie belangrijkste zorgproblemen te identificeren.

Instructies:
- Geef uitsluitend problemen terug die uit het dossier blijken. Verzin er niets bij, ga nergens van uit
- Focus vooral op de laatste zes weken. Eerdere rapportages zijn meegegeven als context
- Geef prioriteit aan problemen die de kwaliteit van leven en veiligheid van de bewoner beïnvloeden
- Voor elk probleem geef je een titel, een korte beschrijving en je redenering waarom dit een belangrijk probleem is.

Analyseer het dossier systematisch en identificeer de drie meest urgente zorgproblemen.
"""

problem_identification_agent = Agent(
    name="ProblemIdentificationAgent",
    instructions=INSTRUCTIONS,
    model=OpenAIChatCompletionsModel(
        model="gpt-4o",
        openai_client=azure_open_ai_client
    ),
    output_type=CareProblems,
)


async def run_agent_on_dossier(dossier):
    with open("data/vb_dossier.txt", "r", encoding="utf-8") as f:
        dossier_content = f.read()

    result = await Runner.run(
        problem_identification_agent,
        f"Clientdossier:\n{dossier}",
    )
    return result


if __name__ == "__main__":
    async def main():
        dossier = "Voorbeeld dossier inhoud hier"
        result = await run_agent_on_dossier(dossier)
        print(result)

    asyncio.run(main())