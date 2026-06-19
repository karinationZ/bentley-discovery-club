# Episodes — per-episode DATA

One folder per episode (`ep1/`, `ep2/`, …). Code in `bentley/` stays episode-agnostic; everything
episode-specific lives here.

```
episodes/
└── ep1/
    └── shotlists/      # the *.json shot specs fed to `python pipeline.py <file>`
```

Convention for a new episode: `mkdir -p episodes/epN/shotlists`, add the shot spec JSON, then
`python pipeline.py episodes/epN/shotlists/<spec>.json`. (Assembly/mix tables are still inline in
the builders today — see docs/REPO_ARCHITECTURE.md §8 for the plan to move them here.)
