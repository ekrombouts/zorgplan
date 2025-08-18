#!/usr/bin/env python3
"""
Integratietest voor de aangepaste formatting.
"""

import asyncio
from app.models import CompleteCareplan, CarePlanItem, SpecialistAdvice
from app.careplan_manager import CareplanManager

async def test_integration():
    # Maak test data
    care_items = [
        CarePlanItem(
            problem_title="Test probleem",
            problem_description="Dit is een test beschrijving",
            goal="Test doel",
            actions=["Actie 1", "Actie 2", "Actie 3"]
        )
    ]
    
    specialist_advice = [
        SpecialistAdvice(
            specialist_type="Test Specialist",
            assessment="Test beoordeling",
            recommendation="Test aanbeveling"
        )
    ]
    
    # Maak test zorgplan
    careplan = CompleteCareplan(
        careplan_items=care_items,
        specialist_advice=specialist_advice
    )
    
    # Test de formatting via de manager
    manager = CareplanManager()
    formatted_result = await manager.format_careplan(careplan)
    
    print("=== MANAGER FORMAT TEST ===")
    print(formatted_result)
    print("=== EINDE ===")
    
    # Verifieer dat het markdown bevat
    assert "# 🏥 Zorgplan" in formatted_result
    assert "Test probleem" in formatted_result
    assert "Test Specialist" in formatted_result
    
    print("✅ Alle tests geslaagd!")

if __name__ == "__main__":
    asyncio.run(test_integration())
