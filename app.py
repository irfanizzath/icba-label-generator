import gradio as gr

# ZPL label generation function
def small_label(rack_number, plastic_bottle1, plastic_bottle2):
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
        stickers = sorted([line.strip() for line in sticker_text.strip().splitlines() if line.strip()])
        n = len(stickers)
        mid = (n + 1) // 2
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
    This tool generates ZPL code for 2 small location labels per 2x1 inch sticker.

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
        output = gr.Textbox(label="ZPL Output", lines=20, interactive=False, elem_id="zpl-output-box")
        copy_btn = gr.Button("Copy to Clipboard", elem_id="copy-btn")

        gr.HTML("""
        <script>
        document.addEventListener("DOMContentLoaded", function () {
            const copyBtn = document.getElementById("copy-btn");
            copyBtn.addEventListener("click", async function () {
                const textarea = document.querySelector('#zpl-output-box textarea');
                if (textarea) {
                    try {
                        await navigator.clipboard.writeText(textarea.value);
                        alert("ZPL code copied to clipboard!");
                    } catch (err) {
                        alert("Failed to copy: " + err);
                    }
                } else {
                    alert("Output textarea not found!");
                }
            });
        });
        </script>
        """)

    generate_btn.click(fn=generate_labels_from_text, inputs=[sticker_input, rack_input], outputs=output)

    gr.Markdown("""
    **Developed by:**  
    Mohamed Irfan, International Center for Biosaline Agriculture
    """)

demo.launch()
