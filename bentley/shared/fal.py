"""fal.ai helpers — timeout-guarded subscribe, model IDs, and approved reference URLs.

Single source for the fal model slugs + the APPROVED Bentley/Pip master references that
pipeline.py used to define inline.
"""
import concurrent.futures

import fal_client

M_T2I = "fal-ai/nano-banana"
M_EDIT = "fal-ai/nano-banana/edit"
M_VIDEO = "fal-ai/kling-video/v2.5-turbo/pro/image-to-video"
M_AVATAR = "fal-ai/kling-video/ai-avatar/v2/standard"

# APPROVED clean masters (paws fixed, 16:9, ears down, short tail).
REFS = {
    "bentley": "https://v3b.fal.media/files/b/0a9eb213/K0YEhgC0hRPAknNVA_bSO_Bentley_MASTER_clean_16x9.png",
    "pip": "https://d8j0ntlcm91z4.cloudfront.net/user_3F9AzDc10VXM2MT0k5hLwTCbjQr/hf_20260616_223627_2eb7befd-9545-47ad-9d34-d1f13e108bfa.png",
}


def fsub(model, arguments=None, timeout=420):
    """fal_client.subscribe with a HARD timeout so a balance-lock / queue hang can't eat hours
    (a single Kling render is minutes, not hours)."""
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as ex:
        try:
            return ex.submit(fal_client.subscribe, model, arguments=arguments).result(timeout=timeout)
        except concurrent.futures.TimeoutError:
            raise RuntimeError(
                f"FAL_TIMEOUT after {timeout}s on {model} (likely exhausted balance or queue hang)")
