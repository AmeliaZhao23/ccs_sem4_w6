# Local MNIST digit model

## Origin and scope

Educational digit recognition, not a general handwriting/letter recognizer. Runtime inference uses only NumPy and Pillow, bundled `model.npz`, and no network or scikit-learn. Weights were genuinely trained from scratch on MNIST, not generated or hand-coded.

Dataset download: https://storage.googleapis.com/tensorflow/tf-keras-datasets/mnist.npz
Original MNIST description: https://yann.lecun.org/exdb/mnist/
MNIST creators: Yann LeCun, Corinna Cortes, Christopher J. C. Burges; derived from NIST handwritten-digit data.
Dataset SHA-256: `731c5ac602752760c8e48fbffcf8c3b850d9dc2a2aedcf2cc48468fc17b673d1`.

**Rights notice:** MNIST dataset rights are distinct from the licenses of Keras, NumPy, scikit-learn, and this project's code. No permissive dataset license is asserted here. The downloaded NPZ contains no accompanying license grant; verify original MNIST/NIST terms for your intended redistribution/use. Bundled samples are actual MNIST test images, not newly authored artwork. This card does not grant rights to the underlying data or claim a separately verified license for trained weights.

## Architecture and training

784 inputs -> dense 64 ReLU -> dense 10 -> numerically stable softmax. Inputs are flattened grayscale values divided by 255. `model.npz` contains float32 arrays `w1` (784,64), `b1` (64,), `w2` (64,10), `b2` (10,). Compressed file: 188991 bytes.

Teacher training uses scikit-learn MLPClassifier, Adam, batch size 256, learning rate .001, seed 42, max 60 epochs, early stopping with patience 8. Actual run: 30 epochs. Of the standard 60000 training examples, 54000 are used for fitting and 6000 for validation. Best validation accuracy: 97.1667%. Standard 10000 test examples are untouched by fitting or early stopping. No sample selection based on prediction success is used.

Versions: Python 3.11, NumPy 2.4.6, Pillow 13.0.0, scikit-learn 1.9.1. Training/export script and exact dependency freeze are retained in `teacher_tools/train_model.py` and `teacher_tools/training-requirements.txt` in the teacher tools, in the supplied lesson package.

## Measured held-out evaluation

- **9732 / 10000 correct = 97.32%**, measured across the entire original test split.
- Evaluation applies the same crop/resize/polarity preprocessing used by the deployed API, not just raw MNIST vectors.
- float32 NumPy exported predictions agree with scikit-learn on **100%** of test examples.
- Separate evaluation through actual `predict(image)` on all 10000 images, with `socket.socket` and `socket.create_connection` disabled: **97.32%**. No scikit-learn imported.
- Bundled examples: 19/20 recognized correctly. These are the first two test occurrences per label, not cherry-picked successes; see provenance README.
- Detailed confusion matrix, dataset and weight hashes, versions, validation score: teacher tools `teacher_tools/metrics.json`. Public API offline run and per-sample predictions: `teacher_tools/offline_metrics.json`; raw logs: `training.log` and `offline-evaluation.log`.

## API and preprocessing

```python
from shared.digit_model import predict, prepare_image
scores = predict(image)  # dict[str, float], ordered keys '0' through '9'
preview = prepare_image(image)  # PIL.Image.Image, mode 'L', 28x28
```

Accepts PIL images or NumPy grayscale/RGB/RGBA arrays. Arrays normally use uint8 0..255; floating 0..1 is also supported. RGBA is composited over white. Border brightness determines inversion so either dark-on-light or light-on-dark ink works. The background is subtracted, ink bounding box is cropped using a modest noise threshold, aspect ratio is preserved while fitting inside 20x20, and the result is geometrically centered on a black 28x28 canvas. Preview has bright ink on black, and is exactly the image scored.

None/blank input raises `ValueError('Please draw a digit from 0 to 9 first!')`. Weights are loaded lazily and cached once per imported module, from a path relative to `__file__`, with `allow_pickle=False`.

## Limitations

MNIST accuracy is not an accuracy guarantee on children's tablet/mouse drawings. Different pen widths, rotations, crowded backgrounds, clipped edges, multiple digits, letters, and unfamiliar writing styles can cause mistakes. The classifier always chooses among 0..9 for nonblank input; it has no out-of-distribution detector. Softmax values sum to one but are not calibrated probabilities or proof of certainty. The simple polarity heuristic assumes a mostly uniform background. Geometric centering is used, not center-of-mass deskewing. The model is a small teaching model, not intended for consequential decisions.

## Reproduction (teacher tools, internet needed only for initial dataset download)

From `teacher_tools`, with the sibling `../shared` directory retained:

```sh
python3 -m venv training-venv
training-venv/bin/pip install -r training-requirements.txt
training-venv/bin/python train_model.py > training.log 2>&1
training-venv/bin/python evaluate_offline.py > offline-evaluation.log 2>&1
training-venv/bin/python -m pytest ../tests -q
```

On Windows, use `training-venv\Scripts\python.exe` and the corresponding pip command. Training sets BLAS threads to 2. Reruns on other libraries/platforms may differ numerically. Training is never needed for lesson use. Training tools are optional teacher material. Do not distribute a training environment or the full dataset to students; neither is needed for inference.
