# Digit Detective — local model lesson

**50-minute lesson • English • Windows / Mac / iPad**

Every prediction runs on the student's own device. The weights and sample images are bundled. There is no hosted model, teacher server, API key, login or first-run weight download. Desktop Gradio opens a browser page on **127.0.0.1**, which means this same computer. Do not use `share=True`.

## Folder contents

- `desktop_starter.py` / `desktop_solution.py`: student and teacher versions for Windows/Mac.
- `ipad_starter.ipynb` / `ipad_solution.ipynb`: corresponding Carnets notebooks.
- `shared/model.npz`: trained neural-network weights. Keep this file.
- `shared/digit_model.py`: provided NumPy/Pillow prediction code.
- `shared/lesson_ui.py`: provided desktop and notebook interfaces.
- `shared/samples/`: bundled handwriting examples.
- `MODEL_CARD.md` or `shared/MODEL_CARD.md`: training, evaluation and limitations.
- `TEACHER_NOTES.md`: timings, code answers, recovery route and device checklist.

**Extract the whole ZIP first. Keep each program/notebook next to `shared`.** Do not run a file from inside the ZIP.

## Before class — Windows

Python and VS Code are already part of the course setup. An adult should complete package installation while internet is available:

1. Open this extracted folder in VS Code: **File → Open Folder**.
2. Open **Terminal → New Terminal**. Make sure it is in this folder.
3. Run:

```powershell
py -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements-desktop.txt
```

4. In VS Code select `.venv` through **Python: Select Interpreter**. Do not change a working system installation or repair PATH during class.
5. Test the teacher version:

```powershell
.\.venv\Scripts\python desktop_solution.py
```

If `py` is unavailable but `python --version` identifies the working course Python, use `python -m venv .venv`. If neither works, ask an adult to check the existing installation; do not start reinstalling blindly.

## Before class — Mac

1. Open this extracted folder in VS Code.
2. Open **Terminal → New Terminal**.
3. Run:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-desktop.txt
```

4. Select the `.venv` interpreter in VS Code.
5. Test:

```bash
.venv/bin/python desktop_solution.py
```

The desktop requirements need internet **during preparation only**. Once installed, prediction does not need internet. This is not a claim that a new computer can install Python packages without internet.

## In class — desktop

Use the same command but change `desktop_solution.py` to `desktop_starter.py`. Use the browser on that same computer. If it does not open automatically, open `http://127.0.0.1:7860`.

After editing: save the file; stop the old server with **Ctrl+C in VS Code's terminal**; rerun the command; refresh the browser. The model runs only when you click **Predict**. The unfinished starter deliberately shows a TODO message.

## Before class — iPad / Carnets

1. Install the normal **Carnets — Jupyter** app. This lesson uses NumPy, Pillow and ipywidgets; it does not need the separate SciPy edition.
2. Save the whole ZIP to Files, then extract it into **On My iPad**. Download all files fully; do not leave cloud-only placeholders.
3. In Carnets open `ipad_starter.ipynb` from that folder. The notebook must remain beside `shared`.
4. Run the setup cell. Then run the function cell and interface cell, in that order.
5. Pick a bundled image and click **Predict**. Edit the same three TODO lines as the desktop students.
6. After edits rerun the function cell, **then rerun the interface cell**. This recreates buttons with the new function.
7. Save using the notebook Save control. Reopen and rerun the cells to restore the interface.

For a personal image, save one black digit on white as PNG/JPEG to Files and use **Upload image**. The uploaded image overrides the sample menu until **Use sample again** is clicked. The model may misread unfamiliar handwriting. Sample selection alone does not invoke prediction.

No desktop Gradio server runs on the iPad. Carnets executes the same `recognise` function and bundled neural network locally, with a supplied notebook interface instead.

## Offline rehearsal

Before the lesson, fully install packages and download/extract files. Disable Wi-Fi, close and reopen the program, and classify three bundled images. Repeat in the actual classroom iPad. Testing a Jupyter kernel elsewhere is **not** a physical Carnets/Safari test.

## Safety and privacy

Use bundled digit pictures or drawings, not children’s faces or documents. Images stay in the local app during inference; notebooks can retain uploaded data or outputs when saved, so clear personal outputs before sharing. The desktop is bound to loopback and public sharing is disabled.

## Troubleshooting

- `No module named ...`: desktop dependencies may have been installed in a different interpreter. Use the exact `.venv` command above. On iPad use Carnets, not a different Python app.
- `shared` or `model.npz` missing: extract the entire folder; keep the notebook/program beside `shared`.
- Port 7860 already in use: stop your previous copy with Ctrl+C. Do not terminate unrelated processes.
- Your change is invisible: desktop — save, stop, restart, refresh; iPad — rerun function then interface cells.
- TODO message: the starter is intentionally unfinished. Complete Step 1 first.
- Blank / no-ink message: choose a digit picture rather than a blank image.
- Unexpected result: center one upright digit on a plain background. A model score is not a promise of correctness.

## Optional verification tools

The runtime needs no training packages. Teacher-only tests use `requirements-test.txt` and `pytest tests -q`. Training scripts, if included under `teacher_tools`, require their separate training dependencies and internet for the original dataset. They are **not** lesson launch steps.
