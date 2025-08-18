"""
Entry point voor de Zorgplan applicatie.
"""

from app.careplan_app import ui


def main():
    """Start de Gradio applicatie"""
    print("Zorgplan applicatie starten...")
    ui.launch(inbrowser=True)


if __name__ == "__main__":
    main()
