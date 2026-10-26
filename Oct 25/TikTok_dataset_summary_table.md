# TikTok dataset summary table

## Motivation

What makes it hard to study TikTok from **datasets collected in the past** rather than from live observation? This table compares ten public TikTok datasets on the same columns: how the posts were found (crawling seed), how many creators and posts the release contains, the follower tiers of the creators, the engagement distribution of the posts, and when the data was crawled. A `NaN` cell means the public release does not give that information. The pattern of `NaN`s is itself one of the findings.

All counts and percentiles below were computed by us from the files in [downloaded_datasets/](../downloaded_datasets/) with [tmp/dataset_summary/build_summary.py](../tmp/dataset_summary/build_summary.py). Crawl lag, deletion rate and creator concentration were computed with [tmp/dataset_summary/build_extra.py](../tmp/dataset_summary/build_extra.py). Crawling seeds and crawl times that cannot be computed from the files come from the papers and data reports. These sources are summarised in [TikTok_five_more_datasets.md](../TikTok_five_more_datasets.md), [TikTok_additional_papers_and_datasets.md](../TikTok_additional_papers_and_datasets.md) and [Oct 9/readme.md](../Oct%209/readme.md).

### Column definitions

- **Crawling seed**
  - **Creator**: the authors chose relevant or interesting creators and collected their posts.
  - **Post**: the authors chose keywords or hashtags and collected the posts that matched them.
  - **User**: the authors simulated users and recorded the posts TikTok showed them (For You / Explore page).
- **Follower tiers** use the TIDES definitions: nano 1K–10K, micro 10K–50K, mid 50K–500K, macro 500K–1M, mega ≥1M. Accounts below 1K are counted separately as `<1K`.
- **P99** is the 99th percentile across unique posts: 99% of posts have a value below it. The full `describe(percentiles=[.25, .5, .75, .9, .99])` output is in Appendix A.
- **Crawl time** is when the data was collected. **Post period** is when the collected posts were published. Values marked *(data)* were computed from timestamps in the files. All other values are taken from the paper or data report.
- **Crawl lag** is the number of days between a post's publication and its crawl, given as median [25%–75%]. It tells you how "mature" the engagement snapshot is. `≈` marks lags computed against the middle of the reported crawl month, because no exact crawl date is available.
- **Deletion rate** is the share of posts that were no longer available when someone re-checked them later.
- **Creator concentration** is the median number of posts per creator, together with the share of all posts that come from the top 1% most active creators.

## Main table

| Dataset | Crawling seed | Total creators | Total posts | Follower tiers (creators) | P99 views | P99 likes | P99 comments | P99 shares | Crawl time (start – end) | Post period |
|---|---|---:|---:|---|---:|---:|---:|---:|---|---|
| [PoliTok-DE](https://huggingface.co/datasets/tomasruiz/PoliTok-DE) | **Post** (daily keyword search, Research API, `region=DE`) | NaN | 938,961 | NaN | NaN | NaN | NaN | NaN | Daily, 1 Jul 2024 – ~4 May 2025 (96 h after posting); availability re-checks until 11 Jun 2026 | 1 Jul – 30 Nov 2024; 13 Jan – 30 Apr 2025 |
| [Climate Change](https://zenodo.org/records/15131067) | **Creator → Post** (105 seed creators → 193 hashtags, Research API) | 18,041 | 590,360 | NaN | NaN | NaN | NaN | NaN | ~3-month API retrieval; exact dates not reported (seed-account history up to Oct 2024) | 16 Oct 2021 – 15 Oct 2022 |
| [German Multimodal](https://www.weizenbaum-library.de/items/04482f4d-3f73-44e9-859b-f815b089caab) | **User** (logged-out Explore page, German IP) | 2,992 | 5,137 (11,242 appearances) | <1K 37 · nano 416 · micro 645 · mid 1,199 · macro 259 · mega 436 | 47,584,000 | 3,864,000 | 30,664 | 85,876 | 31 Jul – 4 Aug 2023 *(data)* | 10 Apr – 31 Jul 2023 *(data)* |
| [TIDES Influencer](https://github.com/skmtr1/TIDES-TikTok-Influencer-dataset) | **Creator** (influencer lists, 1,000 per tier, ≤50 recent videos each) | 5,000 | 233,994 | nano 1,000 · micro 1,000 · mid 1,000 · macro 1,000 · mega 1,000 | 4,300,000 | 437,407 | 3,094 | 5,444 | Jun 2023 | 27 Apr 2016 – 6 Jun 2023 *(data)* |
| [DeHate](https://github.com/Multimodal-Intelligence-Lab-MIL/DeHate) | NaN (not reported) | NaN | 1,637 TikTok (6,689 incl. BitChute) | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| [Ukraine](https://github.com/networkdynamics/ukraine-tiktok) | **Post** (hashtags + keywords in EN/RU/UK, PyTok scraper) | 5,782 | 9,503 (18,864 before relevance filter) | NaN | NaN | NaN | NaN | NaN | Jul 2022; update Apr 2023 | Mainly 2022 (some early 2023) |
| [US Election 2024](https://github.com/gabbypinto/US2024PresElectionTikToks) | **Post** (election keywords/hashtags, Research API, US region) | NaN | 4,069,908 | NaN | NaN | NaN | NaN | NaN | Not reported (releases Jun 2024 – Feb 2025) | 1 Nov 2023 – 20 Jan 2025 |
| [RELIANCE](https://github.com/realize-lab/RELIANCE) | **Post** (56 health search queries, top 6 results, fresh account) | NaN | 336 (paper; 409 text units released) | NaN | NaN | NaN | NaN | NaN | Jan 2025 | NaN |
| [GESIS News](https://doi.org/10.7802/2819) | **Creator** (18 German-language news outlets, Research API) | 18 | 8,623 | NaN | 723,659 | 49,816 | 2,449 | 5,862 | Jan 2024 | 1 Jan – 31 Dec 2023 *(data)* |
| [TikTok-10M](https://huggingface.co/datasets/The-data-company/TikTok-10M) | NaN ("trending", US points of interest; method not reported) | 3,165,834 | 9,985,545 (10,000,000 rows) | NaN | 2,862,611 | 216,493 | 2,301 | 16,898 | 7 Mar – 3 Jul 2025 *(data)* | 16 Sep 2021 – 2 Jul 2025 *(data)* |

### Summary by column

| Column | Datasets with it | Datasets with NaN |
|---|---|---|
| Crawling seed | 8 of 10. Post: 5 (PoliTok-DE, Climate, Ukraine, US Election, RELIANCE) · Creator: 3 (TIDES, GESIS, Climate) · User: 1 (Multimodal) | DeHate, TikTok-10M |
| Total creators | 6 | PoliTok-DE, DeHate, US Election, RELIANCE |
| Follower counts | 2 (Multimodal, TIDES) | 8 |
| Views / likes / comments / shares | 4 (Multimodal, TIDES, GESIS, TikTok-10M) | 6 |
| Exact crawl dates | 2 from the data (Multimodal, TikTok-10M); the rest only to the month or not at all | DeHate fully missing; Climate and US Election have no crawl dates |

## Data availability matrix

✓ = released publicly · ◐ = partial, indirect or on request · ✗ = not released

| Dataset | Post ID | Post time | Creator ID | Followers | Engagement counts | Text (caption / hashtags) | Video | Comment text | Labels | ✓ count |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| PoliTok-DE | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ◐ 360 posts (935 annotations) | 1 / 9 |
| Climate Change | ✓ | ✗ | ✓ anonymised | ✗ | ✗ | ◐ hashtags only | ✗ | ✗ | ◐ LLM topics | 2 / 9 |
| German Multimodal | ✗ hashed | ✓ | ✓ hashed | ✓ | ✓ | ◐ hashtags only | ◐ embeddings | ✗ | ✗ | 4 / 9 |
| TIDES Influencer | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ◐ URLs + features | ✗ | ✗ | 6 / 9 |
| DeHate | ✗ anonymised | ✗ | ✗ | ✗ | ✗ | ✓ title + desc | ◐ on application | ✗ | ✓ | 2 / 9 |
| Ukraine | ✓ | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ | ◐ via hydration script | ◐ 388 posts (392 coding rows) | 2 / 9 |
| US Election 2024 | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | 1 / 9 |
| RELIANCE | ✗ | ✗ | ✗ | ✗ | ✗ | ◐ transcript sentences | ✗ | ✗ | ✓ | 1 / 9 |
| GESIS News | ✓ | ✓ | ✓ outlet | ✗ | ✓ | ◐ hashtags only | ✗ | ✗ | ✓ | 5 / 9 |
| TikTok-10M | ✓ | ✓ | ✓ | ✗ | ✓ | ✓ | ◐ URLs | ✗ | ✗ | 5 / 9 |

No dataset releases the videos themselves or the text of comments. Only three datasets (TIDES, GESIS, TikTok-10M) fully release more than half of the nine fields. Six of the ten fully release two fields or fewer.

## Crawl lag, deletion rate, creator concentration

| Dataset | Crawl lag, days: median [25%–75%] | Deletion rate | Posts per creator (median) | Share of posts from top 1% creators |
|---|---|---|---:|---:|
| PoliTok-DE | 4 (96 h, fixed by design) | Saxony: 6.3% (Oct 2024) → 17.3% (Dec 2024) → 18.9% (Jan 2025) · Federal: **39.7%** (Jun 2026) | NaN | NaN |
| Climate Change | NaN | NaN | 14 | 10.3% |
| German Multimodal | 47 [26–81] *(data)* | NaN | 1 | 12.3% |
| TIDES Influencer | ≈68 [34–165] | NaN | 50 | 1.1% |
| DeHate | NaN | NaN | NaN | NaN |
| Ukraine | NaN | ~29–30% after ~6 months (paper) | 1 | 15.7% |
| US Election 2024 | NaN | NaN | NaN | NaN |
| RELIANCE | NaN | NaN | NaN | NaN |
| GESIS News | ≈186 [99–276] | NaN | 376.5 (18 outlets) | 21.5% (1 outlet) |
| TikTok-10M | 78 [2–322] *(data)* | NaN | 1 | **21.4%** |

How to read this:
- **Engagement snapshots are taken at very different ages.** PoliTok-DE IDs were collected 4 days after posting, the Multimodal videos about 1.5 months after, and the GESIS videos about 6 months after. TikTok-10M ranges from 2 days to almost a year. A P99 of views from GESIS and one from TikTok-10M therefore measure different points in a video's life.
- **Posts disappear, and the share keeps growing.** In PoliTok-DE, 6% of the Saxony posts were gone after 1–3 months and 19% after 2–6 months. Of the federal posts, 40% were gone after 13–17 months. The availability files give the reasons, such as removal by the creator, a private account, a banned account, or failed moderation review. Any ID-only dataset (US Election, Ukraine, PoliTok-DE) loses part of its sample before anyone can hydrate it again.
- **The seed shapes the creator distribution.** In the Creator-seeded datasets, the authors chose the number of posts per creator: TIDES took about 50 recent videos per creator, so the top 1% hold only 1.1% of posts. In the Post- and User-seeded datasets, most creators appear once (median 1), but a small group dominates. In TikTok-10M, 1% of creators produced 21% of the posts.

## Appendix A — Engagement distributions

`describe(percentiles=[.25, .5, .75, .9, .99])` was computed on unique posts. When a post appears more than once, its latest snapshot is used. Values are rounded to integers. Only the four datasets with engagement counts are included.

### German Multimodal (n = 5,137 unique videos; "views" = `plays`)

| Metric | count | mean | std | min | 25% | 50% | 75% | 90% | 99% | max |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| views | 5,137 | 5,629,729 | 11,511,303 | 0 | 951,300 | 2,300,000 | 5,800,000 | 13,600,000 | 47,584,000 | 249,900,000 |
| likes | 5,137 | 415,755 | 815,947 | 0 | 59,300 | 159,900 | 399,500 | 1,000,000 | 3,864,000 | 15,000,000 |
| comments | 5,137 | 3,207 | 8,100 | 0 | 413 | 1,254 | 3,250 | 7,375 | 30,664 | 312,200 |
| shares | 5,137 | 7,518 | 21,781 | 0 | 469 | 1,877 | 6,302 | 17,700 | 85,876 | 629,300 |

### TIDES Influencer (n = 233,994 unique videos)

| Metric | count | mean | std | min | 25% | 50% | 75% | 90% | 99% | max |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| views | 233,994 | 274,048 | 2,235,126 | 0 | 3,024 | 15,400 | 92,200 | 457,100 | 4,300,000 | 402,000,000 |
| likes | 233,994 | 25,514 | 188,788 | 0 | 194 | 1,008 | 6,870 | 39,800 | 437,407 | 30,900,000 |
| comments | 233,994 | 202 | 2,955 | 0 | 4 | 16 | 66 | 275 | 3,094 | 1,200,000 |
| shares | 233,994 | 328 | 5,831 | 0 | 1 | 6 | 40 | 266 | 5,444 | 1,700,000 |

### GESIS News (n = 8,623 unique videos; 64 have no view count)

| Metric | count | mean | std | min | 25% | 50% | 75% | 90% | 99% | max |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| views | 8,559 | 48,878 | 191,810 | 0 | 143 | 1,645 | 21,265 | 121,800 | 723,659 | 7,105,469 |
| likes | 8,623 | 4,524 | 17,200 | 1 | 155 | 707 | 3,509 | 10,581 | 49,816 | 821,805 |
| comments | 8,623 | 201 | 1,656 | 0 | 4 | 22 | 115 | 415 | 2,449 | 137,075 |
| shares | 8,623 | 303 | 1,855 | 0 | 0 | 3 | 48 | 415 | 5,862 | 75,864 |

### TikTok-10M (n = 9,985,545 unique videos; views = `play_count`, likes = `digg_count`)

| Metric | count | mean | std | min | 25% | 50% | 75% | 90% | 99% | max |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| views | 9,985,545 | 151,239 | 1,249,233 | 0 | 1,021 | 4,010 | 26,318 | 160,394 | 2,862,611 | 342,570,787 |
| likes | 9,985,545 | 11,099 | 104,781 | 22 | 61 | 166 | 1,092 | 8,311 | 216,493 | 22,168,410 |
| comments | 9,985,545 | 137 | 1,421 | 0 | 3 | 9 | 34 | 155 | 2,301 | 1,070,474 |
| shares | 9,985,545 | 952 | 14,875 | 0 | 1 | 8 | 60 | 544 | 16,898 | 10,376,480 |

## Appendix B — Follower tiers

| Dataset | <1K | nano (1K–10K) | micro (10K–50K) | mid (50K–500K) | macro (500K–1M) | mega (≥1M) | Total |
|---|---:|---:|---:|---:|---:|---:|---:|
| German Multimodal | 37 | 416 | 645 | 1,199 | 259 | 436 | 2,992 |
| TIDES Influencer | 0 | 1,000 | 1,000 | 1,000 | 1,000 | 1,000 | 5,000 |

- **German Multimodal**: a creator can appear on several days with different follower counts, so we use each creator's highest observed count. The sample leans heavily towards large accounts: 63% are mid or larger. This is what the Explore page shows, not what a typical TikTok creator looks like.
- **TIDES**: the authors chose the sample to have 1,000 creators per tier. The table uses the authors' `tier` labels. If our thresholds are applied to the `followers` column instead, 4 creators move across a tier boundary (micro 999, mid 1,001, macro 999, mega 1,001), because their follower count sits exactly on a boundary.

## Notes — why cells are NaN, and caveats

- **ID-only releases (PoliTok-DE, US Election, Ukraine).** Only post IDs (and, for Ukraine, user handles) are public. Followers and engagement require re-collecting each post from TikTok ("hydration") through the Research API or a logged-in scraper. We did not hydrate these datasets, and many posts are no longer available: PoliTok-DE was built to measure this, and the Ukraine authors found about 30% of videos unavailable after six months.
- **Text-only or label-only releases (RELIANCE, DeHate, Climate Change).** RELIANCE releases only transcribed claim sentences and labels, with no video IDs, so the post count of 336 comes from the paper. The paper reports 56 queries, but the released JSON contains only 55 distinct queries. DeHate releases annotations with anonymised IDs and does not document its crawling method or dates. Climate Change releases hashtags, topics and a follower network, but no engagement counts.
- **Counting details.** Climate Change has 590,361 rows with 590,360 unique IDs, and 18,041 authors in `videos.json` but only 14,047 in `profiles.csv`. US Election has three overlapping ID files; we count the latest (`TikTok_IDs_2025_Feb.csv`). The 4,069,908 IDs exceed the 3,144,836 videos analysed in the paper. TikTok-10M has 10,000,000 rows but 9,985,545 unique IDs. In GESIS, "creators" means news outlets. Label counts are unique posts: PoliTok-DE has 935 annotation rows (several annotators per post) on 360 posts, and Ukraine has 392 coding rows on 388 videos (4 videos are coded twice).
- **Engagement counts are snapshots.** Each number was recorded at the time of the crawl, so a video crawled one day after posting and one crawled a year later are not directly comparable.
- **German Multimodal counts appearances.** 11,242 rows are Explore-page appearances of 5,137 unique videos. We report statistics on unique videos. The crawl lag uses the first day each video appeared. The `category` column is the Explore-page tab the video was shown under, not a human label. Concentration is computed on unique videos, which covers 2,987 creators: 5 hashed creator IDs occur only on repeated appearances.
- **How the extra columns were computed.** The deletion rate for PoliTok-DE is the number of `DELETED` posts divided by the posts that got a conclusive result (`AVAILABLE` or `DELETED`) at each re-check. `NOT_RESCRAPED` and `UNKNOWN_ERROR` posts are excluded. The approximate crawl lags for GESIS and TIDES use 15 Jan 2024 and 15 Jun 2023, the middle of each reported crawl month. TikTok-10M uses each post's own `collected_time`; 46 posts have no collection time.
- **TikTok-10M looks filtered.** The minimum like count is 22, which suggests a popularity filter. Together with the "trending" label, this pushes the distribution upward. The dataset card does not explain how posts were sampled.
- **No dataset is a random sample of TikTok.** Each one reflects its seed: keyword lists, chosen creators, or the feed one simulated user was shown. Differences between the P99 values reflect these sampling choices as well as audience behaviour.
