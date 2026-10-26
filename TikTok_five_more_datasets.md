# Five More TikTok Datasets

Availability and links were checked on **17 September 2026**.

## Scope

This note describes five TikTok datasets that are additional to the three datasets in the earlier report: the 2024 US Presidential Election dataset, News on TikTok, and PoliTok-DE. It is a dataset search and description only. No statistical analysis was performed, and the datasets were not combined.

For each dataset, the note answers four practical questions:

1. Is it still available, and under what access conditions?
2. What is actually provided: raw videos, IDs, metadata, text, comments, or annotations?
3. How large is it?
4. How and when was it collected?

`Not reported` means that the official paper or repository does not give the number. It is not an estimate.

## 1. The Invasion of Ukraine Viewed through TikTok

**Topic.** TikTok activity related to Russia's invasion of Ukraine, including videos, comments, and user information.

**Available links.** [Official GitHub repository](https://github.com/networkdynamics/ukraine-tiktok), [Zenodo record](https://doi.org/10.5281/zenodo.7926959), and [paper](https://arxiv.org/abs/2301.08305).

### Availability

- The GitHub repository and Zenodo record are public.
- The public release mainly provides TikTok video IDs and collection scripts. It does **not** redistribute raw video files.
- Researchers must run the supplied scripts to request the current TikTok records. This is a hydration step: deleted, private, or otherwise unavailable posts cannot be recovered.
- No explicit dataset licence was found in the GitHub repository. The paper itself is available under CC BY 4.0, but that should not be treated automatically as the licence for the TikTok data.

### Dataset structure

The public release contains `video_ids.csv`, scripts, raw pre-filtering IDs, and a manually coded sample used to train the relevance filter. If hydration succeeds, the scripts create JSON responses and parsed CSV files.

The documented hydrated structure includes:

- video ID, creation time, author name and ID;
- description, hashtags, mentions, and duet/stitch information;
- like, share, comment, and play counts;
- comment ID, time, author, text, language, mentions, likes, and reply relation;
- user profile statistics such as follower, following, video, and like counts.

The release therefore gives IDs and tools for reconstructing metadata, comments, and user statistics. It does not provide video pixels, audio, OCR, or transcripts.

### Size

- Approximately **9,500 filtered videos**.
- Approximately **4.4 million collected comments**.
- Approximately **2.6 million comment-author accounts**.
- Number of distinct video creators: **not reported**.
- The eight files in the Zenodo release total **333,277 bytes**, about **0.32 MiB**. This small size is consistent with an ID-and-script release rather than a raw-media archive.

### Collection method and time

The researchers used their custom **PyTok** scraper. The software used browser automation to obtain session cookies and then made TikTok web requests. They started with invasion-related hashtags and keyword searches, expanded the search terms, filtered the results for relevance, and collected comments for the selected videos. The paper notes a maximum of 1,000 retrieved comments per video.

- Main content period: mainly **2022**, with additional early-2023 material in the updated collection.
- Initial collection: **July 2022**.
- Repeat/update collection: **April 2023**.
- Exact start and end timestamps of each crawl: **not reported**.

### Important limitations

- It is a search- and hashtag-based corpus, not a representative sample of all TikTok users or recommendations.
- Search popularity and platform ranking can influence which posts appear.
- The paper reports that roughly 29–30% of previously collected videos were unavailable about six months later, so reconstruction becomes less complete over time.
- The hydrated records may contain public personal information and require careful ethical handling.

## 2. DeHate

**Topic.** Explicit and implicit hate in multimodal videos from TikTok and BitChute.

**Available links.** [Official GitHub repository](https://github.com/Multimodal-Intelligence-Lab-MIL/DeHate) and [ACM Multimedia 2025 paper record](https://doi.org/10.1145/3746027.3758272).

### Availability

- The annotation file `DeHate.xlsx` is publicly downloadable from GitHub.
- The actual videos are **not openly downloadable** from the repository. Researchers must complete an application form; accepted applicants receive a separate download link.
- The repository says that the data are for research purposes and must be handled confidentially.
- No explicit dataset licence file is shown in the repository. The publication is CC BY, but the restricted video package has separate access conditions.

### Dataset structure

The public Excel workbook contains cleaned video-level and segment-level annotations. The documented annotations include:

- platform: TikTok or BitChute;
- explicit hate, implicit hate, or non-hate label;
- timestamps locating the hateful segment;
- contributing modality: text, audio, visual, or a combination;
- targeted social group: race, gender, religion, sexual orientation, disability, or immigration.

The videos are multimodal, but raw video and audio are available only through the application process. The public repository does not document a comment dataset, creator metadata table, transcripts, OCR output, or a set of TikTok IDs for independent hydration.

### Size

- **6,689 videos** in total across both platforms.
- TikTok subset: **1,637 videos** — 115 explicit-hate, 115 implicit-hate, and 1,407 non-hate videos.
- BitChute subset: **5,052 videos**.
- Public `DeHate.xlsx` file: **1,267,040 bytes**, about **1.21 MiB**.
- Size of the restricted raw-video package: **not reported**.
- Distinct TikTok creator accounts: **not reported**.
- Comments: **not reported and not documented as released**.

### Collection method and time

The official materials confirm that videos were collected from TikTok and BitChute and then annotated at both video and segment level. However, the public repository and accessible official publication record do not specify the TikTok search terms, API or scraper, exact crawl process, publication window, or collection dates.

- Crawling source and technical method: **not reported in the public repository**.
- Content publication window: **not reported**.
- Actual collection period: **not reported**.

### Important limitations

- Only 1,637 of the 6,689 videos come from TikTok, so the complete dataset is not a TikTok-only corpus.
- Raw media require approval and are not available through direct public download.
- There is no documented public ID list for reconstructing the TikTok subset.
- Creator counts, comments, crawl dates, and the restricted download size are not reported.
- The content is sensitive and can be disturbing to researchers and annotators.

## 3. RELIANCE

**Topic.** Reproductive-health information and misinformation in TikTok videos about pregnancy, postpartum health, and fertility.

**Available links.** [Official GitHub repository and data](https://github.com/realize-lab/RELIANCE), [project page](https://realize-lab.github.io/RELIANCE/), and [KDD 2026 paper](https://arxiv.org/abs/2606.18285).

### Availability

- The processed dataset is directly downloadable as `data.json` from GitHub without registration.
- The repository also publishes the `TikTik` collection tool.
- Raw videos, TikTok IDs, post URLs, creator IDs, and audio are not part of the released JSON.
- Because there are no post IDs or URLs in the released data, users cannot reconstruct the original TikTok corpus from this file.
- No explicit dataset licence was found in the repository. The paper is CC BY-SA 4.0; the collection tool contains its own restrictive notice, so users should not assume that one licence covers every repository component.

### Dataset structure

The released JSON contains **409 rows**. Its fields are:

- `query`: the reproductive-health search question;
- `sentence`: a selected sentence or paragraph from a TikTok video;
- `aggregated_acc`: aggregated clinician label for medical accuracy;
- `aggregated_harm`: aggregated clinician label for harmfulness;
- `categories`: health-information category labels;
- `stages`: pregnancy, postpartum, or fertility stage labels.

During collection, the researchers produced audio transcripts, visual descriptions, and OCR/in-video-text descriptions with Gemini 2.0 Flash. Those full intermediate multimodal records are described in the paper but are **not** included in the public `data.json`. The public dataset is therefore a de-identified textual claim-and-label dataset rather than a downloadable video corpus.

### Size

- **336 TikTok videos** were sampled.
- **409 selected sentences or paragraphs** are released.
- **56 clinician-reviewed queries**.
- Each video received three expert annotations; the annotation team contained four clinicians.
- Public `data.json`: **459,676 bytes**, about **449 KiB**.
- Distinct creators/accounts: **not reported**.
- Comments: **not collected or released**.
- Raw-media storage size: **not applicable to the public release**.

### Collection method and time

The team created 56 health queries with clinician input and collected the top six TikTok search results for each query. They used a fresh account to reduce previous-personalisation effects and a semi-manual tool called **TikTik**. The study focused on English-language, United States-facing search results. Gemini 2.0 Flash generated transcript, visual-description, and in-video-text representations; clinicians then annotated the selected claims for accuracy and harm.

- Collection month: **January 2025**.
- Search depth: the **top six results per query**.
- Exact days and wall-clock crawl duration: **not reported**.

### Important limitations

- The corpus is a small snapshot of top search results, not a representative TikTok sample.
- It focuses on English-language US reproductive-health searches.
- The public release removes the source IDs and raw media, preventing reconstruction and independent multimodal checking.
- It contains expert labels but no engagement metadata, comments, creator statistics, or full platform metadata.

## 4. TikTok-10M

**Topic.** A large general-purpose collection of trending TikTok post metadata for short-video and multimodal research.

**Available link.** [Official Hugging Face dataset card and files](https://huggingface.co/datasets/The-data-company/TikTok-10M).

### Availability

- The dataset is public and ungated on Hugging Face.
- It can be loaded with the Hugging Face `datasets` library or downloaded as ten Parquet shards.
- The card labels the licence as **`other`** and does not provide clear standard licence terms.
- Despite the “multimodal” description, the Parquet files contain metadata and URLs, not embedded raw TikTok video or audio files.
- TikTok URLs and media-related URLs may stop working if source posts are deleted or changed.

### Dataset structure

The table has 55 documented columns, including:

- post ID, TikTok URL, collection time, creation time, and description;
- duet, stitch, advertisement, mute, sharing, and comment-status fields;
- like, save, comment, play, and share counts;
- duration and video-quality score;
- cover-image links;
- point-of-interest name, address, city, country, and category;
- user ID, avatar links, seller and verification indicators;
- hashtags/challenges;
- music ID, title, album, author, duration, originality flag, and audio-play URL.

There are no comment rows or comment texts; `comment_count` is only a number. The files also do not contain captions produced by speech recognition, OCR text, human annotations, or raw audiovisual files.

### Size

- Dataset-card claim: **10,000,000 posts**.
- Current Hugging Face viewer estimate on 17 September 2026: **6,654,004 rows**.
- The difference between the title/card claim and the current viewer estimate is unresolved; both values should be reported rather than treating them as identical.
- Ten Parquet shards: **9.78 GB** in total.
- Distinct creator accounts: **not reported**, although a `user_id` column is present.
- Comments: no comment records; only comment-count metadata.

### Collection method and time

The dataset card says that it contains trending content from **Spring 2025** and only posts associated with United States points of interest. It does not document the API, scraper, search procedure, sampling rule, exact collection dates, or total crawl duration.

- Content/collection period stated by the card: **Spring 2025**.
- Crawling source and method: **not reported**.
- Exact start/end dates and crawl duration: **not reported**.

### Important limitations

- The official card's 10-million claim does not match the present 6.65-million-row viewer estimate.
- It is biased toward trending content and US points of interest.
- The data card does not explain the crawler or sampling process sufficiently for exact replication.
- Raw media are not stored in the released Parquet files, and external URLs may decay.
- The licence label `other` is too vague for clear reuse conditions.
- This resource has a dataset card but no associated peer-reviewed paper listed on the official page.

## 5. The DSA's Blind Spot Audit Dataset

**Topic.** Advertising, influencer promotion, and profiling of minors in TikTok's For You feed.

**Available links.** [Official Zenodo dataset record](https://zenodo.org/records/18879043), [FAccT 2026 paper preprint](https://arxiv.org/abs/2603.05653), and [public analysis-code repository](https://github.com/kinit-sk/ai-auditology-advertising-and-minor-profiling-tiktok).

### Availability

- The Zenodo record is reachable, but the dataset is **restricted** rather than openly downloadable.
- Access is limited to researchers conducting non-commercial research. Applicants must use an academic email address and pass the authors' verification process.
- The Zenodo page does not expose the restricted files before approval and does not state a conventional open-data licence.
- The analysis code is public on GitHub.

### Dataset structure

The restricted package is documented as containing video excerpts and three CSV files:

- one main 31-column file of videos presented to simulated users;
- two files containing independent manual annotations used to check the automated advertisement classifier.

The main table includes session and video identifiers, collection timestamps, advertisement labels and type, advertisement topic, visual indicators, model reasoning, simulated-user topic and demographics, an agent identifier, anonymised video URL and author, video description, duration, transcript, and transcript language. Advertisement labels distinguish formal ads, disclosed promotional content, undisclosed promotional content, and non-ads.

The documentation does not describe a comment table. Because video identifiers, URLs, and authors are anonymised in the published schema example, the data should not be treated as a public ID list for hydrating the original TikToks.

### Size

- **7,095 video presentations** in the For You feed. This is a recommendation-record count and is not explicitly reported as 7,095 unique posts.
- **1,346 presentations** were classified as containing commercial content.
- **Eight sock-puppet accounts**: four matched minor/adult pairs.
- Distinct source videos: **not reported**.
- Distinct creator accounts: **not reported**.
- Comments: **not reported and not documented as collected**.
- Restricted package storage size: **not reported**.

### Collection method and time

The researchers created four pairs of automated TikTok accounts. In every pair, one account represented a minor aged 16–17 and the other an adult aged 20–21, with matching interests. The four interest profiles were beauty, fitness, gaming, and politics. Each bot used TikTok for one one-hour session per day. When a recommended video matched its assigned topic, the bot watched, liked, and bookmarked it; unrelated recommendations were skipped. Metadata, descriptions, hashtags, and visual frames were captured for every presented video. Automated advertisement classification was checked through manual annotation.

- Main collection period: **10 days in December 2025**.
- Daily collection time: **one hour per bot**.
- Location scope: one country/location, represented in the released schema as Germany (`DE`).
- Exact calendar start and end dates: **not reported**.

### Important limitations

- Eight synthetic accounts, four interests, one location, and ten days cannot represent all TikTok users.
- Automated behaviour may not perfectly match real teenage or adult behaviour.
- Advertisement labels are partly model-generated and can contain errors, although the researchers manually evaluated them.
- Recommendation records may contain repeated videos, so 7,095 should not be presented as a verified unique-video count.
- Access restrictions prevent immediate independent inspection, and the original accounts/URLs are anonymised.

## Summary table

| Dataset and topic | Availability and access | Released structure | Size | Accounts, posts, and comments | Collection method | Time | Main limitations |
|---|---|---|---|---|---|---|---|
| [Ukraine invasion](https://github.com/networkdynamics/ukraine-tiktok) — war and political interaction | Public IDs and scripts; hydration required; no raw video; no explicit repository licence | Video IDs; scripts can reconstruct video, comment, and user metadata; no transcripts/OCR/raw media | Zenodo files: **333,277 bytes** | ~**9,500 videos**; **4.4M comments**; **2.6M comment authors**; creator count **not reported** | PyTok web scraper; hashtag and keyword search; relevance filtering; comments capped at 1,000/video | Initial crawl **Jul 2022**; update **Apr 2023**; mainly 2022 posts | Search bias, link decay, incomplete reconstruction, personal-data risk |
| [DeHate](https://github.com/Multimodal-Intelligence-Lab-MIL/DeHate) — explicit and implicit hate | Public annotation XLSX; raw videos by application; dataset licence not stated | Video/segment labels, timestamps, modalities, target groups; no documented public ID/comment/transcript table | XLSX: **1,267,040 bytes**; raw-video size **not reported** | **1,637 TikTok videos** within 6,689 total; creators/comments **not reported** | TikTok and BitChute collection followed by fine-grained annotation; technical crawler/search method **not reported** | Publication window and crawl period **not reported** | Mixed-platform corpus, restricted media, missing crawl details, sensitive content |
| [RELIANCE](https://github.com/realize-lab/RELIANCE) — reproductive-health claims | Public JSON; no raw media, source IDs, or URLs; dataset licence not stated | Query, selected sentence/paragraph, medical-accuracy label, harm label, categories, stages | JSON: **459,676 bytes** | **336 videos**, **409 text units**, **56 queries**; creators **not reported**; no comments | Top six search results/query using fresh account and TikTik; Gemini-generated intermediate transcript/visual/OCR descriptions; clinician labels | **Jan 2025**; exact days/duration **not reported** | Small top-search snapshot; US/English scope; released data cannot reconstruct videos |
| [TikTok-10M](https://huggingface.co/datasets/The-data-company/TikTok-10M) — general trending posts | Public, ungated Parquet; licence `other`; URLs but no embedded raw video/audio | 55 metadata fields covering post, engagement, user, POI, music, and media URLs | **9.78 GB**; card says **10M**, viewer estimates **6,654,004 rows** | Account count **not reported**; no comment rows, only counts | Exact API/scraper and sampling method **not reported**; card says trending US-POI content | **Spring 2025**; exact dates/duration **not reported** | Count inconsistency, trend/geographic bias, weak provenance, link decay, unclear licence |
| [DSA's Blind Spot](https://zenodo.org/records/18879043) — ads and minor profiling | Restricted application for non-commercial academic research; public code; no open licence stated | Restricted video excerpts; 31-column interaction CSV; two manual-annotation CSVs; anonymised URLs/authors | Storage **not reported** | **7,095 presentations**, **1,346 ads**, **8 bot accounts**; unique posts/creators/comments **not reported** | Four matched minor/adult pairs; one hour/day; conditional engagement; captures metadata, descriptions, hashtags, and frames | **10 days, Dec 2025**; exact dates **not reported** | Small synthetic audit, one location, possible repeated videos, model-label errors, restricted access |

## Quick availability conclusion

The five datasets offer very different levels of access. TikTok-10M is the largest direct download but contains metadata rather than raw videos and has incomplete provenance. RELIANCE is directly downloadable but releases only de-identified text and expert labels. The Ukraine dataset provides IDs and reconstruction scripts, but successful hydration depends on whether posts still exist. DeHate openly provides annotations while placing videos behind an application. The DSA audit dataset is the most restricted: its files and video excerpts require approved academic, non-commercial access.

