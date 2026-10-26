# TikTok dataset download manifest

Initial availability verification: 2026-09-17. The four additional datasets below were downloaded and rechecked on 2026-09-22 (Europe/Berlin).

These CSV files are stored locally under `downloaded_datasets/`. They are not generated examples.

## U.S. 2024 Presidential Election TikTok IDs

Official repository: https://github.com/gabbypinto/US2024PresElectionTikToks

| Local file | Official direct download | Bytes | Local SHA-256 | Official Git blob check |
|---|---|---:|---|---|
| `us_election/TikTok_IDs_2025_Feb.csv` | https://raw.githubusercontent.com/gabbypinto/US2024PresElectionTikToks/main/data/TikTok_IDs_2025_Feb.csv | 81,398,163 | `7d381a8c5e125a43bc683958d02df0452fd52529642ca27a1d64a081628b6a9e` | Match: `2ae4bf092826ce3dea9bb08c3fbd98673d9b1289` |
| `us_election/TikTok_IDs_Memo1.csv` | https://raw.githubusercontent.com/gabbypinto/US2024PresElectionTikToks/main/data/TikTok_IDs_Memo1.csv | 35,986,663 | `a7edd643fd0b41cd596cdf03da22dc3ae9ac0b17a01770d7d471456de4da8a70` | Match: `0afc4e6eec400a2fc0e0fe2598133694ae6e6dc1` |
| `us_election/TikTok_IDs_v2.csv` | https://raw.githubusercontent.com/gabbypinto/US2024PresElectionTikToks/main/data/TikTok_IDs_v2.csv | 93,841,027 | `7158bd1f48183e13f997eb3c5682351677ad2f10b1a0ac07bb3a3b9a50376d56` | Match: `5f9c21d8551ccfd29172072dcb8acbc9506fea59` |

The official GitHub API file sizes and blob hashes match the local files exactly.

## News on TikTok (GESIS)

Dataset DOI: https://doi.org/10.7802/2819

Official v2 CSV: https://access.gesis.org/sharing/2863/6673

| Local file | Bytes | Local SHA-256 | Verification |
|---|---:|---|---|
| `gesis_news/TikTok-news_data_v2-0-0.csv` | 3,053,641 | `1ea8810709ba2c10aa086a9901e6bb73f788c832a5d3000300519583f53ac220` | A fresh official download was byte-for-byte identical on 2026-09-17. |

Supporting local documentation:

- `gesis_news/TikTok-news_codebook_v2-0-0.pdf`
- `gesis_news/TikTok-news_datareport_v2-0-0.pdf`

## Invasion of Ukraine on TikTok

Official repository: https://github.com/networkdynamics/ukraine-tiktok

| Local file | Bytes | Local SHA-256 |
|---|---:|---|
| `ukraine/video_ids.csv` | 315,343 | `d50a63b62f2641cdfda45c7af313c7030d245ae57deb7709b3bbfc1f02531b7f` |
| `ukraine/raw_video_ids.csv` | 621,886 | `7bc86632418cadf4cb92a85017127033380bbf576b33524a34e3799079645a87` |
| `ukraine/video_coding.csv` | 24,456 | `1228ae1ef3d310c19aeb0fc3cf088070529cd6e526d60888a5ca0a79911da79e` |
| `ukraine/ukraine_tiktok_dataset.zip` | 474,809 | `e96977c4437077bf985bb3377d677e77ec3ab07f2649853449bcdbdf6d05b34b` |
| `ukraine/README.md` | 7,265 | `ac2bb68ff012b04141f3e00849eb3cc23ae73172eeb93ca3b31141a6fe59d2cf` |

The official archive contains IDs, a manual relevance-coding sample, and hydration scripts. It does not contain the paper's 4.4 million comment rows. Current PyTok requires a previously authenticated TikTok account, so no anonymous comment hydration was performed.

## DeHate

Official repository: https://github.com/Multimodal-Intelligence-Lab-MIL/DeHate

| Local file | Bytes | Local SHA-256 |
|---|---:|---|
| `dehate/DeHate.xlsx` | 1,267,040 | `581bd48a4be39cb9a300b81c24788aad57a1539412d7300ee409c4bfdc0c90ee` |
| `dehate/README.md` | 9,816 | `d7859b21da94ad122753265527dc122e83758adcadbea018e08b4b758671c129` |

The public workbook is downloaded. The raw videos require an approved application and are not part of the local public-data copy.

## RELIANCE

Official repository: https://github.com/realize-lab/RELIANCE

| Local file | Bytes | Local SHA-256 |
|---|---:|---|
| `reliance/data.json` | 459,676 | `65445a19cae23532d657795b2e271f51a329f1a6cac8545830e4ba25aabec4d6` |
| `reliance/README.md` | 1,161 | `36b6cbe076e151fac2f5ea3db449222e61b536803a0cbed494cb2f2372e116cd` |

The JSON contains processed text units and expert labels. It does not include source video IDs, URLs, comments, or raw media.

## TikTok-10M

Official dataset: https://huggingface.co/datasets/The-data-company/TikTok-10M

All ten official Parquet shards were downloaded. They total **9,778,507,336 bytes (9.11 GiB)** and contain **10,000,000 rows**. Each shard opens successfully and reports exactly 1,000,000 rows and 55 columns.

| Local file | Bytes | Local SHA-256 |
|---|---:|---|
| `tiktok_10m/train-00000-of-00010.parquet` | 962,958,914 | `d0cdf39e55c6104c9b6d1eafcb280ee0ec73f1d9441ffeb0be6c8e71c9d810d3` |
| `tiktok_10m/train-00001-of-00010.parquet` | 985,597,059 | `5612564e790d65db49031e2b5ac475deee8078b377966c60c1fb1a1061f96379` |
| `tiktok_10m/train-00002-of-00010.parquet` | 990,419,541 | `461f10da20164e0ef78e572461b325ca58b1a0550c87fa53fbce5c6307420440` |
| `tiktok_10m/train-00003-of-00010.parquet` | 989,685,117 | `dc41df23072a49edfe2f875c6be9d18cb679849c36b658b15cc6d4d280cc5541` |
| `tiktok_10m/train-00004-of-00010.parquet` | 985,086,257 | `1ca58633b1ed49628f8a7959ab37be53ac0be85213aa7f29d2e0ed3dde315ed7` |
| `tiktok_10m/train-00005-of-00010.parquet` | 979,518,366 | `3ba5f950d8abebccca2702242198fa80f11769319e8495513d40910dfbc23a18` |
| `tiktok_10m/train-00006-of-00010.parquet` | 973,608,580 | `e2dd046073e3843447a85b06d077702b98750fc86fe07b060b01896fa82699b1` |
| `tiktok_10m/train-00007-of-00010.parquet` | 971,837,702 | `1e15d4741331cc2e05a143f3322b12252ea23219471b33a24a6760d27afa1b55` |
| `tiktok_10m/train-00008-of-00010.parquet` | 968,791,860 | `b2530c5aa6a2b82bef8aca3a20dabf358ee8eb224dbb9e8447e09cb0ae502059` |
| `tiktok_10m/train-00009-of-00010.parquet` | 971,003,940 | `f315508ac2187d790b3cc5df265d39f4c936e5ea2a100bc4db3d0c49bfc26ff5` |

These files contain metadata and external URLs, not embedded TikTok video, audio, or comment text.
