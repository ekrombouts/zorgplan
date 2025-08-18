from pydantic import BaseModel, Field
from typing import List, Optional


class CareProblems(BaseModel):
    """Model voor de geïdentificeerde zorgproblemen"""

    problems: List["CareProblem"] = Field(
        description="Lijst van de drie belangrijkste zorgproblemen"
    )


class CareProblem(BaseModel):
    """Een specifiek zorgprobleem"""

    title: str = Field(description="Korte, duidelijke titel van het zorgprobleem")
    description: str = Field(description="Korte beschrijving van het probleem")
    reasoning: str = Field(description="Redenering waarom je dit probleem hebt geïdentificeerd")


class CareGoal(BaseModel):
    """Een zorgdoel"""

    goal: str = Field(
        description="Het realistische zorgdoel, aangepast aan de verpleeghuis context"
    )


class CareAction(BaseModel):
    """Een zorgactie"""

    action: str = Field(description="Specifieke actie of interventie")


class CarePlanRule(BaseModel):
    """Een complete zorgplanregel"""

    problem_title: str = Field(description="Titel van het zorgprobleem")
    problem_description: str = Field(description="Beschrijving van het zorgprobleem")
    goal: str = Field(description="Het zorgdoel")
    actions: List[str] = Field(description="Lijst van drie acties")


class SpecialistAdvice(BaseModel):
    """Advies van een specialist"""

    specialist_type: str = Field(
        description="Type specialist (dietist of fysiotherapeut)"
    )
    assessment: str = Field(description="Beoordeling van de situatie")
    recommendation: str = Field(description="Specifieke aanbeveling")


class CompleteCareplan(BaseModel):
    """Het complete zorgplan"""

    patient_summary: str = Field(
        description="Korte samenvatting van de patiëntsituatie"
    )
    care_rules: List[CarePlanRule] = Field(description="Lijst van zorgplanregels")
    specialist_advice: List[SpecialistAdvice] = Field(
        description="Eventuele specialistische adviezen"
    )
    conclusion: str = Field(description="Afsluitende opmerking over het zorgplan")
