import gradio as gr
import pandas as pd

# ZPL label generation function
def small_label(rack_number, plastic_bottle1, plastic_bottle2):
    # Only convert to int if the string is not empty
    bottle1 = str(int(plastic_bottle1)) if plastic_bottle1.strip() else ''
    bottle2 = str(int(plastic_bottle2)) if plastic_bottle2.strip() else ''
    
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
^FPH,3^FT202,183^A0B,34,33^FB183,1,9,C^FH\\^CI28^FD{bottle1}\\5C&^FS^CI27
^FPH,3^FT268,182^A0B,34,33^FB182,1,9,C^FH\\^CI28^FD{rack_number}\\5C&^FS^CI27
^FO221,0^GFA,53,2928,16,:Z64:eJztx6EBAAAIA6AFD9/pVg8wQqM5Jqm7u7u7u799AZcGXl0=:6E3C
^FPH,3^FT311,183^A0B,34,33^FB183,1,9,C^FH\\^CI28^FD{bottle2}\\5C&^FS^CI27
^PQ1,0,1,Y
^XZ
    '''

# Label generation from pasted text
def generate_labels_from_text(sticker_text, rack_number):
    try:
        stickers = [line.strip() for line in sticker_text.strip().splitlines() if line.strip()]
        output = ""
        n = len(stickers)

        # Loop over every 2 items
        for i in range(0, n, 2):
            bottle1 = stickers[i]
            bottle2 = stickers[i + 1] if i + 1 < n else ''  # blank if odd
            output += small_label(rack_number, bottle1, bottle2) + "\n"

        return output.strip()
    except Exception as e:
        return f"Error generating labels: {e}"

# Gradio UI
with gr.Blocks() as demo:
    with gr.Row():
        gr.Image("logo.png", elem_id="logo", show_label=False, scale=0)

    gr.Markdown("""
    
    # ICBA Genebank - Small Location Labels Generator

    **Introduction:**  
    - This tool generates ZPL code for 2 small location labels per 2x1 inch sticker.

    **Instructions:**  
    - Paste your list of bottle numbers below, one per line.
    - Enter the correct Rack number.
    - Click "Generate Labels" to get the ZPL code for printing.

    **Example Input:**  
    ```
    1001
    1002
    1003
    1004
    ```
    """)

    with gr.Row():
        sticker_input = gr.Textbox(label="Paste Bottle IDs (One per line)", lines=10, placeholder="e.g.,\n1001\n1002\n1003")
        rack_input = gr.Textbox(label="Enter Rack Number", placeholder="e.g., A020104")

    generate_btn = gr.Button("Generate Labels")
    output = gr.Textbox(label="ZPL Output", lines=20)

    generate_btn.click(fn=generate_labels_from_text, inputs=[sticker_input, rack_input], outputs=output)

    gr.Markdown("""
    **Developed by:**  
    Mohamed Irfan, International Center for Biosaline Agriculture
    """)

demo.launch()
