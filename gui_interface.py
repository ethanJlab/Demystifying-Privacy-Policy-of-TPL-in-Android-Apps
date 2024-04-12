import gradio as gr
from gradio_pdf import PDF

with gr.Blocks() as demo:
  dataset_file = gr.File(label = "Upload Dataset File Here")
  display= gr.Textbox(label="Question"), PDF(dataset_file)
demo.launch()
