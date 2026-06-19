# Prompts — prompt library as data

Target home for the image/video/thumbnail prompt strings that are currently inline in the
generators (`bentley/asset_generation/*`, `animation/*`). Organize per episode:

```
prompts/
└── ep1/        # keyframe / motion / thumbnail prompts for episode 1
```

Migrate prompts here incrementally (as JSON or `.txt`), so prompt edits don't require touching
code and future episodes can reuse/override them. See docs/REPO_ARCHITECTURE.md §7.
