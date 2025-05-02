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
        n = len(stickers)
        mid = (n + 1) // 2  # ensures extra item goes to left side if odd
        left = stickers[:mid]
        right = stickers[mid:]

        output = ""
        for i in range(mid):
            l = left[i]
            r = right[i] if i < len(right) else ''
            output += small_label(rack_number, l, r) + "\n"

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

    with gr.Column(elem_id="zpl-output"):
        output = gr.Textbox(label="ZPL Output", lines=20)

        gr.HTML("""
        <style>
        .copy-button {
            background: none;
            border: none;
            cursor: pointer;
            position: absolute;
            top: 8px;
            right: 8px;
            padding: 5px;
            opacity: 0.6;
        }

        .copy-button:hover {
            opacity: 1;
        }

        .copy-icon {
            width: 20px;
            height: 20px;
            fill: #4a4a4a;
        }

        .copy-wrapper {
            position: relative;
        }
        </style>

        <script>
        function copyToClipboardIcon() {
            const text = document.querySelector('#zpl-output textarea');
            text.select();
            document.execCommand('copy');

            const btn = document.getElementById('copy-btn');
            const original = btn.innerHTML;
            btn.innerHTML = '✅';
            setTimeout(() => btn.innerHTML = original, 1000);
        }
        </script>

        <div class="copy-wrapper">
            <button class="copy-button" onclick="copyToClipboardIcon()" id="copy-btn" title="Copy to Clipboard">
                <svg class="copy-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                    <path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v16h14c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 18H8V7h11v16z"/>
                </svg>
            </button>
        </div>
        """)

    generate_btn.click(fn=generate_labels_from_text, inputs=[sticker_input, rack_input], outputs=output)

    gr.Markdown("""
    **Developed by:**  
    Mohamed Irfan, International Center for Biosaline Agriculture
    """)

demo.launch()
