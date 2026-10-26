"""Extra columns for the summary table: crawl lag, deletion rate, creator concentration.

    python3 -I tmp/dataset_summary/build_extra.py <downloaded_datasets dir> <out.json>
"""
import json
import math
import sys
from pathlib import Path

import pandas as pd
import pyarrow.parquet as pq

ROOT = Path(sys.argv[1])
OUT = Path(sys.argv[2])


def concentration(author_per_post):
    """Posts per creator (median, mean) and share of posts made by the top 1% of creators."""
    per = author_per_post.value_counts()
    top = max(1, math.ceil(len(per) * 0.01))
    return {"creators": len(per), "median_posts": float(per.median()), "mean_posts": float(per.mean()),
            "top1pct_creators": top, "top1pct_share": float(per.iloc[:top].sum() / per.sum())}


def lag(created, crawled):
    days = (crawled - created).dt.total_seconds().dropna() / 86400
    return {"median_days": float(days.median()), "p25": float(days.quantile(.25)),
            "p75": float(days.quantile(.75)), "n": int(len(days))}


res = {}

# --- Crawl lag ---------------------------------------------------------------
m = pd.read_csv(ROOT / "german_multimodal/meta_data.csv")
m["scraped"] = pd.to_datetime(m.date_scraping, format="%d_%m_%Y")
m["created"] = pd.to_datetime(m.timestamp)
first = m.sort_values("scraped").drop_duplicates("id_hash")  # first time each video was seen
res["German Multimodal"] = {"lag": lag(first.created.dt.normalize(), first.scraped),
                            "conc": concentration(first.author_hash)}

t = pd.concat([pq.read_table(f, columns=["id", "user_id", "collected_time", "create_time"]).to_pandas()
               for f in sorted((ROOT / "tiktok_10m").glob("*.parquet"))], ignore_index=True)
t = t.drop_duplicates("id", keep="last")
created = pd.to_datetime(t.create_time, unit="s", utc=True)
collected = pd.to_datetime(t.collected_time, errors="coerce", utc=True)
res["TikTok-10M"] = {"lag": lag(created, collected), "conc": concentration(t.user_id)}
del t

# Only the crawl month is reported: use the middle of it, so lags are approximate
g = pd.read_csv(ROOT / "gesis_news/TikTok-news_data_v2-0-0.csv").drop_duplicates("M1_video_id")
g_created = pd.to_datetime(g.M3_create_time, errors="coerce")
res["GESIS News"] = {"lag_approx": lag(g_created, pd.Series(pd.Timestamp("2024-01-15"), index=g.index)),
                     "conc": concentration(g.V3_news_outlet)}

v = pd.concat([pd.read_csv(ROOT / f"tides_influencer/tiktok_videos-{i}.csv",
                           usecols=["id", "createTimeISO", "authorId"]) for i in (1, 2)]
              ).drop_duplicates("id", keep="last")
v_created = pd.to_datetime(v.createTimeISO, errors="coerce", utc=True)
res["TIDES Influencer"] = {"lag_approx": lag(v_created, pd.Series(pd.Timestamp("2023-06-15", tz="UTC"), index=v.index)),
                           "conc": concentration(v.authorId)}

# --- Creator concentration (no timestamps) ------------------------------------
c = pd.DataFrame(json.load(open(ROOT / "climate_change/videos.json")))
res["Climate Change"] = {"conc": concentration(c.drop_duplicates("video_id").author_id)}
u = pd.read_csv(ROOT / "ukraine/video_ids.csv").drop_duplicates("video_id")
res["Ukraine"] = {"conc": concentration(u.user_unique_id)}

# --- Deletion rate (PoliTok-DE availability re-checks) ------------------------
dele = {}
for name, f in [("federal_2025", "federal"), ("saxony_2024", "saxony")]:
    p = pd.read_parquet(ROOT / f"politok_de/{f}_post_ids.parquet")
    for col in [c for c in p.columns if c.startswith("availability_")]:
        vc = p[col].value_counts()
        conclusive = vc.get("AVAILABLE", 0) + vc.get("DELETED", 0)
        dele[f"{name} @ {col[13:]}"] = {"deleted": int(vc.get("DELETED", 0)), "conclusive": int(conclusive),
                                        "total": len(p), "rate": vc.get("DELETED", 0) / conclusive}
res["PoliTok-DE"] = {"deletion": dele}

OUT.write_text(json.dumps(res, indent=2, default=str))
print(json.dumps(res, indent=1, default=str))
