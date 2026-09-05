# Additional TikTok papers and datasets

Prepared for Fraunhofer SIT. Links and availability were checked on **2 September 2026**.

## Scope

This report treats the literature review and the dataset search as **two independent tasks**:

1. **Five additional TikTok papers:** the papers may address any aspect of TikTok research. They do not need to introduce a public dataset.
2. **Three TikTok datasets:** these are evaluated primarily by present availability, released structure, size, collection method, and collection time. They do not need to correspond to the five papers in Part 1.

The five papers below do not duplicate the eight papers already reviewed in `TikTok_research_warmup.md`. Paper details were checked against the full text and official proceedings records. Dataset details were checked against the current repository, README, codebook, collection code, or data report. “Not reported” means that the source does not provide the figure; no estimate has been substituted.

## Part 1 — Five additional papers on TikTok

### 1. Gong et al. (2025), *ClipMind: A Framework for Auditing Short-Format Video Recommendations Using Multimodal AI Models*

**Reference.** Aoyu Gong, Sepehr Mousavi, Yiting Xia, and Savvas Zannettou. [ICWSM 2025, pp. 671–687](https://ojs.aaai.org/index.php/ICWSM/article/view/35838), DOI 10.1609/icwsm.v19i1.35838.

**Question and method.** The paper asks whether a scalable multimodal framework can detect topical concentration and possible “rabbit holes” in short-video recommendations. Five Playwright-controlled TikTok accounts collected For You Page sequences from a US IP between November 2023 and January 2024. One account behaved randomly; four were trained on Food, Beauty Care, Mental Health, or War/Military. Each trace contained 500 recommended videos, giving 2,500 videos in total. ClipMind represented visual, audio, platform-text, and AI-generated features as embeddings and analysed similarity over sliding windows.

**Findings.** Food and Beauty Care traces became substantially more internally similar than the random trace. The Mental Health and War/Military traces did not show the same concentration, so this experiment found no evidence of extreme-content rabbit holes for those two topics. This is evidence about five controlled traces, not proof that such rabbit holes never occur.

**Limitations.** The audit covers one platform snapshot, five accounts, four selected interests, and a US network location. It does not measure demographic effects or recommendation diversity directly. Part of the pipeline depends on closed AI models; the authors report about USD 30 in model costs for the analysed traces.

**AI relevance and reason to read.** It offers a reusable way to combine video, audio, text, embeddings, and sequence analysis for recommender-system auditing. It is especially useful for understanding how an AI audit operationalises “similar recommendations” rather than relying only on hashtags.

### 2. Yan and Wu (2026), *Auditing Algorithmic Personalization in TikTok Comment Sections*

**Reference.** Yueru Yan and Siqi Wu. [ICWSM 2026, pp. 2595–2606](https://ojs.aaai.org/index.php/ICWSM/article/view/42769), DOI 10.1609/icwsm.v20i1.42769. The authors also release [audit code](https://github.com/raye22/tiktok_personalization).

**Question and method.** This study moves beyond the For You Page and asks whether TikTok personalises the comments and comment order shown to politically different users. The researchers created 20 partisan sock-puppet accounts and five cold-start controls. Seventeen partisan accounts were successfully validated through their recommended videos. On 15 April 2025, the 17 validated and five control accounts inspected 65 politically neutral election videos; for each account–video pair, the script retained the first 50 observed top-level comments with rank, text, likes, and reply counts.

The test videos came from an auxiliary corpus of 4,691 election-related videos posted by 257 verified US political-media channels between 7 October and 5 November 2024. Candidate videos were screened for substantial left- and right-leaning discussion using GPT-4o classifications, with human validation.

**Findings.** Different account groups usually saw similar sets of top comments. However, comment **ranking** diverged more strongly between political groups for some videos, especially where discussion volume, engagement inequality, or partisan imbalance was high. An exploratory five-video analysis found some politically aligned exposure, but the pattern was not universal.

**Limitations.** The audit used search-and-watch training but not follows, likes, location changes, or direct comment interactions, so it may underestimate personalisation. The final analysis covers only 65 older videos and 22 accounts; baseline comments also leaned left. The results therefore demonstrate context-dependent ranking effects, not platform-wide prevalence.

**AI relevance and reason to read.** The paper is a clear example of causal-style black-box auditing, ranked-list comparison, and LLM-assisted political labelling. It is worth reading because comment ranking is an often-overlooked recommender system that can shape which opinions appear prominent.

### 3. Greenfield et al. (2026), *What’s Political on TikTok? Perceptions, Prevalence, and Patterns of Exposure to TikToks Users Perceive as Political*

**Reference.** Jason Greenfield, Stephanie T. Wang, Samuel Jung, Sanjana Gautam, Kevin Yang, and Danaé Metaxa. [ICWSM 2026, pp. 939–956](https://ojs.aaai.org/index.php/ICWSM/article/view/42675), DOI 10.1609/icwsm.v20i1.42675. The data-collection extension is [open source](https://github.com/Penn-HCI/tiktokpolperception).

**Question and method.** Instead of defining political content from the top down, the authors ask what TikTok users themselves regard as political, how much of it they encounter, and how exposure varies across users. From July to September 2023, 366 US adults recruited through Prolific used a browser extension on their own logged-in feeds. Each participant annotated at least 40 videos as explicitly political, implicitly political, or neither and supplied a short explanation.

The final sample contains 15,154 participant annotations of 11,312 unique TikToks. Researchers qualitatively coded the explanations into 32 political topics and related exposure patterns to participant attributes.

**Findings.** Participants perceived an average of 16.85% of their feeds as political. Older age and greater political interest were associated with more overall perceived-political content. Gender and ideology were associated with exposure to content about gender and sexuality rights. The study also shows that people can disagree about whether the same content is political.

**Limitations.** The adult US sample is not representative of either the country or TikTok’s full user base and excludes teenagers. Some topic categories are too small for well-powered comparisons. The observational design cannot separate algorithmic personalisation from user behaviour or differences in interpretation.

**AI relevance and reason to read.** This paper provides a valuable human-centred counterpoint to automated political-content classifiers. It is useful when designing labels or evaluation sets because it shows that “political” is partly a perception, not merely an objective binary class.

### 4. Galdeman and Aiello (2025), *Mapping the Climate Change Landscape on TikTok*

**Reference.** Alessia Galdeman and Luca Maria Aiello. [ICWSM 2025 poster paper, pp. 2614–2621](https://ojs.aaai.org/index.php/ICWSM/article/view/35962), DOI 10.1609/icwsm.v19i1.35962.

**Question and method.** The authors ask which climate topics appear on TikTok and which non-climate topics might act as gateways into climate discussion. They built a ten-part climate taxonomy from prior research, found 105 specialist seed accounts, extracted 193 relevant hashtags, and queried the official TikTok Research API. The initial collection contained 1,326,684 videos from 199,968 users; the final topic analysis used 590,361 videos with sufficiently long English descriptions. Creator profiles and a follower network were also constructed.

**Findings.** Lifestyle and dietary choices dominate the observed climate-related discourse. Semantic links suggest that topics such as healthy cooking, lifestyle, nature, oceans, travel, and some political themes may connect audiences to climate discussion.

**Limitations.** API volume restrictions limited the three-month retrieval process. Hashtag selection, seed accounts, English-description filtering, manual taxonomy design, and quota sampling all shape the result. The study maps published content, not what representative users actually saw.

**AI relevance and reason to read.** It combines a literature-derived taxonomy, topic modelling, semantic similarity, and network structure. It is a compact example of using AI to organise a large social-media corpus while keeping the assumptions behind the taxonomy visible.

### 5. Ling, Gummadi, and Zannettou (2023), *“Learn the Facts about COVID-19”: Analyzing the Use of Warning Labels on TikTok Videos*

**Reference.** Chen Ling, Krishna P. Gummadi, and Savvas Zannettou. [ICWSM 2023, pp. 554–565](https://ojs.aaai.org/index.php/ICWSM/article/view/22168), DOI 10.1609/icwsm.v17i1.22168.

**Question and method.** The paper examines how accurately TikTok’s soft-moderation warning labels were applied to COVID-19 videos. On 29 May 2021, the researchers expanded from `#coronavirus` and `#vaccine` to 26 co-occurring COVID-related hashtags and scraped 41,583 popular search results. Metadata included creator and publication time, engagement counts, URL, description, and warning-label status. Two researchers then performed a detailed thematic analysis of 222 English COVID-related videos drawn from a random sample of 500.

**Findings.** Forty-six percent of the full corpus had a warning label, and 99% of videos containing `#coronavirus` were labelled. Among the manually analysed data, 37.3% contained benign information despite a warning, while 7.7% contained misinformation or harmful information without a warning. Thirty-five percent of harmful/misleading items that needed a label were framed as entertainment or humour.

**Limitations.** TikTok search returned a popularity-ranked and non-representative sample. Hashtag sampling excludes untagged COVID content, and the qualitative analysis was small and English-only. The study infers likely hashtag-based moderation from observed patterns but cannot inspect TikTok’s internal classifier.

**AI relevance and reason to read.** It demonstrates the practical costs of false positives, false negatives, and overly generic safety labels. It is useful for moderation research because it connects platform-scale measurements with human review of actual meaning and risk.

### Short synthesis of the five papers

Together, the papers show five different ways of studying TikTok. ClipMind audits recommendation sequences; Yan and Wu audit comment ranking; Greenfield et al. foreground users’ subjective judgements; Galdeman and Aiello map a public issue through text and networks; and Ling et al. evaluate platform moderation. The common lesson is that the sampling frame matters: a For You feed, a comment ranking, a participant’s feed, a hashtag corpus, and search results represent different platform processes and cannot be interpreted as equivalent evidence.

## Part 2 — TikTok datasets

The following three datasets were selected independently of Part 1. All three resource pages were reachable at the check date, but “available” has different meanings: some provide only IDs, while others provide metadata and annotations.

### Dataset A — 2024 US Presidential Election TikTok Dataset

**Available link:** [GitHub repository](https://github.com/gabbypinto/US2024PresElectionTikToks) and [associated paper](https://arxiv.org/abs/2412.15583).

- **Availability:** Public GitHub repository. It releases TikTok IDs, collection scripts, and query terms. Whisper transcripts are linked in a public Google Drive folder. Raw videos are not redistributed. Rehydrating current posts requires TikTok access and many historical IDs may no longer resolve. No licence file was found in the repository.
- **Structure:** Overlapping CSV snapshots of video IDs; scripts for Research API metadata collection; keyword and hashtag lists for successive election phases. The paper describes a richer internal corpus containing IDs, captions/descriptions, timestamps, region, music, hashtags, usernames, engagement counters, platform transcripts, downloaded videos where available, and Whisper transcripts. Public transcript files are separate from the CSVs. The release does not contain a row-level corpus of 161,892,802 comments; that paper figure is an aggregate of `comment_count` metadata.
- **Size:** Paper snapshot: 3,144,836 videos, 485,343 transcripts, and 693,826 unique users. Repository update dated 13 February 2025: 4,069,908 IDs through 20 January 2025. The three current CSV snapshots occupy about 201.4 MiB in total, but they overlap and must not be concatenated as separate observations. Later account and transcript counts are not reported.
- **Collection method and time:** Official TikTok Research API with US-region election keywords/hashtags and event-based date phases; PyKTok was used to download live videos and Whisper for ASR. The paper’s publication window is 1 November 2023–16 October 2024; the later release extends it to 20 January 2025. Exact wall-clock crawl start and finish times are not reported. Repository releases ran from June 2024 to February 2025.
- **Main limitations:** Keyword/search corpus rather than a sample of recommendations; API caps and missingness; changing engagement counters; overlapping versions; public data are much thinner than the internal multimodal corpus; no explicit repository licence.

### Dataset B — News on TikTok

**Available link:** [current GESIS version-2 data report and files](https://access.gesis.org/sharing/2863/6674) and [dataset paper](https://ojs.aaai.org/index.php/ICWSM/article/view/35953).

- **Availability:** Open download from GESIS under CC BY 4.0. The release contains a CSV, PDF codebook, and PDF data report. IDs and URLs can be inspected without application, but source videos remain on TikTok and may disappear.
- **Structure:** One row per sampled video. Metadata include video ID, music ID, creation time, like/view/comment/share counts, hashtags, URL, outlet, and country. Twenty-five human-coded variables cover news status, visual style, text overlays, audio, interaction cues, topics, actors, and journalism news values. It does **not** include raw video, audio files, descriptions/captions, transcripts, OCR text, or comment text.
- **Size:** 8,623 videos from 18 German-speaking news-outlet accounts; 7,978 news videos received the complete form/content coding. No downloadable-media size is applicable, and repository storage size is not reported. There are no comment rows—only a comment-count field.
- **Collection method and time:** The sample contains every second video published during 2023 by the selected outlets in Germany, Austria, and Switzerland. Metadata were obtained with the official Research API in January 2024 and cross-checked with the Zeeschuimer browser extension, which added 64 missed videos. Human coding took place from September 2024 to February 2025; the first public release followed in 2025.
- **Main limitations:** Fixed list of professional outlets rather than all TikTok news; engagement is a later snapshot; no media or descriptions for independent multimodal reanalysis; deletion produces link rot.

### Dataset C — PoliTok-DE

**Available link:** [Hugging Face dataset](https://huggingface.co/datasets/tomasruiz/PoliTok-DE) and [paper](https://arxiv.org/abs/2509.15860).

- **Availability:** Public and ungated under CC BY 4.0. The public release provides post IDs, deletion/availability snapshots, 935 Saxony annotations, and a hydration script. It does not directly provide raw video, image, audio, or complete metadata. The script can retrieve still-live posts; stored deleted content is request-only for academic research.
- **Structure:** Two Parquet ID tables contain `post_id`, collection name, dated availability values, and TikTok status codes. A third Parquet file contains human labels for a Saxony subset. Hydration writes media (video, or image plus audio), a progress log, and metadata for successfully retrieved posts.
- **Size:** 938,961 released post IDs: 195,373 for the 2024 Saxony election and 743,588 for the 2025 federal election. Adding 935 annotation rows gives the 939,896 rows displayed by Hugging Face across its three configurations. The three Parquet files occupy about 12.5 MB. Unique creators and comments are not reported.
- **Collection method and time:** Daily official Research API keyword queries with `region=DE`; each publication day was queried 96 hours later to allow API indexing. Researchers then scraped live media/metadata and performed later re-scrapes. Publication windows are 1 July–30 November 2024 (Saxony) and 13 January–30 April 2025 (federal). Saxony availability snapshots are dated 2 October 2024, 10 December 2024, and 13 January 2025; the federal snapshot is 11 June 2026.
- **Main limitations:** Keyword matching misses politics expressed only in audio or images; posts deleted before API indexing are absent; hydration cannot recover unavailable posts; re-scrapes are snapshots; deletion cause cannot always be known; creator counts are absent.

## Dataset comparison table

| Dataset and topic | Availability and licence | What is actually released? | Size, accounts, posts, comments | Crawl source and method | Publication window / actual collection time | Main limitations |
|---|---|---|---|---|---|---|
| [US 2024 Presidential Election](https://github.com/gabbypinto/US2024PresElectionTikToks) — US election discourse | Public IDs/scripts; separate public Whisper transcripts; hydration/API access needed; **no repository licence stated** | Overlapping ID CSVs, query terms, scripts; no raw video. Internal paper corpus had metadata, captions and transcripts. | Paper: **3,144,836 videos**, **693,826 users**, **485,343 transcripts**. Repo 13 Feb 2025: **4,069,908 IDs**. CSV snapshots: **~201.4 MiB**, overlapping. No public comment rows. | Official Research API, US-region keyword/hashtag and date-phase queries; PyKTok; Whisper ASR | Posts: **1 Nov 2023–16 Oct 2024** in paper; repo extends to **20 Jan 2025**. Exact crawl period **not reported**; releases Jun 2024–Feb 2025. | Search/API bias, caps and missingness; IDs can decay; version overlap; public release is not the full internal corpus. |
| [News on TikTok](https://access.gesis.org/sharing/2863/6674) — German-language professional news | Direct GESIS download; **CC BY 4.0** | CSV metadata and 25 human-coded variables; IDs/URLs; no video, audio, captions, transcripts, OCR, or comment text | **18 accounts; 8,623 videos**; 7,978 fully coded news videos. Storage **not reported**. Comments: **none**, only count metadata. | Official Research API, account-based sampling; Zeeschuimer cross-check (+64) | Posts: **2023**. API crawl: **Jan 2024**. Annotation: **Sep 2024–Feb 2025**. | Selected outlets only; engagement snapshot; source media absent; link rot. |
| [PoliTok-DE](https://huggingface.co/datasets/tomasruiz/PoliTok-DE) — German elections and deletion | Public ID/status/annotation Parquet and hydration code; deleted stored media request-only; **CC BY 4.0** | IDs and dated availability/status; 935 annotations. Media and metadata only through hydration if still live. | Creators **not reported**; **938,961 IDs** + 935 annotation rows; **12.5 MB** public files; comments **not reported**. | Daily Research API keyword queries (`region=DE`) 96 hours after publication; web hydration; later re-scrapes | Posts: **1 Jul–30 Nov 2024** and **13 Jan–30 Apr 2025**. Rechecks through **11 Jun 2026**. | Keyword/API-lag bias; deleted content cannot hydrate; time-specific deletion measures; no creator count. |

## Practical conclusion

For immediate research use, **News on TikTok** is the cleanest labelled tabular dataset. **PoliTok-DE** is the strongest choice for studying deletion and temporal availability, provided that ID hydration is acceptable. The **US election dataset** offers the largest scale but requires careful version management and has no stated repository licence. None of these three directly redistributes a complete raw-video collection.

The most important reporting rule is therefore to avoid writing only “the dataset is public.” A reproducible description should state whether the public object is raw content, metadata, annotations, IDs, hydration code, or a controlled-access archive, and should record both the content-publication window and the actual retrieval date.

## Validation notes

- Full text and official ICWSM records were checked for all five papers.
- Dataset pages and links were checked on 2 September 2026. The check confirms page/file availability and semantic relevance; it does not mean that every TikTok ID was hydrated or every multi-gigabyte dataset was downloaded.
- Counts that changed between a paper snapshot and a later repository release are reported with their corresponding dates.
- The five papers were compared with the eight headings in `TikTok_research_warmup.md`; no duplicate paper was found.
- No existing research note was modified, and nothing was committed or published.
