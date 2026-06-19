"""Canonical filesystem locations.

Resolve the repo root once (portably) and hang everything off it, so scripts no longer
hardcode an absolute ``/Users/...`` path.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]   # bentley/shared/paths.py -> repo root
ASSETS = ROOT / "assets"
SCRATCH = ROOT / "scratch"
EPISODES = ROOT / "episodes"


def episode_assets(ep="hybrid_ep1"):
    """Asset working directory for an episode, e.g. assets/pilot_shots/hybrid_ep1."""
    return ASSETS / "pilot_shots" / ep
