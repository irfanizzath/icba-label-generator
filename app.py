import gradio as gr
import pandas as pd

# HTML Header with ICBA logo and title
def header_html():
    return """
    <div style="display: flex; align-items: center; gap: 20px;">
        <a href="https://www.biosaline.org/" target="_blank">
            <img src="file/logo.png" alt="ICBA Logo" style="height: 80px;">
        </a>
        <h1 style="font-size: 28px; margin: 0;">Genebank Label Generator</h1>
    </div>
    """

# ZPL label format generator
def small_label(rack_number, plastic_bottle1, plastic_bottle2):
    return f'''
    CT~~CD,~CC^~CT~
^XA
~TA000
~JSN
^LT0
^MNW
^MTT
^PON
^PMN
^LH0,0
^JMA
^PR4,4
~SD15
^JUS
^LRN
^CI27
^PA0,1,1,0
^XZ
^XA
^MMT
^PW386
^LL183
^LS0
^FPH,3^FT159,182^A0B,34,33^FB182,1,9,C^FH\\^CI28^FD{rack_number}\\5C&^FS^CI27
^FO112,0^GFA,53,2928,16,:Z64:eJztx6EBAAAIA6AFD9/pVg8wQqM5Jqm7u7u7u799AZcGXl0=:6E3C
^FPH,3^FT202,183^A0B,34,33^FB183,1,9,C^FH\\^CI28^FD{int(plastic_bottle1)}\\5C&^FS^CI27
^FPH,3^FT268,182^A0B,34,33^FB182,1,9,C^FH\\^CI28^FD{rack_number}\\5C&^FS^CI27
^FO221,0^GFA,53,2928,16,:Z64:eJztx6EBAAAIA6AFD9/pVg8wQqM5Jqm7u7u7u799AZcGXl0=:6E3C
^FPH,3^FT311,183^A0B,34,33^FB183,1,9,C^FH\\^CI28^FD{int(plastic_bottle2)}\\5C&^FS^CI27
^PQ1,0,1,Y
^XZ
    '''

# Function to read file and generate label output
def generate_labels(file, rack_number):
    try:
        df = pd.read_excel(file.name)
    except Exception as e:
        return f"Error reading Excel file: {e}"

    try:
        stickers = df['Sticker'].dropna().tolist()
        output = ""
        n = len(stickers)
        mid = n // 2
        for i in range(mid):
            output += small_label(rack_number, stickers[i], stickers[i + mid]) + "\n"
        if n % 2 != 0:
            output += small_label(rack_number, 0, stickers[-1])
        return output.strip()
    except Exception as e:
        return f"Error generating labels: {e}"

# Gradio UI
with gr.Blocks() as demo:
    gr.HTML(header_html())
    
    gr.Markdown("""
    **Instructions:**  
    - Upload `.xlsx` file with list of locations in a column named `Sticker`.  
    - Check the [sample file here](file/Bottle_Location.xlsx) for correct format.
    """)
    
    with gr.Row():
        file = gr.File(label="Upload Excel File (.xlsx)", file_types=[".xlsx"])
        rack_input = gr.Textbox(label="Enter Rack Number", placeholder="e.g., A020104")
    
    generate_btn = gr.Button("Generate Labels")
    output = gr.Textbox(label="ZPL Output", lines=20)
    
    generate_btn.click(fn=generate_labels, inputs=[file, rack_input], outputs=output)

demo.launch()

