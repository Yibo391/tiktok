# TikTok research review — warm-up

Prepared for Fraunhofer SIT — 20 August 2026

## Scope and reading status

This is a targeted narrative review, not a systematic review. I read the full text of the eight papers synthesised below and recorded each study's question, evidence, main finding and limitation. The review separates a study's observations from stronger claims about TikTok's internal ranking system or impacts on users. The papers cover 2021–2026; findings should therefore be treated as time-, interface- and region-dependent.

One useful corroborating source is [Pearson et al. (2025), *Beyond the Margin of Error: a Systematic and Replicable Audit of the TikTok Research API*](https://doi.org/10.1080/1369118X.2024.2420032). Its publisher abstract and bibliographic record were checked, but its full text was not accessible during this review, so it is not counted among the eight read papers or used for detailed conclusions.

## Papers read: review notes

### 1. [Boeker & Urman (2022), *An Empirical Investigation of Personalization Factors on TikTok*](https://doi.org/10.1145/3485447.3512102)

**Question and approach.** This early controlled audit asks which observable user signals affect For You Page (FYP) recommendations. The authors ran paired active/control sock-puppet accounts in 39 scenarios between late June and mid-August 2021, varying language, location, follows, likes and video-viewing rate. Their bot collected 30,436 posts and compared overlap in posts, hashtags, creators and sounds between the paired feeds.

**What it found.** Every tested factor changed recommendations. Following creators was the strongest tested signal, followed by viewing behaviour and likes; location had a larger effect than language. This is evidence that the then-observed feed responded to those behaviours, not a direct observation of ranking weights or objectives.

**Review assessment.** The paired design is a strong way to isolate a single behavioural treatment, but the result is bound to web bots, the selected signals, and a short 2021 observation window. It is a foundational audit-design paper, not a current description of TikTok’s production ranking.

### 2. [Zannettou et al. (2024), *Analyzing User Engagement with TikTok’s Short Format Video Recommendations using Data Donations*](https://doi.org/10.1145/3613904.3642433)

**Question and approach.** Rather than simulate users, this study analyses GDPR data donations from 347 active TikTok users recruited in early 2022. The donation covers 9.21 million video-view records from July 2020 to February 2022, along with likes, searches, shares, comments and network traces. The researchers subsequently retrieved available public metadata for 83.4% of unique watched-video URLs; the rest were deleted, private or otherwise unavailable.

**What it found.** Daily videos watched and inferred viewing time rose markedly over continued use. About 55% of recommended videos were not watched to completion, usually being skipped before halfway. Participants were more likely to like content from followed accounts, while content from non-followed accounts was watched through more often.

**Review assessment.** This is the strongest paper in the set for real exposure and user behaviour, but it does not establish what the recommender optimises: behaviour may reflect user preference, changing inventory and interface design as well as ranking. The donor sample is non-representative, metadata are incomplete, and the donated traces contain view starts rather than actual view duration.

### 3. [Mousavi, Gummadi & Zannettou (2024), *Auditing Algorithmic Explanations of Social Media Feeds: A Case Study of TikTok Video Explanations*](https://ojs.aaai.org/index.php/ICWSM/article/view/31376)

**Question and approach.** This audit examines TikTok's “Why this video” explanations: their types, accuracy and completeness. Forty-five Android sock-puppet accounts undertook controlled likes, shares and follows over three months. The study logged 69,000 video views, 32,000 unique videos and 128,000 explanations, then compared explanation claims with measured account behaviour and available video metadata.

**What it found.** Nearly 90% of viewed videos displayed two explanations; “popular in your country” appeared on more than 98%. Explanations tied to content were comparatively accurate, but engagement explanations contained both false positives and false negatives—for example, a comment-based explanation appeared for 34% of accounts that had made no comments. Only 9% of videos showed all explanations that were feasible under the measured conditions.

**Review assessment.** The paper supports a mismatch between surfaced explanations and observable conditions, not proof that TikTok's private internal rationale is false. It is a valuable transparency/accountability audit, with limitations from the three-month window and the simplified hashtag/sound/creator proxies for content similarity.

### 4. [Entrena-Serrano, Degeling, Romano & Çetin (2025), *TikTok’s Research API: Problems Without Explanations*](https://arxiv.org/abs/2506.09746)

**Question and approach.** This empirical report tests whether the official Research API returns metadata for videos known to exist through data donation and logged-out front-end collection. The initial donation comparison used about 260,000 video URLs; it was followed by individual re-queries, a one-week German FYP sample and repeated checks of ten videos.

**What it found.** Initially, 70,239 donated URLs returned no metadata. The authors report that 36% of this missing subset was no longer public, while 62.7% was still public but unavailable through the API. After retries, roughly one in eight of the original donation URLs remained unavailable for analysis. The study also identifies systematic gaps involving ads and certain accounts, including Canadian accounts.

**Review assessment.** This is strong practical evidence that API coverage needs to be measured, not assumed. It is a preprint/report rather than a peer-reviewed paper, and its donation and FYP samples are not a random census of TikTok; its missingness rates should therefore not be extrapolated platform-wide. The defensible conclusion is methodological: validate API retrieval against independently known URLs and report the gap.

### 5. [Steel, Parker & Ruths (2023), *The Invasion of Ukraine Viewed through TikTok: A Dataset*](https://arxiv.org/abs/2301.08305)

**Question and approach.** The authors build an event- and query-based corpus for studying TikTok discourse around Russia's invasion of Ukraine: 9,500 videos, 4.4 million comments and 2.6 million users. They use seed-and-snowball keyword/hashtag collection in English, Russian and Ukrainian, then illustrate language, topic and bot-related analyses.

**What it found.** The paper shows both the value and difficulty of this corpus type. Search appears to have a popularity ceiling of roughly 1,000 results and produces fuzzy matches (for example, “nato” can retrieve “naruto”). Applying a Twitter bot detector out of distribution labels 99.8% of accounts above a 0.5 threshold—an implausible result that demonstrates cross-platform feature failure rather than widespread bot prevalence.

**Review assessment.** The most important contribution is methodological humility: search-collected content is not representative of FYP exposure, and Twitter-derived bot models cannot simply be transferred to TikTok. The paper is useful for multilingual conflict research and reproducible collection, but not for causal recommender claims.

### 6. [Pinto, Burghardt, Lerman & Ferrara (2024), *GET-Tok: A GenAI-Enriched Multimodal TikTok Dataset Documenting the 2022 Attempted Coup in Peru*](https://arxiv.org/abs/2402.05882)

**Question and approach.** GET-Tok demonstrates a pipeline that turns a query-based political-event corpus into multimodal research material. From 50,631 API-discovered videos (20 November 2022–1 March 2023), the authors successfully downloaded 43,697 after losses from privatisation, slideshow format and invalid downloads. They used Whisper transcription and GPT-4 visual descriptions/stance labels for a selected 2,345-video subset.

**What it found.** TikTok's built-in transcripts covered only 1.4–15.3% of the corpus, showing why caption-only analysis misses much of the content. The pipeline makes speech and visual context more searchable and analysable, while providing a concrete crisis-data case study.

**Review assessment.** This is a useful model for multimodal collection and provenance capture, but the enhanced subset is much smaller than the full corpus. Whisper errors, omitted emoji/context, generated visual descriptions and GPT-4 stance labels require human validation before they become analytical ground truth. The working code repository remains available; the separately cited data repository was unavailable when checked on 20 August 2026.

### 7. [Mosnar et al. (2025), *Revisiting Algorithmic Audits of TikTok: Poor Reproducibility and Short-term Validity of Findings*](https://arxiv.org/abs/2504.18140)

**Question and approach.** This replication study re-runs an earlier TikTok personalisation audit and asks whether its conclusions remain stable. The reproduction took about five months and nine person-months. It varies the interaction scenario and the overlap metrics used to compare feeds, and it investigates whether web-interface actions were honoured.

**What it found.** The later audit found watch time to be the strongest signal; likes and follows showed an initial exploratory period then stronger exploitation after roughly 1,000 videos. Those results differ materially from the earlier audit, and changing the metric or scenario changes the conclusion. GDPR traces also suggested that likes/follows made through the web interface may not have taken effect in some conditions.

**Review assessment.** This does not falsify the earlier paper; it demonstrates that audit results can depend on platform time, interface, protocol and measurement. It is the key reason to treat a one-off audit as a dated measurement, preserve execution details, and repeat the protocol longitudinally. Its own hashtag-based metrics and possible bot detection remain limitations.

### 8. [Jamie, Ghasemian & Hosseinmardi (2026), *Seeking Help, Facing Harm: Auditing TikTok’s Mental Health Recommendations*](https://arxiv.org/abs/2601.08720)

**Question and approach.** This safety audit asks whether FYP recommendations distinguish initial distress expression from explicit help-seeking and whether they avoid harmful mental-health content. Thirty fresh US accounts followed a 2 × 3 design: initial query framing (distress or help-seeking) crossed with engaged, avoidant or passive subsequent behaviour. LLM-guided agents collected 8,727 FYP videos over 1–7 January 2026.

**What it found.** Engagement with mental-health content rapidly led to about 45% mental-health recommendations per day. Avoidant and passive accounts received a lower share (about 11–20%), but still encountered mental-health content. Help-seeking framing shifted recommendations towards supportive material, yet harmful content—including self-harm/suicide-related material—remained present. Avoidance reduced the volume more clearly than the risk composition.

**Review assessment.** This gives a concrete safety-research protocol, but the study uses fresh accounts, four seed queries and a seven-day horizon. Its automated relevance/harm/support classification has moderate performance, so high-stakes claims should receive human or clinical-expert validation and uncertainty reporting. It tests feed outcomes under its simulated behaviours, not clinical impact on real users.

## Cross-paper synthesis

The evidence points to a platform that must be studied as an **exposure system**, rather than solely as a repository of publicly searchable content. Keyword/API corpora show what can be retrieved; sock-puppet logs measure an experimental feed response; data donations reveal selected users’ actual exposures. They answer different questions and should not be pooled as if they were equivalent samples.

Personalisation is observable but unstable across time and method. The 2021 audit identified follows as its strongest treatment, while the later replication identified watch time. The appropriate synthesis is not a permanent ranking-factor list: follows, likes, viewing, language and location can all influence observed feeds, and the apparent strength of a signal can change with the interface, content supply and experimental design.

Multimodality is essential. Captions and hashtags omit speech, on-screen text, editing and visual claims. ASR/OCR/visual-description pipelines improve coverage, but generated features are measurement instruments with error—not labels to accept as truth. For security or safety research, validate them against human annotation, including language and format subgroups.

Finally, access infrastructure is part of the research object. The API study shows that missing retrieval can be systematic; reproducibility work shows that a faithful protocol may yield different results later. Every TikTok study should report date, region, device/interface, query/interaction protocol, data losses and validation checks.

## TikTok datasets and data-access options

“Dataset” here includes reusable releases and repeatable collection infrastructures. Static TikTok corpora are affected by deletion, privacy changes, geographic availability and platform changes. Availability status below was checked on 20 August 2026.

| Dataset / access route | Coverage and modalities | Access / main limitation |
|---|---|---|
| [TikTok Research API and codebook](https://developers.tiktok.com/products/research-api/) | Public videos/accounts; metadata, captions, hashtags, engagement, comments and account relations, subject to endpoint and scope. | Application-only for eligible not-for-profit researchers in the US, Europe and Brazil. Public videos from adult creators; excludes Canada; does not capture personalised-feed exposure. |
| [Ukraine discourse dataset](https://arxiv.org/abs/2301.08305) | 2022 invasion-related video descriptions, comments and user statistics; language/interaction and bot-analysis use case. | Event- and query-bound; search results are not FYP exposure. |
| [GET-Tok Peru pipeline](https://github.com/gabbypinto/GET-Tok-Peru) | Political-event corpus with video, transcripts, visual descriptions and stance enrichment described in the paper. | Code is public; the separately cited data repository returned 404 on the check date. Treat it as a pipeline, not an immediately downloadable corpus. |
| [CSMV / MSA-CRVI](https://github.com/IEIT-AGI/MSA-CRVI) | More than 100k manually annotated TikTok comments, visual feature tensors and raw video links; intended for comment-response sentiment. | Annotations CC BY-SA 4.0; code Apache-2.0; video links may no longer resolve. |
| [Coronavirus TikTok content-analysis data](https://datacatalog.hshsl.umaryland.edu/dataset/225) | #coronavirus sample from 20 September 2020, with expert misinformation coding and engagement variables. | Unrestricted spreadsheet; narrow historical health topic. |
| [MUD3](https://github.com/Syx1030/MUD3) | Privacy-preserving user-level dynamic data for depression detection: facial landmarks and low-level vocal descriptors rather than reconstructible raw video. | Application required; sensitive and purpose-specific. |
| [Vietnamese harmful-video dataset](https://huggingface.co/datasets/funa21/tiktok-data) | Crawled TikTok videos and metadata for harmful-content detection. | Vietnamese keyword/hashtag sample, no official split, CC BY-NC 4.0. |
| [Mental-health awareness aggregate dataset](https://zenodo.org/records/20646752) | Research-API collection for 2023–24; derived topic, sentiment and toxicity measures for videos/comments. | IDs, raw text and media removed: suitable for aggregate reproducibility, not content-model training. |
| [Digital-nomad identity dataset](https://github.com/kargam0167/TikTok) | Hashtag-based longitudinal metadata, captions and OCR text with hashed IDs and a removal process. | Six identity-related hashtags only; useful compliance example, not representative content. |

## A taxonomy for TikTok research and datasets

Use three independent axes rather than one flat list:

1. **Object of study:** content/culture; creators/communities; interactions/comments; recommendation/search; moderation/governance; advertising/commerce; security/privacy.
2. **Societal domain/risk:** health and youth safety; misinformation; politics/elections/conflict; hate and harassment; body image/addiction; consumer harm; cultural participation.
3. **Evidence/method:** API/metadata corpus; manual qualitative coding; computational multimodal analysis; sock-puppet audit; data donation; survey/experiment; policy/legal analysis.

For every dataset, record two further descriptors:

- **Modality:** metadata; caption/hashtags; comments; audio/ASR; OCR/on-screen text; frames/video; network; feed/exposure log.
- **Provenance and validity:** acquisition route; date/time/region/language; sampling query; deletion/compliance procedure; annotation process; known omissions; whether it describes available content or actually recommended exposure.

## Validation record — 20 August 2026

The literature synthesis above is based on full-text reading of the eight listed papers. Their claims were checked against the methods/results sections, not inferred from titles alone. The external links in the dataset table were checked for availability; publisher DOI resolvers may reject automated requests, so persistent DOI links are retained alongside working conference/arXiv/repository sources where relevant.

Availability validation does not reproduce the underlying experiments. It establishes the status of referenced access routes on the stated date; platform behaviour and dataset availability can subsequently change.
