#!/usr/bin/env python3
"""
Test script voor de nieuwe format functie.
"""

from app.models import CompleteCareplan, CarePlanItem, SpecialistAdvice
from app.careplan_agents.format import format_careplan_to_markdown

def test_format():
    # Maak test data
    care_items = [
        CarePlanItem(
            problem_title="Gewichtsverlies",
            problem_description="Bewoner heeft in de afgelopen maand 3 kg verloren",
            goal="Stabilisatie van het gewicht",
            actions=[
                "Dagelijks wegen en registreren",
                "Zie specialistisch advies",
                "Extra tussendoortjes aanbieden"
            ]
        ),
        CarePlanItem(
            problem_title="Valrisico",
            problem_description="Verhoogd valrisico door instabiliteit",
            goal="Voorkomen van vallen",
            actions=[
                "Gebruik van looprek",
                "Antislip sokken dragen",
                "Begeleiding bij transfers"
            ]
        )
    ]
    
    specialist_advice = [
        SpecialistAdvice(
            specialist_type="Diëtist",
            assessment="Bewoner heeft moeite met eten vanwege verminderde eetlust",
            recommendation="Eiwitverrijking van maaltijden en frequente kleine porties"
        )
    ]
    
    # Maak test zorgplan
    careplan = CompleteCareplan(
        careplan_items=care_items,
        specialist_advice=specialist_advice
    )
    
    # Test de formatting
    result = format_careplan_to_markdown(careplan)
    print("=== GEFORMATTEERD ZORGPLAN ===")
    print(result)
    print("=== EINDE ===")
    
    return result

if __name__ == "__main__":
    test_format()
