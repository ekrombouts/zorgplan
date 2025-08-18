"""
Agents module - Bevat alle gespecialiseerde AI agents.
"""

from .care_plan import care_plan_agent
from .problem_identification import problem_identification_agent
from .specialist import dietist_agent, fysio_agent
from .format import format_agent
from .email import email_agent

__all__ = [
    'care_plan_agent',
    'problem_identification_agent', 
    'dietist_agent',
    'fysio_agent',
    'format_agent',
    'email_agent'
]
