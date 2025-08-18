"""
Test script om de configureerbare client setup te testen.
"""
import os
import sys
sys.path.append('/Users/eva/projects/zorgplan')

from app.settings import settings
from app.client_factory import create_openai_client, setup_global_client, create_model


def test_configuration():
    """Test de configuratie instellingen."""
    print("=== Configuratie Test ===")
    print(f"USE_AZURE_OPENAI: {settings.USE_AZURE_OPENAI}")
    print(f"DISABLE_TRACING: {settings.DISABLE_TRACING}")
    print(f"DEFAULT_MODEL: {settings.DEFAULT_MODEL}")
    print(f"AZURE_MODEL: {settings.AZURE_MODEL}")
    
    if settings.USE_AZURE_OPENAI:
        print(f"Azure config valid: {settings.validate_azure_config()}")
        print(f"Azure endpoint configured: {settings.AZURE_OPENAI_ENDPOINT is not None}")
    else:
        print(f"OpenAI config valid: {settings.validate_openai_config()}")
    
    print()


def test_client_creation():
    """Test het maken van OpenAI clients."""
    print("=== Client Creation Test ===")
    try:
        client = create_openai_client()
        print(f"Client created successfully: {type(client).__name__}")
        
        model = create_model()
        print(f"Model created successfully: {type(model).__name__}")
        print(f"Model name: {model.model}")
        
        setup_global_client()
        print("Global client setup completed")
        
    except Exception as e:
        print(f"Error creating client: {e}")
    
    print()


def test_agent_import():
    """Test het importeren van agents."""
    print("=== Agent Import Test ===")
    try:
        from app.careplan_agents.problem_identification import problem_identification_agent
        print("✓ problem_identification_agent imported")
        
        from app.careplan_agents.care_plan import care_plan_agent
        print("✓ care_plan_agent imported")
        
        from app.careplan_agents.specialist import dietist_agent, fysio_agent
        print("✓ specialist agents imported")
        
        from app.careplan_agents.format import format_agent
        print("✓ format_agent imported")
        
        from app.careplan_agents.email_agent import email_agent
        print("✓ email_agent imported")
        
    except Exception as e:
        print(f"✗ Error importing agents: {e}")
    
    print()


if __name__ == "__main__":
    test_configuration()
    test_client_creation()
    test_agent_import()
    print("Test completed!")
