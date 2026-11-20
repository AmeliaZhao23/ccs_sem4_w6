# Bundled digit examples

These 20 PNGs are actual images from the standard **held-out MNIST test split**, not synthetic drawings and not training examples. Source archive: https://storage.googleapis.com/tensorflow/tf-keras-datasets/mnist.npz (`x_test`, `y_test`). Original dataset: https://yann.lecun.org/exdb/mnist/ (Yann LeCun, Corinna Cortes, Christopher J. C. Burges; underlying source NIST).

Each filename `digit_D_mnist_test_IIIII.png` records the true label D and zero-based original test-array index IIIII. Two examples per digit are selected by taking the **first two test indices with that ground-truth label**, without filtering on whether the trained model predicts correctly. The model gets 19/20 of these right; a mistake is a useful lesson, not a broken sample. Per-file labels and indices are also recorded by the teacher training tool in `modelwork/sample_manifest.json`.

Images are unmodified 28x28 grayscale MNIST pixels (light ink on dark background), saved losslessly as PNG. `prepare_image` applies the same normalization to these examples as to user drawings.

Rights: do not assume the license of Keras or this lesson applies to MNIST images. No blanket permissive dataset license is asserted. Verify original MNIST/NIST terms before redistributing for your intended use. See `../MODEL_CARD.md` for dataset hash, evaluation and limitations.
