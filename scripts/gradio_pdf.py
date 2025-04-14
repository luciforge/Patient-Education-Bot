import gradio as gr
from explainer_pdf import explain_medical_term, explain_lab_file

#Text-based Input
def chatbot_interface(user_input):
    try:
        result = explain_medical_term(user_input)
        return f"**Explanation:**\n{result['explanation']}\n\n**Model:** {result['model']}\n\n**Sources Used:**\n" + "\n".join(f"- {src}" for src in result["context_used"])
    except Exception as e:
        return f"Error: {e}"

#File Upload Handler
def file_interface(file):
    try:
        return explain_lab_file(file)
    except Exception as e:
        return f"Error processing file: {e}"

#Gradio UI
with gr.Blocks(title="Patient Education Bot") as demo:
    gr.Markdown("""
    # Patient Education Bot  
    Get plain-language explanations of lab results or medical terms related to kidney health.
    """)

    with gr.Row():
        input_box = gr.Textbox(label="Enter your medical query", placeholder="e.g. My creatinine is 2.0")
    output_box = gr.Markdown(label="Explanation")
    button = gr.Button("Explain")
    button.click(fn=chatbot_interface, inputs=input_box, outputs=output_box)

    gr.Markdown("## Or upload your lab report (.pdf or .txt)")

    with gr.Row():
        file_input = gr.File(label="Upload File", file_types=[".pdf", ".txt"])
    file_output = gr.Markdown(label="File Analysis")
    file_button = gr.Button("Explain Uploaded Lab Report")
    file_button.click(fn=file_interface, inputs=file_input, outputs=file_output)

if __name__ == "__main__":
    demo.launch()
