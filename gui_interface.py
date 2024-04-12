import gradio as gr
from gradio_pdf import PDF

with gr.Blocks() as demo:
  dataset_file = gr.File(label = "Upload Dataset File Here", )

  output_PDF_path = "./Fig5.pdf"
  PDF(output_PDF_path, label = "PDF")
demo.launch()
