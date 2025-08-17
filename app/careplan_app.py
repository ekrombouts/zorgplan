import gradio as gr
from dotenv import load_dotenv
from app.careplan_manager import CareplanManager
import os

load_dotenv(override=True)


async def process_careplan(file):
    """Verwerk het geüploade clientdossier en genereer een zorgplan"""
    if file is None:
        yield "Geen bestand geüpload. Upload alstublieft een clientdossier."
        return

    try:
        # Lees de inhoud van het bestand
        # File is al bytes van Gradio, dus direct decoderen
        if isinstance(file, bytes):
            file_content = file.decode("utf-8")
        else:
            # Als het een file object is
            file_content = file.read().decode("utf-8")

        # Start het zorgplan proces
        manager = CareplanManager()
        async for update in manager.run(file_content):
            yield update

    except Exception as e:
        yield f"Fout bij verwerken van het dossier: {str(e)}"


# Gradio interface
with gr.Blocks() as ui:
    gr.Markdown(
        """
    # 🏥 Automatische Zorgplan Generatie
    
    Upload een clientdossier (.txt) om automatisch een zorgplan te genereren.
    
    Het systeem:
    - Identificeert de drie belangrijkste zorgproblemen
    - Stelt voor elk probleem een zorgplanregel op
    - Vraagt specialistische adviezen op waar nodig (diëtist/fysiotherapeut)
    - Genereert een volledig zorgplan en verstuurt dit per email
    """
    )

    with gr.Row():
        with gr.Column():
            file_input = gr.File(
                label="Upload Clientdossier (.txt)", file_types=[".txt"], type="binary"
            )
            process_button = gr.Button("Genereer Zorgplan", variant="primary")

        with gr.Column():
            output_display = gr.Markdown(
                label="Zorgplan Output",
                value="Upload een clientdossier en klik op 'Genereer Zorgplan' om te beginnen.",
            )

    # Event handlers
    process_button.click(fn=process_careplan, inputs=file_input, outputs=output_display)

    # Ook Enter in file upload
    file_input.upload(fn=process_careplan, inputs=file_input, outputs=output_display)

if __name__ == "__main__":
    ui.launch(inbrowser=True)
