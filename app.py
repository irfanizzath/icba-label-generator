import gradio as gr

# --- ZPL Label Functions ---

# 1. Location Label Function (with Rack Number)
def location_label(rack_number, plastic_bottle1, plastic_bottle2):
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

# 2. Eppendorf Label Function
def eppendorf_label(plastic_bottle1, plastic_bottle2):
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
^FO112,0^GFA,53,2928,16,:Z64:eJztx6EBAAAIA6AFD9/pVg8wQqM5Jqm7u7u7u799AZcGXl0=:6E3C
^FPH,3^FT182,183^A0B,50,50^FB183,1,9,C^FH\\^CI28^FD{bottle1}\\5C&^FS^CI27
^FO221,0^GFA,53,2928,16,:Z64:eJztx6EBAAAIA6AFD9/pVg8wQqM5Jqm7u7u7u799AZcGXl0=:6E3C
^FPH,3^FT291,183^A0B,50,50^FB183,1,9,C^FH\\^CI28^FD{bottle2}\\5C&^FS^CI27
^PQ1,0,1,Y
^XZ
'''

# --- Main Label Generators ---
def generate_location_labels(sticker_text, rack_number):
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
            output += location_label(rack_number, l, r) + "\n"

        return output.strip()
    except Exception as e:
        return f"Error generating labels: {e}"

def generate_eppendorf_labels_range(first_tube, last_tube):
    try:
        first = int(first_tube)
        last = int(last_tube)
        if first > last:
            return "First tube number must be less than or equal to last tube number."

        stickers = [str(i) for i in range(first, last + 1)]
        n = len(stickers)
        mid = (n + 1) // 2
        left = stickers[:mid]
        right = stickers[mid:]

        output = ""
        for i in range(mid):
            l = left[i]
            r = right[i] if i < len(right) else ''
            output += eppendorf_label(l, r) + "\n"

        return output.strip()
    except Exception as e:
        return f"Error generating Eppendorf labels: {e}"

# --- Gradio UI ---
with gr.Blocks() as demo:
    with gr.Row():
        gr.Image("logo.png", elem_id="logo", show_label=False, height=120, width=300)

    gr.Markdown("""
    # ICBA Genebank - Labels Generator Tool
    **Instructions for Location Labelling:**  
    - Paste your list of bottle numbers below (one per line).
    - Enter the Rack number.
    - Click "Generate Labels" to get ZPL code for printing.
    """)

    mode = gr.Radio(["Location Labels", "Eppendorf Labels"], label="Choose Label Type", value="Location Labels")
    
    # Shared
    sticker_input = gr.Textbox(label="Paste Bottle IDs", lines=10, visible=True)
    rack_input = gr.Textbox(label="Enter Rack Number", placeholder="e.g., A020104", visible=True)
    
    # New Inputs for Eppendorf Range
    first_tube = gr.Textbox(label="First Tube Number", placeholder="e.g., 1", visible=False)
    last_tube = gr.Textbox(label="Last Tube Number", placeholder="e.g., 46", visible=False)
    
    # Update visibility based on mode
    def update_visibility(mode):
        return {
            sticker_input: gr.update(visible=(mode == "Location Labels")),
            rack_input: gr.update(visible=(mode == "Location Labels")),
            first_tube: gr.update(visible=(mode == "Eppendorf Labels")),
            last_tube: gr.update(visible=(mode == "Eppendorf Labels")),
        }
    
    mode.change(fn=update_visibility, inputs=mode, outputs=[sticker_input, rack_input, first_tube, last_tube])

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

    def generate_by_mode(mode, bottles, rack, first, last):
        if mode == "Location Labels":
            return generate_location_labels(bottles, rack)
        else:
            return generate_eppendorf_labels_range(first, last)
    
    generate_btn.click(fn=generate_by_mode,
                       inputs=[mode, sticker_input, rack_input, first_tube, last_tube],
                       outputs=output)

    gr.Markdown("""
    **Developed by:**  
    Mohamed Irfan, International Center for Biosaline Agriculture
    """)

demo.launch()
