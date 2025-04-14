import gradio as gr
from rag_explainer import explain_medical_term

#Interface Wrapper
def chatbot_interface(user_input):
    try:
        result = explain_medical_term(user_input)
        return f"**Explanation:**\n{result['explanation']}\n\n**Model:** {result['model']}\n\n**Sources Used:**\n" + "\n".join(f"- {src}" for src in result["context_used"])
    except Exception as e:
        return f"Error: {e}"

#Launch Gradio App
with gr.Blocks(title="Patient Education Bot") as demo:
    gr.Markdown("""
    #Patient Education Bot
    Enter a medical term or lab result related to kidney health (e.g., "GFR 45", "BUN high", "what is dialysis?")
    """)
    with gr.Row():
        input_box = gr.Textbox(label="Enter your medical query", placeholder="e.g. My creatinine is 2.0")
    output_box = gr.Markdown(label="Explanation")
    button = gr.Button("Explain")

    button.click(fn=chatbot_interface, inputs=input_box, outputs=output_box)

if __name__ == "__main__":
    demo.launch()