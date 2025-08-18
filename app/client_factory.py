"""
Client factory for creating OpenAI clients based on configuration.
"""
from typing import Union
from openai import AsyncOpenAI, AsyncAzureOpenAI
from agents import set_default_openai_client, set_tracing_disabled, OpenAIChatCompletionsModel

from .settings import settings


def create_openai_client() -> Union[AsyncOpenAI, AsyncAzureOpenAI]:
    """
    Create the appropriate OpenAI client based on configuration.
    
    Returns:
        AsyncOpenAI or AsyncAzureOpenAI client instance
        
    Raises:
        ValueError: If configuration is invalid
    """
    if settings.USE_AZURE_OPENAI:
        if not settings.validate_azure_config():
            raise ValueError(
                "Azure OpenAI is enabled but configuration is incomplete. "
                "Please check AZURE_OPENAI_API_KEY, AZURE_OPENAI_API_VERSION, "
                "AZURE_OPENAI_ENDPOINT, and AZURE_OPENAI_DEPLOYMENT environment variables."
            )
        
        return AsyncAzureOpenAI(
            api_key=settings.AZURE_OPENAI_API_KEY,  # type: ignore
            api_version=settings.AZURE_OPENAI_API_VERSION,  # type: ignore
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,  # type: ignore
            azure_deployment=settings.AZURE_OPENAI_DEPLOYMENT  # type: ignore
        )
    else:
        if not settings.validate_openai_config():
            raise ValueError(
                "OpenAI API key is required when not using Azure OpenAI. "
                "Please set OPENAI_API_KEY environment variable."
            )
        
        return AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


def setup_global_client():
    """
    Set up the global OpenAI client and tracing configuration.
    This should be called once at application startup.
    """
    client = create_openai_client()
    set_default_openai_client(client)
    
    if settings.DISABLE_TRACING:
        set_tracing_disabled(disabled=True)


def create_model(model_name: str = None) -> OpenAIChatCompletionsModel:  # type: ignore
    """
    Create an OpenAIChatCompletionsModel with the configured client.
    
    Args:
        model_name: Override the default model name
        
    Returns:
        Configured OpenAIChatCompletionsModel instance
    """
    client = create_openai_client()
    
    if model_name is None:
        model_name = settings.AZURE_MODEL if settings.USE_AZURE_OPENAI else settings.DEFAULT_MODEL
    
    return OpenAIChatCompletionsModel(
        model=model_name,
        openai_client=client
    )
