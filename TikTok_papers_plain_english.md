# TikTok papers — plain English notes for an AI researcher

These notes explain each paper in simple English: what it says, how it connects to AI, and why it is useful for your TikTok research review at Fraunhofer SIT.

## 1. Boeker & Urman (2022) — Personalisation factors on TikTok

**What is this paper about?**

The authors created test TikTok accounts and gave them different behaviours. For example, some accounts followed creators, liked videos, watched longer, used another language, or appeared to be in another location. They then checked how the For You Page changed.

**Main message:** TikTok recommendations reacted to user behaviour. In this 2021 experiment, following creators had the strongest effect; watching and liking also mattered.

**Why is this related to AI?**

TikTok's recommender system is an AI system. This paper is an example of **algorithm auditing**: testing the behaviour of an AI system from the outside when we cannot see its source code or model.

**Why should I read it?**

It gives you a basic method for studying recommendations. It also teaches an important lesson: an experiment can show that a behaviour changes recommendations, but it cannot tell us the exact hidden ranking formula.

## 2. Zannettou et al. (2024) — Real users’ TikTok viewing behaviour

**What is this paper about?**

Instead of using fake accounts, the researchers used data voluntarily donated by 347 real TikTok users. They studied millions of video-view records: what people watched, skipped, liked, searched for and shared.

**Main message:** People skipped many recommended videos quickly. They liked videos from accounts they followed more often, but often watched videos from accounts they did not follow until the end.

**Why is this related to AI?**

AI recommendations only matter when people actually see and react to them. This paper connects a recommender system’s output with real human behaviour. It is useful for **human-centred AI** and recommendation evaluation.

**Why should I read it?**

It shows the difference between a controlled test account and a real person. If your research asks “what does TikTok show users?”, real exposure data are usually more meaningful than a simple keyword dataset.

## 3. Mousavi, Gummadi & Zannettou (2024) — “Why this video?” explanations

**What is this paper about?**

TikTok sometimes tells users why a video was recommended, for example “popular in your country.” This paper checks whether these explanations match what the account really did and what is known about the video.

**Main message:** Some explanations were incomplete or did not match the observed account behaviour. For example, some accounts received a comment-related explanation even though they had never commented.

**Why is this related to AI?**

This is about **explainable AI (XAI)** and AI transparency. An explanation is useful only if it is understandable, relevant and not misleading. This matters especially for accountable and trustworthy AI systems.

**Why should I read it?**

It gives you a direct link to Fraunhofer SIT topics: trustworthy systems, transparency, accountability and security. It also shows how to test an AI explanation instead of simply trusting it.

## 4. Entrena-Serrano et al. (2025) — Problems with the TikTok Research API

**What is this paper about?**

Researchers often use TikTok’s official Research API to collect data. This paper checked whether the API returned data for videos that researchers already knew existed. Sometimes it did not.

**Main message:** A video can still be public on TikTok but missing from the API. Therefore, API data may be incomplete in systematic ways.

**Why is this related to AI?**

AI results are only as reliable as the data used to create them. If the dataset is incomplete or biased, an AI model, analysis or benchmark may produce misleading results. This is a **data quality**, **dataset bias** and **reproducibility** problem.

**Why should I read it?**

Before training models or making claims from TikTok data, you need to know what data are missing. This paper tells you to validate your data collection, log failures, and avoid treating API results as the whole platform.

## 5. Steel, Parker & Ruths (2023) — TikTok data about the Ukraine war

**What is this paper about?**

The authors collected TikTok videos, comments and users related to Russia’s invasion of Ukraine. They used keywords and hashtags in English, Russian and Ukrainian, then explored language, topics and possible bot activity.

**Main message:** TikTok search data have important limits. Search results can be incomplete or contain irrelevant matches. A bot detector trained on Twitter gave unrealistic results on TikTok.

**Why is this related to AI?**

This is relevant to **NLP**, **multilingual AI**, **social-media analysis**, and **bot detection**. It also shows a classic AI problem: a model trained for one platform may fail badly on another platform. This is called poor generalisation or domain shift.

**Why should I read it?**

It is a useful warning before applying an existing AI model to TikTok. You need to validate models on TikTok-specific data rather than assume that a Twitter, Facebook or Reddit model will work.

## 6. Pinto et al. (2024) — GET-Tok: multimodal AI for a political event

**What is this paper about?**

The authors collected TikTok videos about the political crisis in Peru. They used AI tools to turn speech into text, describe visual content and estimate the political stance of videos.

**Main message:** Captions and hashtags alone are not enough. Important meaning is often in speech, on-screen text and visuals. AI transcription and visual analysis can make videos easier to search and study.

**Why is this related to AI?**

This is directly about **multimodal AI**: combining text, audio and video. It uses automatic speech recognition (Whisper) and large language models (GPT-4) as research tools.

**Why should I read it?**

It gives you a practical pipeline for analysing TikTok video content. It also teaches a key AI lesson: AI-generated labels and transcripts are not automatically correct. You need human evaluation before using them as ground truth.

## 7. Mosnar et al. (2025) — Why TikTok audits are hard to reproduce

**What is this paper about?**

This team repeated an earlier TikTok recommendation audit. They found different results even when trying to follow the original research idea closely.

**Main message:** The strongest personalisation signal changed from the earlier study. Results also changed when the researchers changed the metric or experimental setup. TikTok and its interface can change faster than research papers are published.

**Why is this related to AI?**

This is about **reproducible AI**, evaluation and measurement. AI systems deployed online are not fixed models: their data, policies, interfaces and behaviour can change over time.

**Why should I read it?**

It prevents overconfident conclusions. If you study TikTok, always record the date, region, device, account setup and method. A result should be presented as “what we observed then,” not as a permanent truth about the algorithm.

## 8. Jamie, Ghasemian & Hosseinmardi (2026) — Mental-health recommendations

**What is this paper about?**

The authors used test accounts that searched for mental-health content. Some accounts acted as if they were distressed; others explicitly asked for help. Then the accounts either engaged with, avoided or passively watched mental-health videos.

**Main message:** After engaging with mental-health content, the accounts received many more mental-health recommendations. Asking for help produced more supportive content, but harmful content could still appear. Avoiding the content lowered the amount but did not fully remove the risk.

**Why is this related to AI?**

This is about **AI safety**, recommender-system risk and high-stakes AI. An algorithm may shape what vulnerable users see. It also uses automated/LLM-based content classification, which needs careful validation.

**Why should I read it?**

It is a concrete example of how to study potential harm from recommender systems. For SIT, it connects AI evaluation with security, human wellbeing, risk management and trustworthy AI.

## The short story across all eight papers

You should read these papers because they cover the full AI research chain:

| AI research question | Papers that help |
|---|---|
| How does a recommender react to user behaviour? | 1, 2, 7, 8 |
| Can we trust an AI system’s explanation? | 3 |
| Can we trust the data used for AI research? | 4, 5 |
| How can we analyse video, audio and text together? | 6 |
| How do we evaluate safety and harm? | 3, 8 |

In one sentence: these papers help you study TikTok not only as a social-media app, but as a changing AI system whose recommendations, explanations, data access and possible risks all need to be measured carefully.
