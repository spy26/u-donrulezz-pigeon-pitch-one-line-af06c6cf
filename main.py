"""Pigeon Pitch, One Line — entry writer.

Prints the one-line elevator pitch and writes it, byte for byte, to
$MAKEFUN_OUTPUT_DIR/entry.txt and to /output/entry.txt (when they differ),
verifying every written file by reading it back.
"""

import os
import sys

PITCH = (
    "We run a 10,000-courier delivery fleet paid in breadcrumbs, "
    "and our only churn is when a hawk eats middle management."
)

MAX_CHARS = 200
SECONDARY_DIR = "/output"
TARGET_NAME = "entry.txt"


def _reject(reason):
    print("INVALID: " + reason, file=sys.stderr)
    sys.exit(1)


def check_pitch(text):
    """Gate the pitch: one non-blank line, 1-200 chars, exactly one sentence."""
    if not text:
        _reject("pitch is empty")
    if text.strip() == "":
        _reject("pitch is only whitespace")
    if "\n" in text or "\r" in text:
        _reject("pitch spans more than one line")
    if len(text) > MAX_CHARS:
        _reject("pitch is %d chars, over the %d limit" % (len(text), MAX_CHARS))
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in text):
        _reject("pitch contains a control character")
    if text != text.strip():
        _reject("pitch has leading or trailing whitespace")
    if "  " in text:
        _reject("pitch has a double space")
    if not text.endswith("."):
        _reject("pitch must end with a full stop")
    body = text[:-1]
    for closer in (". ", "? ", "! "):
        if closer in body:
            _reject("pitch has a sentence break in the middle")
    if "?" in body or "!" in body:
        _reject("pitch has a question or exclamation mark in the middle")


def write_and_prove(folder, payload):
    """Write payload to folder/entry.txt, then read it back and compare bytes."""
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, TARGET_NAME)
    with open(path, "wb") as handle:
        handle.write(payload)
    with open(path, "rb") as handle:
        back = handle.read()
    if back != payload:
        _reject("read-back mismatch in %s" % path)
    return path


def main():
    check_pitch(PITCH)
    payload = PITCH.encode("utf-8")
    print(PITCH)

    primary = os.environ.get("MAKEFUN_OUTPUT_DIR") or SECONDARY_DIR
    written = [write_and_prove(primary, payload)]
    if os.path.abspath(primary) != os.path.abspath(SECONDARY_DIR):
        written.append(write_and_prove(SECONDARY_DIR, payload))

    for path in written:
        print("wrote %s (%d bytes)" % (path, len(payload)))


if __name__ == "__main__":
    main()
