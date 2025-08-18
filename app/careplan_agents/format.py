from app.models import CompleteCareplan


def format_careplan_to_markdown(careplan: CompleteCareplan) -> str:
    """
    Formatteert een zorgplan naar een professionele markdown presentatie.
    
    Args:
        careplan: Het complete zorgplan object
        
    Returns:
        str: Geformatteerde markdown string
    """
    markdown_output = []
    
    # Header
    markdown_output.append("# Zorgplan")
    markdown_output.append("")
        
    for i, rule in enumerate(careplan.careplan_items, 1):
        markdown_output.append(f"### {i}. {rule.problem_title}")
        markdown_output.append("")
        markdown_output.append(f"**Beschrijving:** {rule.problem_description}")
        markdown_output.append("")
        markdown_output.append(f"**Doel:** {rule.goal}")
        markdown_output.append("")
        markdown_output.append("**Acties:**")
        for action in rule.actions:
            markdown_output.append(f"- {action}")
        markdown_output.append("")
    
    # Specialistische adviezen sectie (indien aanwezig)
    if careplan.specialist_advice:
        markdown_output.append("## Specialistische Adviezen")
        markdown_output.append("")
        
        for advice in careplan.specialist_advice:
            markdown_output.append(f"### {advice.specialist_type}")
            markdown_output.append("")
            markdown_output.append(f"**Beoordeling:** {advice.assessment}")
            markdown_output.append("")
            markdown_output.append(f"**Aanbeveling:** {advice.recommendation}")
            markdown_output.append("")
    
    # Footer
    markdown_output.append("---")
    markdown_output.append("*Dit zorgplan is automatisch gegenereerd en dient te worden beoordeeld door het zorgteam.*")
    
    return "\n".join(markdown_output)
