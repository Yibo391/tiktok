"""Compute per-dataset counts, follower tiers and engagement percentiles for the
TikTok dataset summary table. Run from anywhere:

    python3 -I tmp/dataset_summary/build_summary.py <downloaded_datasets dir> <out.json>
"""
import json
import sys
from pathlib import Path

import pandas as pd
import pyarrow.parquet as pq

ROOT = Path(sys.argv[1])
OUT = Path(sys.argv[2])

PERCENTILES = [.25, .5, .75, .9, .99]
METRICS = ["views", "likes", "comments", "shares"]
# TIDES tier boundaries, verified against the min/max followers of each tier
TIER_BINS = [0, 1_000, 10_000, 50_000, 500_000, 1_000_000, float("inf")]
TIER_LABELS = ["<1K", "nano", "micro", "mid", "macro", "mega"]


def tiers(followers):
    cut = pd.cut(pd.to_numeric(followers, errors="coerce").dropna(),
                 bins=TIER_BINS, labels=TIER_LABELS, right=False)
    return {k: int(v) for k, v in cut.value_counts().reindex(TIER_LABELS).items()}


def describe(posts):
    out = {}
    for m in METRICS:
        if m in posts:
            s = pd.to_numeric(posts[m], errors="coerce").dropna()
            out[m] = s.describe(percentiles=PERCENTILES).to_dict()
    return out


def date_range(s):
    s = s.dropna()
    return [str(s.min()), str(s.max())] if len(s) else None


def politok():
    ids = pd.concat([pd.read_parquet(ROOT / f"politok_de/{f}_post_ids.parquet", columns=["post_id"])
                     for f in ("federal", "saxony")])
    return {"posts": ids.post_id.nunique()}


def climate():
    v = pd.DataFrame(json.load(open(ROOT / "climate_change/videos.json")))
    return {"posts": v.video_id.nunique(), "creators": v.author_id.nunique()}


def multimodal():
    m = pd.read_csv(ROOT / "german_multimodal/meta_data.csv")
    m["scraped"] = pd.to_datetime(m.date_scraping, format="%d_%m_%Y")
    m["created"] = pd.to_datetime(m.timestamp)
    # Same video can appear on several scrape days: keep its latest snapshot
    posts = (m.sort_values("scraped").drop_duplicates("id_hash", keep="last")
             .rename(columns={"plays": "views"}))
    followers = m.groupby("author_hash").author_followers.max()
    return {"posts": m.id_hash.nunique(), "rows": len(m), "creators": m.author_hash.nunique(),
            "tiers": tiers(followers), "engagement": describe(posts),
            "post_period": date_range(m.created.dt.date), "crawl_period": date_range(m.scraped.dt.date)}


def tides():
    inf = pd.read_csv(ROOT / "tides_influencer/tiktok_influencers.csv")
    inf = inf[inf.tier.isin(TIER_LABELS)]
    cols = ["id", "createTimeISO", "authorId", "views", "likes", "comments", "shares"]
    v = pd.concat([pd.read_csv(ROOT / f"tides_influencer/tiktok_videos-{i}.csv", usecols=cols)
                   for i in (1, 2)]).drop_duplicates("id", keep="last")
    created = pd.to_datetime(v.createTimeISO, errors="coerce", utc=True).dt.date
    return {"posts": v.id.nunique(), "creators": inf.id.nunique(),
            "tiers": tiers(inf.followers), "tiers_as_labelled": inf.tier.value_counts().to_dict(),
            "engagement": describe(v), "post_period": date_range(created)}


def dehate():
    d = pd.read_excel(ROOT / "dehate/DeHate.xlsx")
    return {"posts": d.loc[d.Platform == "TikTok", "Video ID"].nunique(), "rows_all_platforms": len(d)}


def ukraine():
    u = pd.read_csv(ROOT / "ukraine/video_ids.csv")
    raw = pd.read_csv(ROOT / "ukraine/raw_video_ids.csv")
    return {"posts": u.video_id.nunique(), "creators": u.user_unique_id.nunique(),
            "raw_posts_before_filter": raw.video_id.nunique()}


def us_election():
    ids = pd.read_csv(ROOT / "us_election/TikTok_IDs_2025_Feb.csv", dtype={"id": str})
    return {"posts": ids.id.nunique()}


def reliance():
    d = json.load(open(ROOT / "reliance/data.json"))["data"]
    return {"text_units": len(d), "queries": len({r["query"] for r in d})}


def gesis():
    g = pd.read_csv(ROOT / "gesis_news/TikTok-news_data_v2-0-0.csv")
    posts = g.drop_duplicates("M1_video_id").rename(columns={
        "M5_view_count": "views", "M4_like_count": "likes",
        "M6_comment_count": "comments", "M7_share_count": "shares"})
    created = pd.to_datetime(g.M3_create_time, errors="coerce").dt.date
    return {"posts": g.M1_video_id.nunique(), "creators": g.V3_news_outlet.nunique(),
            "engagement": describe(posts), "post_period": date_range(created)}


def tiktok_10m():
    cols = ["id", "user_id", "collected_time", "create_time",
            "play_count", "digg_count", "comment_count", "share_count"]
    t = pd.concat([pq.read_table(f, columns=cols).to_pandas()
                   for f in sorted((ROOT / "tiktok_10m").glob("*.parquet"))], ignore_index=True)
    rows = len(t)
    t = t.drop_duplicates("id", keep="last").rename(columns={
        "play_count": "views", "digg_count": "likes",
        "comment_count": "comments", "share_count": "shares"})
    created = pd.to_datetime(t.create_time, unit="s", errors="coerce").dt.date
    collected = pd.to_datetime(t.collected_time, errors="coerce", utc=True).dt.date
    return {"posts": t.id.nunique(), "rows": rows, "creators": t.user_id.nunique(),
            "engagement": describe(t), "post_period": date_range(created),
            "crawl_period": date_range(collected)}


LOADERS = {"PoliTok-DE": politok, "Climate Change": climate, "German Multimodal": multimodal,
           "TIDES Influencer": tides, "DeHate": dehate, "Ukraine": ukraine,
           "US Election 2024": us_election, "RELIANCE": reliance, "GESIS News": gesis,
           "TikTok-10M": tiktok_10m}

results = {}
for name, fn in LOADERS.items():
    print("loading", name, flush=True)
    results[name] = fn()
    print(json.dumps(results[name], default=str)[:400], flush=True)
OUT.write_text(json.dumps(results, indent=2, default=str))
