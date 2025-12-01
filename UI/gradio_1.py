import gradio as gr
from gradio.components import download_button
import pandas as pd
import requests
import tempfile
from pathlib import Path
from uuid import uuid4
import io

def send_tabular(file_in):
    df = pd.read_excel(file_in)
    file = df.to_csv()
    files = {
        'file': ('mold.csv',file,'text/csv')
    }
    result = requests.post('http://api:8000/test3', files=files)
    df['result'] = result.json()['result']
    out_dir = Path(tempfile.mkdtemp(prefix="gradio_csv_"))
    out_path = out_dir / f"processed_{uuid4().hex}.csv"
    bio = io.BytesIO()
    df.to_excel(bio, index=False)
    xlsx_bytes = bio.getvalue()
    out_path.write_bytes(xlsx_bytes)
    
    return gr.update(visible=True, value=str(out_path), label="Download processed CSV")

with gr.Blocks(title="Processed Excel") as demo:
    file_in = gr.File(label="Upload Excel", file_types=[".xls",".xlsx"], file_count="single")
    send_btn = gr.Button("Send to API", variant="primary")
    download_btn = gr.DownloadButton("Download processed CSV", visible=False)

    send_btn.click(
            fn=send_tabular,
            inputs=[file_in],
            outputs=[download_btn],
            api_name="send_tabular"
        )

demo.launch(server_name="0.0.0.0", server_port=8000)