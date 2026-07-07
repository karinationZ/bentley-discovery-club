"""Best-of image picker (bentley/qa/image_bestof.py) — ranks candidates by on-model-ness (lever #4).
Verifies: the candidate whose palette matches the DNA ranks above an off-color one; a white-paw
candidate is penalised and flagged; the CLI picks the best."""
import numpy as np
from PIL import Image

from bentley.qa.image_bestof import rank, white_paw_frac

COAT = (150, 92, 52)      # red-fawn
BG = (90, 130, 80)
WHITE = (240, 238, 235)


def dog(path, coat=COAT, white_paws=False):
    """220x220 fawn dog on meadow; optional white paws in the lower-center."""
    rng = np.random.default_rng(3)
    a = np.zeros((220, 220, 3), np.float64)
    a[..., :] = BG
    a[40:170, 70:150] = coat                 # body
    a[60:95, 95:125] = (20, 18, 20)          # dark face mask
    a[150:200, 80:140] = coat                # legs
    if white_paws:
        a[185:200, 85:135] = WHITE           # white socks (lower-center = paw region)
    a += rng.normal(0, 3, a.shape)
    Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).save(path)


def test_onmodel_beats_offcolor(tmp_path):
    ref = str(tmp_path / "dna.png"); dog(ref)
    good = str(tmp_path / "good.png"); dog(good)                       # same palette
    bad = str(tmp_path / "bad.png"); dog(bad, coat=(60, 90, 170))      # blue coat = off-model
    rows = rank([bad, good], ref)
    assert rows[0]["path"] == good            # on-model ranks first regardless of input order


def test_white_paws_penalised_and_flagged(tmp_path):
    ref = str(tmp_path / "dna.png"); dog(ref)
    clean = str(tmp_path / "clean.png"); dog(clean)
    socks = str(tmp_path / "socks.png"); dog(socks, white_paws=True)
    rows = rank([socks, clean], ref)
    assert rows[0]["path"] == clean
    socks_row = next(r for r in rows if r["path"] == socks)
    assert socks_row["white_paw"] > 0.02 and any("WHITE-PAWS" in f for f in socks_row["flags"])


def test_white_paw_frac_detects_socks(tmp_path):
    p = str(tmp_path / "s.png"); dog(p, white_paws=True)
    arr = np.asarray(Image.open(p).convert("RGB"), np.float64)
    assert white_paw_frac(arr) > 0.02
    p2 = str(tmp_path / "c.png"); dog(p2, white_paws=False)
    arr2 = np.asarray(Image.open(p2).convert("RGB"), np.float64)
    assert white_paw_frac(arr2) < 0.01


def test_cli_picks_best(tmp_path, capsys):
    from bentley.qa.image_bestof import main
    ref = str(tmp_path / "dna.png"); dog(ref)
    good = str(tmp_path / "good.png"); dog(good)
    bad = str(tmp_path / "bad.png"); dog(bad, coat=(60, 90, 170))
    rc = main([bad, good, "--ref", ref])
    out = capsys.readouterr().out
    assert rc == 0 and "BEST:" in out and "good.png" in out.splitlines()[-1]
