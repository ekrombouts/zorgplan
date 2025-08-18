from agents import Runner, trace, gen_trace_id
from app.careplan_agents import (
    problem_identification_agent,
    care_plan_agent, 
    dietist_agent,
    fysio_agent,
    format_agent,
    email_agent
)
from app.models import (
    CareProblems,
    CarePlanRule,
    SpecialistAdvice,
    CompleteCareplan,
)
import asyncio
from typing import List


class CareplanManager:

    async def run(self, dossier_content: str):
        """
        Voer het complete zorgplanproces uit, met status updates

        Voert het volledige zorgplanproces uit als een asynchrone generator, waarbij tussentijdse statusupdates worden gegeven.
        Ontvangt het dossier als tekst, analyseert problemen, stelt zorgplanregels op, vraagt specialistisch advies,
        stelt het zorgplan samen, formatteert het resultaat en verstuurt het per e-mail. Geeft statusberichten en het
        geformatteerde zorgplan terug via yield.
        
        Args:
            dossier_content (str): De inhoud van het cliëntdossier als tekst.

        Yields:
            str: Statusupdates en het geformatteerde zorgplan.
        """
        trace_id = gen_trace_id()  # Genereer een unieke trace ID
        with trace("Zorgplan trace", trace_id=trace_id):
            print(
                f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}"
            )
            yield f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}"

            yield "Identificeren van zorgproblemen..."
            care_problems = await self.identify_problems(dossier_content)

            yield "Opstellen van zorgplanregels..."
            care_rules = await self.create_care_rules(dossier_content, care_problems)

            yield "Inwinnen van specialistische adviezen..."
            specialist_advice = await self.get_specialist_advice(
                dossier_content, care_problems
            )

            yield "Samenstellen van het complete zorgplan..."
            complete_careplan = await self.compile_careplan(
                dossier_content, care_rules, specialist_advice
            )

            yield "Formatteren voor weergave..."
            formatted_plan = await self.format_careplan(complete_careplan)

            yield "Versturen per email..."
            await self.send_email(complete_careplan)

            yield "Zorgplan voltooid!"
            yield formatted_plan

    async def identify_problems(self, dossier_content: str) -> CareProblems:
        """Identificeer de drie belangrijkste zorgproblemen"""
        print("Identificeren van zorgproblemen...")
        result = await Runner.run(
            problem_identification_agent,
            f"Clientdossier:\n{dossier_content}",
        )
        problems = result.final_output_as(CareProblems)
        print(f"Geïdentificeerde problemen: {[p.title for p in problems.problems]}")
        return problems

    async def create_care_rules(
        self, dossier_content: str, care_problems: CareProblems
    ) -> List[CarePlanRule]:
        """Maak voor elk probleem een zorgplanregel"""
        print("Opstellen van zorgplanregels...")
        care_rules = []

        tasks = []
        for problem in care_problems.problems:
            # Check of specialistisch advies nodig is
            needs_specialist = self._needs_specialist_advice(problem.title)

            input_text = f"""
Clientdossier:
{dossier_content}

Zorgprobleem: {problem.title}
Beschrijving: {problem.description}

{'Een van de drie acties moet "Specialistisch advies inwinnen" zijn.' if needs_specialist else ''}
"""
            task = asyncio.create_task(self._create_single_care_rule(input_text))
            tasks.append(task)

        for task in asyncio.as_completed(tasks):
            care_rule = await task
            care_rules.append(care_rule)

        print(f"Zorgplanregels opgesteld: {len(care_rules)}")
        return care_rules

    async def _create_single_care_rule(self, input_text: str) -> CarePlanRule:
        """Maak een enkele zorgplanregel"""
        try:
            result = await Runner.run(care_plan_agent, input_text)
            return result.final_output_as(CarePlanRule)
        except Exception as e:
            print(f"Fout bij maken zorgplanregel: {e}")
            # Return a default care rule in case of error
            return CarePlanRule(
                problem_title="Onbekend probleem",
                problem_description="Kon niet worden bepaald",
                goal="Te bepalen",
                actions=["Herbeoordeling nodig", "Overleg team", "Nader onderzoek"],
            )

    async def get_specialist_advice(
        self, dossier_content: str, care_problems: CareProblems
    ) -> List[SpecialistAdvice]:
        """Vraag specialistische adviezen op waar nodig"""
        print("Inwinnen van specialistische adviezen...")
        specialist_advice = []

        tasks = []
        for problem in care_problems.problems:
            if (
                "gewichtsverlies" in problem.title.lower()
                or "intake" in problem.title.lower()
                or "voeding" in problem.title.lower()
            ):
                task = asyncio.create_task(
                    self._get_dietist_advice(dossier_content, problem)
                )
                tasks.append(task)
            elif (
                "valrisico" in problem.title.lower()
                or "mobiliteit" in problem.title.lower()
                or "val" in problem.title.lower()
            ):
                task = asyncio.create_task(
                    self._get_fysio_advice(dossier_content, problem)
                )
                tasks.append(task)

        for task in asyncio.as_completed(tasks):
            advice = await task
            specialist_advice.append(advice)

        print(f"Specialistische adviezen: {len(specialist_advice)}")
        return specialist_advice

    async def _get_dietist_advice(
        self, dossier_content: str, problem
    ) -> SpecialistAdvice:
        """Krijg diëtist advies"""
        try:
            input_text = f"""
Clientdossier:
{dossier_content}

Focus op het zorgprobleem: {problem.title} - {problem.description}
"""
            result = await Runner.run(dietist_agent, input_text)
            advice = result.final_output_as(SpecialistAdvice)
            advice.specialist_type = "Diëtist"
            return advice
        except Exception as e:
            print(f"Fout bij diëtist advies: {e}")
            return SpecialistAdvice(
                specialist_type="Diëtist",
                assessment="Kon niet worden bepaald",
                recommendation="Nader overleg nodig",
            )

    async def _get_fysio_advice(
        self, dossier_content: str, problem
    ) -> SpecialistAdvice:
        """Krijg fysiotherapeut advies"""
        try:
            input_text = f"""
Clientdossier:
{dossier_content}

Focus op het zorgprobleem: {problem.title} - {problem.description}
"""
            result = await Runner.run(fysio_agent, input_text)
            advice = result.final_output_as(SpecialistAdvice)
            advice.specialist_type = "Fysiotherapeut"
            return advice
        except Exception as e:
            print(f"Fout bij fysio advies: {e}")
            return SpecialistAdvice(
                specialist_type="Fysiotherapeut",
                assessment="Kon niet worden bepaald",
                recommendation="Nader overleg nodig",
            )

    def _needs_specialist_advice(self, problem_title: str) -> bool:
        """Check of een probleem specialistisch advies nodig heeft"""
        title_lower = problem_title.lower()
        return (
            "gewichtsverlies" in title_lower
            or "intake" in title_lower
            or "voeding" in title_lower
            or "valrisico" in title_lower
            or "mobiliteit" in title_lower
            or "val" in title_lower
        )

    async def compile_careplan(
        self,
        dossier_content: str,
        care_rules: List[CarePlanRule],
        specialist_advice: List[SpecialistAdvice],
    ) -> CompleteCareplan:
        """Stel het complete zorgplan samen"""
        print("Samenstellen van het complete zorgplan...")

        # Maak een korte patiëntsamenvatting
        patient_summary = "Bewoner in verpleeghuis met complexe zorgbehoeften"

        # Maak een conclusie
        conclusion = f"Dit zorgplan bevat {len(care_rules)} hoofdproblemen en {len(specialist_advice)} specialistische adviezen ter ondersteuning van de kwaliteit van leven."

        return CompleteCareplan(
            patient_summary=patient_summary,
            care_rules=care_rules,
            specialist_advice=specialist_advice,
            conclusion=conclusion,
        )

    async def format_careplan(self, careplan: CompleteCareplan) -> str:
        """Formatteer het zorgplan voor weergave"""
        print("Formatteren van het zorgplan...")
        try:
            # Converteer naar string representatie voor de format agent
            careplan_text = f"""
Patiëntsamenvatting: {careplan.patient_summary}

Zorgplanregels:
"""
            for i, rule in enumerate(careplan.care_rules, 1):
                careplan_text += f"""
{i}. {rule.problem_title}
   Beschrijving: {rule.problem_description}
   Doel: {rule.goal}
   Acties:
"""
                for j, action in enumerate(rule.actions, 1):
                    careplan_text += f"   - {action}\n"

            if careplan.specialist_advice:
                careplan_text += "\nSpecialistische adviezen:\n"
                for advice in careplan.specialist_advice:
                    careplan_text += f"""
{advice.specialist_type}:
   Beoordeling: {advice.assessment}
   Aanbeveling: {advice.recommendation}
"""

            careplan_text += f"\nConclusie: {careplan.conclusion}"

            result = await Runner.run(format_agent, careplan_text)
            return result.final_output
        except Exception as e:
            print(f"Fout bij formatteren: {e}")
            return str(careplan)

    async def send_email(self, careplan: CompleteCareplan) -> None:
        """Verstuur het zorgplan per email"""
        print("Versturen per email...")
        try:
            # Converteer naar string voor email agent
            careplan_text = f"""
Patiëntsamenvatting: {careplan.patient_summary}

Zorgplanregels:
"""
            for i, rule in enumerate(careplan.care_rules, 1):
                careplan_text += f"""
{i}. {rule.problem_title}
   Beschrijving: {rule.problem_description}
   Doel: {rule.goal}
   Acties:
"""
                for j, action in enumerate(rule.actions, 1):
                    careplan_text += f"   - {action}\n"

            if careplan.specialist_advice:
                careplan_text += "\nSpecialistische adviezen:\n"
                for advice in careplan.specialist_advice:
                    careplan_text += f"""
{advice.specialist_type}:
   Beoordeling: {advice.assessment}
   Aanbeveling: {advice.recommendation}
"""

            careplan_text += f"\nConclusie: {careplan.conclusion}"

            result = await Runner.run(email_agent, careplan_text)
            print("Email verzonden")
        except Exception as e:
            print(f"Fout bij email verzenden: {e}")
