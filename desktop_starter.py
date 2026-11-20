"""Local Digit Detective: desktop starter."""

# Steps 1-3 are identical in the desktop file and the iPad notebook.
# Safety checks and the result-message format are already provided.
def recognise(image):
    if image is None:
        return "Choose a picture first.", {}

    from shared.digit_model import predict
    try:
        # STEP 1: Ask the bundled model for its scores.
        scores = {}  # TODO 1: replace {}
    except ValueError as error:
        return str(error), {}

    # Provided: the unfinished starter still runs safely.
    if not scores:
        return "TODO: connect the model in Step 1.", {}

    # STEP 2: Find the digit with the highest score.
    winner = "?"  # TODO 2: replace "?"

    # STEP 3: Read that digit's score from the dictionary.
    confidence = 0.0  # TODO 3: replace 0.0

    # Provided: .0% displays a decimal score as a whole percentage.
    message = f"My guess: {winner} | Model score: {confidence:.0%}"
    return message, scores


# Provided: the interface and local-only launch settings.
if __name__ == "__main__":
    from shared.lesson_ui import launch_desktop
    launch_desktop(recognise)
