#!/usr/bin/env python3
"""
Test script to verify the OpenAI client configuration works correctly.
"""
import os
import sys
import asyncio
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app.settings import settings
from app.client_factory import create_openai_client, setup_global_client, create_model


async def test_configuration():
    """Test the OpenAI client configuration."""
    print("🔧 Testing OpenAI Client Configuration")
    print("=" * 50)
    
    # Display current settings
    print(f"USE_AZURE_OPENAI: {settings.USE_AZURE_OPENAI}")
    print(f"DISABLE_TRACING: {settings.DISABLE_TRACING}")
    print(f"Default Model: {settings.DEFAULT_MODEL}")
    print(f"Azure Model: {settings.AZURE_MODEL}")
    print()
    
    # Test configuration validation
    if settings.USE_AZURE_OPENAI:
        print("🔍 Validating Azure OpenAI configuration...")
        if settings.validate_azure_config():
            print("✅ Azure OpenAI configuration is valid")
        else:
            print("❌ Azure OpenAI configuration is incomplete")
            print("   Missing environment variables:")
            if not settings.AZURE_OPENAI_API_KEY:
                print("   - AZURE_OPENAI_API_KEY")
            if not settings.AZURE_OPENAI_API_VERSION:
                print("   - AZURE_OPENAI_API_VERSION")
            if not settings.AZURE_OPENAI_ENDPOINT:
                print("   - AZURE_OPENAI_ENDPOINT")
            if not settings.AZURE_OPENAI_DEPLOYMENT:
                print("   - AZURE_OPENAI_DEPLOYMENT")
            return
    else:
        print("🔍 Validating OpenAI configuration...")
        if settings.validate_openai_config():
            print("✅ OpenAI configuration is valid")
        else:
            print("❌ OpenAI API key is missing")
            print("   Please set OPENAI_API_KEY environment variable")
            return
    
    # Test client creation
    try:
        print("\n🚀 Creating OpenAI client...")
        client = create_openai_client()
        client_type = "Azure OpenAI" if settings.USE_AZURE_OPENAI else "OpenAI"
        print(f"✅ Successfully created {client_type} client")
        
        # Test global setup
        print("\n🌐 Setting up global client...")
        setup_global_client()
        print("✅ Global client setup completed")
        
        # Test model creation
        print("\n🤖 Creating model...")
        model = create_model()
        print(f"✅ Successfully created model: {model.model}")
        
        print("\n🎉 All tests passed! Configuration is working correctly.")
        
    except Exception as e:
        print(f"\n❌ Error creating client: {e}")
        return


if __name__ == "__main__":
    asyncio.run(test_configuration())
