import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from app.careplan_agents.problem_identification import problem_identification_agent
from app.models import CareProblems
from agents import Runner

from dotenv import load_dotenv

load_dotenv()

async def test_problem_identification():
    with open("data/vb_dossier.txt", "r", encoding="utf-8") as f:
        dossier_content = f.read()

    result = await Runner.run(
        problem_identification_agent,
        f"Clientdossier:\n{dossier_content}",
    )

    problems = result.final_output_as(CareProblems)
    print(50 * "-")
    print(f"Geïdentificeerde problemen: {[p.title for p in problems.problems]}")
    
    for i, problem in enumerate(problems.problems, 1):
        print(f"{i}. {problem.title}: \n{problem.description}\nRedenering: {problem.reasoning}")
    print(50 * "-")
if __name__ == "__main__":
    asyncio.run(test_problem_identification())
