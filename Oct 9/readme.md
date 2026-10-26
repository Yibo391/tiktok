# Five TikTok datasets: questions a supervisor may ask

Checked on **9 October 2026**. This guide accompanies five independent English notebooks. It keeps three types of evidence separate:

- **Paper-reported:** stated by the authors in a paper or, for the German multimodal archive, a data report.
- **Release-described:** stated by the official dataset or code repository.
- **Locally measured:** calculated by executing the notebooks on files saved in `downloaded_datasets/`.

These are not interchangeable. A paper can analyse information that its public release does not contain. The [download-status guide](../downloaded_datasets/FIVE_NEW_DATASETS_DOWNLOADS.md) lists the local folders and release links.

## Questions that apply to every dataset

**Where did the numbers in your presentation come from?**  I state the source beside each number. Paper totals describe the authors' research corpus at publication time; notebook totals describe the specific public files downloaded here. If the two differ, I show both. All local statistics are computed from the public files, not copied from a paper.

**What does a row represent?**  It depends on the file: a post ID, an annotation vote, a video record, a creator, a follower edge, or an Explore-page appearance. Before calculating a rate, I identify the unit and the denominator. An annotation row is not always a unique video.

**Are these representative samples of all TikTok videos?**  No. They were collected using election keywords, climate hashtags and language filters, a German Explore page, selected influencers, or eating-disorder search terms. Their statistics describe those collections. None is a random platform-wide sample. Collection designs are in the [PoliTok-DE paper, §3](https://arxiv.org/html/2509.15860), [climate paper, §§3–4](https://arxiv.org/html/2505.03813), [TIDES paper, “Our New TIDES Dataset”](https://ojs.aaai.org/index.php/ICWSM/article/download/31405/33565/35461), and [EDTok paper, “Data Collection”](https://arxiv.org/html/2505.02250).

**Does a comment field mean we have comments?**  No. A field such as `comments` can be a **number of comments attached to a video at a particular observation time**. It is not a table of individual comments or their text. To calculate comment sentiment or themes, we would need actual comment rows. Even a per-video count may change if a video is re-checked later.

**Why use both mean and median?**  A few viral videos may have very large engagement counts. The mean responds strongly to these videos; the median describes the middle video. I report the number of non-missing observations and whether videos or creators are the unit. Spearman correlation ranks two quantities; it does not show that one causes the other.

## 1. PoliTok-DE — German elections

[English notebook](PoliTok_DE_dataset_analysis.ipynb) · [Paper v2](https://arxiv.org/html/2509.15860) · [Official release and hydration information](https://huggingface.co/datasets/tomasruiz/PoliTok-DE)

**Where did the data come from? Does the paper say this?**  Yes. Paper §3 describes daily keyword searches in the TikTok Research API, restricted to `region=DE`, followed by website scraping for media/metadata, later re-scraping for availability, and human annotation of a subset. The paper says API queries were delayed by 96 hours to allow for indexing. The Saxony collection covers posts published July–November 2024; the federal collection covers January–April 2025. This is the **authors' collection method**, not a crawl performed by our notebook.

**What did we actually download?**  Two post-ID/availability Parquet files and one Saxony annotation Parquet file. Public rows: **195,373** Saxony IDs and **743,588** federal IDs, matching paper v2. We did **not** download the raw videos, full creator records, captions, or comments. The authors say that media and metadata were collected for their research, but their public release provides IDs and hydration code rather than redistributing raw content. See [paper §§3 and 8](https://arxiv.org/html/2509.15860) and the [dataset card](https://huggingface.co/datasets/tomasruiz/PoliTok-DE).

**What does `DELETED` measure?**  It is a later accessibility/status snapshot. It is **not** by itself evidence that TikTok removed a rule-breaking video. Creator withdrawal, privacy changes, and platform action are possible; the paper uses further status-code patterns to infer categories. The notebook finds **36,617 / 195,373 = 18.74%** Saxony IDs in this state on 13 January 2025, and **295,101 / 743,588 = 39.69%** federal IDs on 11 June 2026. The paper's limitations explicitly warn that the two recheck horizons should not be compared as a direct election effect. See [paper §§4.2 and 7](https://arxiv.org/html/2509.15860).

**Where does the intolerance percentage come from?**  The public annotation file has **935 rows for 360 distinct posts**; in our notebook, `is_intolerant=yes` is **20.49% of valid yes/no annotation votes**, not of all election videos. The authors intentionally sampled deleted posts to increase the chance of finding intolerance; their Table 4 reports about **20.5% yes** and §6 provides the annotation definition/codebook. We also see **three posts with five annotation rows**, while §6.1 says each post had one to four annotators. The reason for that mismatch is unknown; do not guess. See [paper §6.1–6.2 and Appendix D](https://arxiv.org/html/2509.15860).

## 2. Climate change on TikTok

[English notebook](Climate_Change_TikTok_dataset_analysis.ipynb) · [Paper](https://arxiv.org/html/2505.03813) · [Zenodo release](https://zenodo.org/records/15131067)

**How were the videos found?**  Paper §3 starts with **105 climate-focused seed creators**, derives and manually checks **193 hashtags**, and queries the TikTok Research API in two-week publication intervals from **16 October 2021 to 15 October 2022**. The broader collected set was **1,326,684 videos from 199,968 users**. Paper §4 then selects **590,361 videos** with sufficiently long English descriptions for topic analysis. The seed accounts' history was collected by October 2024; the publication window and the time of actual API collection are different concepts. See [paper §§3–4](https://arxiv.org/html/2505.03813).

**What is in the release?**  Zenodo supplies `videos.json`, `profiles.csv`, `network.csv`, `topics.json`, and a README. The five files were downloaded locally and checked against Zenodo MD5 values. There is no raw video or individual comment text. Despite its suffix, `topics.json` contains **CSV text**. The notebook measures **590,361 video rows but 590,360 unique video IDs**: one extra duplicate row. This is a local file observation, not a paper claim. See the [Zenodo file list](https://zenodo.org/records/15131067).

**What is an `Outlier`? Does it mean anti-climate content?**  No. It means the topic model did not assign a named topic. The notebook measures **267,718 rows, or 45.35%**, with this label. Paper §4 describes a BERTopic pipeline and a final grouping into **26 named topics**, **17** climate-related. The model's topics describe text patterns, not scientific accuracy or political beliefs. See [paper §4](https://arxiv.org/html/2505.03813).

**Can you combine the follower network with the video table?**  Not by a naive join: network endpoints are username-like strings, while video author IDs are numeric. The notebook finds **zero direct matches** between the network `source` values and the video author IDs. The paper reports **13,867** network creators and **161,891** retained directed links; the notebook verifies those released-network counts. A verified crosswalk would be needed for creator-level joins. See [paper §3](https://arxiv.org/html/2505.03813).

## 3. German multimodal archive

[English notebook](German_Multimodal_TikTok_dataset_analysis.ipynb) · [Weizenbaum data record](https://www.weizenbaum-library.de/items/04482f4d-3f73-44e9-859b-f815b089caab) · [Data report PDF](https://www.weizenbaum-library.de/bitstreams/54049d98-d6c8-4c66-a890-6360118c22f9/download)

**Is this a paper? Where does the data come from?**  This source is a **dataset record with a data report by Lion Wedel (2023)**, not one of the peer-reviewed papers. The record/report describe capture of TikTok's Explore page from a German IP without logging in, using 4CAT and Zeeschuimer, from **31 July to 4 August 2023**. Its **11,242 appearance rows** and **5,137 distinct videos** are source-reported figures. An appearance is not necessarily a new video. See the [institutional record](https://www.weizenbaum-library.de/items/04482f4d-3f73-44e9-859b-f815b089caab) and [report](https://www.weizenbaum-library.de/bitstreams/54049d98-d6c8-4c66-a890-6360118c22f9/download).

**Which figures have we verified locally?**  After the manual download on 9 October 2026, four extracted CSVs are present in `downloaded_datasets/german_multimodal/`. The notebook now independently verifies **11,242 appearance rows** and **5,137 unique video hashes**, finds **3,676** videos appearing on multiple days, and confirms that each of the three embedding tables covers all 5,137 videos. Using each video's last observed scrape, the comment-count median is **1,254** and the mean is about **3,207**. These are counts in metadata, not individual comment records. See the [local acquisition-status note](../downloaded_datasets/german_multimodal/README.md).

**Are embeddings the original videos?**  No. They are numeric representations derived from text, audio, or visual material. The public description says video links/descriptions are withheld and creator/music identifiers are hashed. The current release therefore cannot support direct checking of raw video content or individual comments, even once the ZIPs are obtained. See the [institutional record and report](https://www.weizenbaum-library.de/items/04482f4d-3f73-44e9-859b-f815b089caab).

## 4. TIDES — influencer tiers

[English notebook](TIDES_Influencer_TikTok_dataset_analysis.ipynb) · [ICWSM 2024 paper PDF](https://ojs.aaai.org/index.php/ICWSM/article/download/31405/33565/35461) · [Authors' GitHub repository](https://github.com/skmtr1/TIDES-TikTok-Influencer-dataset)

**Where did the creators and videos come from?**  The paper's “Our New TIDES Dataset” section says the authors started with HypeAuditor and StarNgage influencer lists, checked follower counts against TikTok, selected **1,000 creators in each of five follower tiers**, then used an Apify TikTok scraper to get profiles and up to **50 recent videos per creator**. The authors used video URLs and Selenium to retrieve videos for their own feature extraction. The paper says they collected **230,406 videos in June 2023**. Their public release provides CSV-derived features and URLs, not MP4 files. See [paper pp. 2–3](https://ojs.aaai.org/index.php/ICWSM/article/download/31405/33565/35461).

**Why does your notebook say 233,994 videos, not 230,406?**  The downloaded public `tiktok_videos-1.csv` and `tiktok_videos-2.csv` together contain **233,994 distinct video IDs**, **3,588 more** than the paper snapshot. This is a verified release-versus-paper mismatch. The public files do not establish its cause, so we keep both values rather than silently removing rows. The creator file has **5,000 unique creators** and matches the paper count.

**What does `comments` mean, and how were the averages calculated?**  `comments` is a **per-video comment count in a CSV row**, not a comment table. The notebook converts it to numeric, then calculates the mean and median across non-missing video rows: **201.66** and **16**. When grouped by `authorTier`, the video-level medians are **3, 6, 14, 31, 88** from Nano to Mega. In a separate analysis, it first calculates each creator's median comment count across that creator's videos, then finds the median of those creator-level values within each tier. This avoids giving creators with more videos extra weight. The tier definitions are follower-count brackets in the [paper introduction](https://ojs.aaai.org/index.php/ICWSM/article/download/31405/33565/35461), while these particular means and medians are **our new descriptive calculations**, not claims made by the paper.

**Does a higher tier or a longer video cause more comments?**  No causal conclusion follows. The paper studies tier differences and potentially actionable features, but our notebook's duration bands and Spearman rank correlations describe associations in the released tables only. Creator size, topic, and posting time may affect both duration and engagement.

## 5. EDTok — eating-disorder content

[English notebook](EDTok_TikTok_dataset_analysis.ipynb) · [Paper](https://arxiv.org/html/2505.02250) · [Public GitHub repository](https://github.com/cbickham3232/EDTok-A-Dataset-for-Eating-Disorder-Content-on-TikTok)

**How did the authors collect and filter posts?**  The paper's “Data Collection” and “Data Filtering” sections describe TikTok API searches using eating-disorder terms, video download attempts with PykTok, invalid-format/photo-post losses, keyword filtering, and Gemini-assisted relevance screening. The authors went from **72,622** attempted downloads to **56,472** usable videos and finally **43,040** relevant videos. This is the authors' workflow, not a workflow reconstructed from the public CSV. See [paper, collection and filtering sections](https://arxiv.org/html/2505.02250).

**What does the public file contain? Can you check the paper's user and comment numbers?**  The entire public repository is now downloaded. Its `data/metadata.csv` has **43,040 distinct 19-digit video IDs** and **no other column**; `data/sample_metadata.csv` adds only **50 IDs already in the full list**. The README explicitly says only IDs are publicly distributed. The scripts are not additional datasets. This confirms the final video-ID count, but cannot verify the paper's **10,897 users**, **388,332 top-level comments**, or **188,739 replies**. The paper's total **577,071** combines those two comment types. See [paper, “Engagement Statistics”](https://arxiv.org/html/2505.02250) and [public repository](https://github.com/cbickham3232/EDTok-A-Dataset-for-Eating-Disorder-Content-on-TikTok).

**Can we compute mean or median comments per video?**  **Not from the public release.** It has IDs but no per-video comment counts and no comment rows. The notebook has an optional later step for an authorised `hydrated_videos.csv`; until such a file exists, the result is explicitly **Not calculated**. Dividing 577,071 by 43,040 would at most create a paper-total ratio, not a validated distribution or median, and the paper's collection details do not prove all comments and replies are aligned with an available local per-video table.

## One-sentence answer to give in a meeting

“For each dataset, I checked the paper's collection method and compared its reported totals with the exact public files I downloaded. My notebooks label new calculations as local results and leave unavailable media or comment statistics uncalculated.”
