# GESIS News — video URLs per creator

One file per creator (news outlet account), one TikTok video URL per line. There are 18 files with 8,623 URLs in total.

- **Source:** `TikTok-news_data_v2-0-0.csv` (GESIS, [doi:10.7802/2819](https://doi.org/10.7802/2819)). URLs are from column `V2_video_link`, and creators are from `V3_news_outlet`.
- **Format:** URLs are as released, `https://www.tiktok.com/share/video/<video_id>`. Every URL is unique and matches its `M1_video_id`.
- **Unavailable videos are kept.** In the dataset, 69 videos were already coded as unavailable (`V5_news_classification = 77`). They are still listed, so that it is possible to check whether they can be retrieved.
- **Period:** all videos were posted between 1 Jan and 31 Dec 2023 and collected in Jan 2024.

| File | Country | URLs | of which coded unavailable |
|---|---|---:|---:|
| 20minuten.txt | CH | 1,853 | 19 |
| heute.at.txt | AT | 1,090 | 7 |
| blick.txt | CH | 754 | 9 |
| watson_news.txt | CH | 537 | 6 |
| derstandard.txt | AT | 444 | 11 |
| zeitimbild.txt | AT | 424 | 2 |
| bluenews.ch.txt | CH | 395 | 1 |
| kleinezeitung.txt | AT | 389 | 1 |
| tagesschau.txt | DE | 388 | 0 |
| kurier.at.txt | AT | 365 | 4 |
| rtlaktuell.txt | DE | 365 | 1 |
| srfnews.txt | CH | 349 | 2 |
| krone.at.txt | AT | 305 | 0 |
| zeit.txt | DE | 284 | 2 |
| faz.txt | DE | 277 | 0 |
| neuezuercherzeitung.txt | CH | 157 | 1 |
| nachrichten.at.txt | AT | 126 | 1 |
| tagesanzeiger.txt | CH | 121 | 2 |
| **Total** | | **8,623** | **69** |

Follower counts are not in the GESIS release. To collect them, use the 18 account names (the file names without `.txt`).
