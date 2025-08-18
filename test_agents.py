#!/usr/bin/env python3
"""
Test script to verify that agents can be imported and initialized correctly.
"""
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def test_agent_imports():
    """Test that all agents can be imported and initialized."""
    print("🤖 Testing Agent Imports and Initialization")
    print("=" * 50)
    
    try:
        # Test individual agent imports
        print("📥 Importing problem identification agent...")
        from app.careplan_agents.problem_identification import problem_identification_agent
        print(f"✅ Problem identification agent: {problem_identification_agent.name}")
        
        print("📥 Importing care plan agent...")
        from app.careplan_agents.care_plan import care_plan_agent
        print(f"✅ Care plan agent: {care_plan_agent.name}")
        
        print("📥 Importing specialist agents...")
        from app.careplan_agents.specialist import dietist_agent, fysio_agent
        print(f"✅ Dietist agent: {dietist_agent.name}")
        print(f"✅ Fysio agent: {fysio_agent.name}")
        
        print("📥 Importing format agent...")
        from app.careplan_agents.format import format_agent
        print(f"✅ Format agent: {format_agent.name}")
        
        print("📥 Importing email agent...")
        from app.careplan_agents.email_agent import email_agent
        print(f"✅ Email agent: {email_agent.name}")
        
        # Test collective import
        print("\n📦 Testing collective import...")
        from app.careplan_agents import (
            problem_identification_agent as pi_agent,
            care_plan_agent as cp_agent,
            dietist_agent as d_agent,
            fysio_agent as f_agent,
            format_agent as fmt_agent,
            email_agent as e_agent
        )
        print("✅ Collective import successful")
        
        print("\n🎉 All agent imports successful! Configuration is working.")
        print(f"🔧 Using Azure OpenAI: {hasattr(pi_agent.model, 'openai_client')}")
        
    except Exception as e:
        print(f"\n❌ Error importing agents: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_agent_imports()
