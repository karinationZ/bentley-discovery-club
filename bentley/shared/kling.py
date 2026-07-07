"""Canonical Kling 3.0 i2v payload builder — with FIRST+LAST frame pinning (drift lever #3).

The whole EP3/EP4 render pattern is `image_urls:[keyframe]` — only the FIRST frame is on-model, so
Kling can drift the character over the clip and END on a mutated Bentley (paws whiten, tail lengthens).
Kling 3.0 single-shot i2v also accepts a LAST frame at image_urls[1]: the model then only interpolates
motion between two identity-correct anchors, so it can't wander far mid-clip and cannot finish off-model.
This is the cheapest structural drift-killer per shot (verified in KIE's Kling 3.0 docs; single-shot only).

Usage — build the payload, then hand it to kie_client.run("kling-3.0/video", payload):

    from bentley.shared.kling import i2v_payload, bentley_element
    payload = i2v_payload(prompt, first_url,
                          elements=[bentley_element(master_url, turn_url)],
                          last_url=end_keyframe_url)          # <-- the new lever
    r = kie_client.run("kling-3.0/video", payload, timeout=1200, poll=10)

Rules baked in (owner law / research): multi_shots ALWAYS False (last-frame is honored only in
single-shot; omitting multi_shots → 422); both frames must themselves be on-model (garbage-in); keep
start/end POSES CLOSE or the interpolation warps — this lever is for calm holds/continuations, not a
big pose swing. For a big action beat, pin only the first frame (pass last_url=None) and keep the clip
short. Does NOT change the model (kling-3.0/video, locked).
"""

VIDEO_MODEL = "kling-3.0/video"


def bentley_element(master_url, turnaround_url, name="Bentley", description=None):
    """The standard Bentley identity element (2 refs: master + turnaround)."""
    description = description or (
        "Bentley the red-fawn Boxer puppy: black face mask, grey chin, floppy folded-down ears, "
        "white chest blaze, short docked tail stub, teal collar with gold paw-print tag, paws the "
        "same color as her coat, no white socks")
    return {"name": name, "description": description,
            "element_input_urls": [master_url, turnaround_url]}


def i2v_payload(prompt, first_url, *, last_url=None, elements=None, duration="5",
                aspect_ratio="16:9", mode="std", sound=False):
    """Build a kling-3.0/video i2v payload. Pass last_url to PIN the clip's end frame (drift lever #3).

    image_urls[0] = first frame; image_urls[1] = last frame (single-shot only). multi_shots is forced
    False (required for last-frame + avoids the 422). Returns the input dict for kie_client.run."""
    if not first_url:
        raise ValueError("first_url (the on-model start keyframe) is required")
    image_urls = [first_url] if last_url is None else [first_url, last_url]
    payload = {
        "prompt": prompt,
        "image_urls": image_urls,
        "sound": sound,
        "duration": str(duration),
        "aspect_ratio": aspect_ratio,
        "mode": mode,
        "multi_shots": False,          # last-frame honored only here; omitting → 422
    }
    if elements:
        payload["kling_elements"] = elements
    return payload
