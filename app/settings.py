import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings:
    """Centralized configuration for the zorgplan application."""
    
    # OpenAI Configuration
    USE_AZURE_OPENAI: bool = os.getenv("USE_AZURE_OPENAI", "false").lower() == "true"
    DISABLE_TRACING: bool = os.getenv("DISABLE_TRACING", "true").lower() == "true"
    
    # Azure OpenAI Configuration
    AZURE_OPENAI_API_KEY: Optional[str] = os.getenv("AZURE_OPENAI_API_KEY")
    AZURE_OPENAI_API_VERSION: Optional[str] = os.getenv("AZURE_OPENAI_API_VERSION")
    AZURE_OPENAI_ENDPOINT: Optional[str] = os.getenv("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_DEPLOYMENT: Optional[str] = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    
    # Regular OpenAI Configuration (fallback)
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    
    # Default model configurations
    DEFAULT_MODEL: str = os.getenv("DEFAULT_MODEL", "gpt-4o-mini")
    AZURE_MODEL: str = os.getenv("AZURE_MODEL", "gpt-4o")
    
    @classmethod
    def validate_azure_config(cls) -> bool:
        """Validate that all required Azure OpenAI configuration is present."""
        if not cls.USE_AZURE_OPENAI:
            return True
            
        required_fields = [
            cls.AZURE_OPENAI_API_KEY,
            cls.AZURE_OPENAI_API_VERSION,
            cls.AZURE_OPENAI_ENDPOINT,
            cls.AZURE_OPENAI_DEPLOYMENT
        ]
        
        return all(field is not None for field in required_fields)
    
    @classmethod
    def validate_openai_config(cls) -> bool:
        """Validate that OpenAI API key is present when not using Azure."""
        if cls.USE_AZURE_OPENAI:
            return True
        return cls.OPENAI_API_KEY is not None


# Create global settings instance
settings = Settings()
