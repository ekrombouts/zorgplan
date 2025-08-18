"""
Test om te controleren of alle imports correct werken na de herstructurering.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """Test alle belangrijke imports"""
    try:
        # Test models import
        from app.models import CareProblems, CarePlanItem, SpecialistAdvice, CompleteCareplan
        print("✅ Models import successful")
        
        # Test agents import
        from app.careplan_agents import (
            problem_identification_agent,
            care_plan_agent,
            dietist_agent,
            fysio_agent
        )
        print("✅ Careplan Agents import successful")
        
        # Test manager import
        from app.careplan_manager import CareplanManager
        print("✅ Manager import successful")
        
        # Test app import
        from app.careplan_app import ui
        print("✅ App import successful")
        
        print("\n🎉 Alle imports werken correct!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False


if __name__ == "__main__":
    test_imports()
