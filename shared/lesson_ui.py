"""Provided local interfaces; students edit recognise(), not this file."""
from io import BytesIO
from pathlib import Path
import os

os.environ.setdefault('GRADIO_ANALYTICS_ENABLED', 'False')
HERE = Path(__file__).resolve().parent


def uploaded_image(value):
    """Accept both ipywidgets 7 and 8 FileUpload representations."""
    from PIL import Image, ImageOps
    if not value:
        return None
    files = list(value.values()) if isinstance(value, dict) else list(value)
    with Image.open(BytesIO(bytes(files[0]['content']))) as image:
        return ImageOps.exif_transpose(image).convert('RGB').copy()


def make_desktop(callback):
    import gradio as gr
    samples = sorted((HERE / 'samples').glob('*.png'))
    with gr.Blocks(title='Digit Detective', analytics_enabled=False) as demo:
        gr.Markdown('# Digit Detective\n### Your picture. Your model. Your computer.\nChoose a bundled example or upload one digit. Then click **Predict**.')
        with gr.Row():
            image = gr.Image(type='pil', height=280, elem_id='digit-input', image_mode='RGB', sources=['upload', 'clipboard'], label='One handwritten digit', value=str(samples[0]) if samples else None)
            with gr.Column():
                button = gr.Button('Predict', variant='primary')
                message = gr.Textbox(label='Result', interactive=False)
                scores = gr.Label(label='Model scores — not a guarantee', num_top_classes=3)
        if samples:
            gr.Examples(examples=[[str(p)] for p in samples], inputs=[image], label='Bundled examples — click a picture, then Predict', examples_per_page=10)
        button.click(callback, inputs=[image], outputs=[message, scores], api_name='recognise')
        gr.Markdown('Runs locally. No account, API key or model download.\n\nA high model score can still be wrong. This model recognises digits, not words or objects.')
    return demo


def launch_desktop(callback):
    # The browser opens on this same device, not on a remote server.
    demo = make_desktop(callback)
    demo.launch(server_name='127.0.0.1', server_port=7860, share=False,
                inbrowser=True, show_error=True, footer_links=[], run_history=False,
                css='#digit-input img {width: 100% !important; height: 100% !important; object-fit: contain; image-rendering: pixelated;}',
                theme=__import__('gradio').themes.Base(font=['Arial', 'sans-serif'], font_mono=['Consolas', 'monospace']))


def show_notebook(callback):
    """Local widget interface. No hosted JavaScript, HTTP API or remote model."""
    import ipywidgets as widgets
    from IPython.display import display, clear_output
    from PIL import Image
    samples = sorted((HERE / 'samples').glob('*.png'))
    if not samples:
        raise FileNotFoundError('Keep the shared/samples folder with this notebook.')
    picker = widgets.Dropdown(options=[(f'Sample {index:02d}', str(p)) for index,p in enumerate(samples,1)], description='Sample:')
    upload = widgets.FileUpload(accept='.png,.jpg,.jpeg', multiple=False, description='Upload image')
    preview = widgets.Image(format='png', width=168, height=168)
    button = widgets.Button(description='Predict', button_style='primary')
    reset = widgets.Button(description='Use sample again')
    output = widgets.Output()

    def selected_image():
        image = uploaded_image(upload.value)
        if image is None:
            with Image.open(picker.value) as source:
                image = source.convert('RGB').copy()
        return image

    def update_preview(change=None):
        # Local preview only: never call the prediction callback here.
        try:
            image = selected_image()
            stream = BytesIO()
            image.resize((168, 168)).save(stream, format='PNG')
            preview.value = stream.getvalue()
        except (ValueError, OSError) as error:
            preview.value = b''
            with output:
                clear_output(wait=True)
                print(f'Please choose a PNG or JPEG picture. {error}')

    def show_result(_):
        with output:
            clear_output(wait=True)
            try:
                image = selected_image()
                message, scores = callback(image)
                print(message)
                if scores:
                    for digit in sorted(scores, key=scores.get, reverse=True)[:3]:
                        print(f'{digit}: {scores[digit]:.0%}')
            except (ValueError, OSError) as error:
                print(f'Please choose a PNG or JPEG picture of one digit. {error}')

    def clear_upload(_):
        upload.value = {} if isinstance(upload.value, dict) else ()
        if hasattr(upload, '_counter'):
            upload._counter = 0
        with output:
            clear_output(wait=True)
            print('Upload cleared. Choose a sample and click Predict.')

    button.on_click(show_result)
    reset.on_click(clear_upload)
    picker.observe(update_preview, names='value')
    upload.observe(update_preview, names='value')
    update_preview()
    display(widgets.VBox([picker, upload, preview,
        widgets.HTML('Look at the picture and make your own guess. Click <b>Predict</b> to update the result.'),
        widgets.HBox([button, reset]), output]))
    # Returning handles allows actual kernel tests to exercise the buttons.
    return {'picker': picker, 'upload': upload, 'predict': button,
            'reset': reset, 'output': output, 'preview': preview}
