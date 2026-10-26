# Sources for the five additional TikTok notebooks

Checked 2026-10-09. Run notebooks from the repository root or open them in Jupyter with the root as working directory. The notebooks use `pandas`, `numpy`, `pyarrow`, and `IPython`; no TikTok account is needed for the four already-downloaded public releases.

| Notebook | Local folder | Primary release | Access actually obtained |
| --- | --- | --- | --- |
| `PoliTok_DE_dataset_analysis.ipynb` | `downloaded_datasets/politok_de/` | [Hugging Face PoliTok-DE](https://huggingface.co/datasets/tomasruiz/PoliTok-DE) | Three Parquet files: two ID/status tables and Saxony annotations |
| `Climate_Change_TikTok_dataset_analysis.ipynb` | `downloaded_datasets/climate_change/` | [Zenodo 15131067](https://zenodo.org/records/15131067) | All five released files; Zenodo MD5 hashes matched |
| `German_Multimodal_TikTok_dataset_analysis.ipynb` | `downloaded_datasets/german_multimodal/` | [Weizenbaum Library](https://www.weizenbaum-library.de/items/04482f4d-3f73-44e9-859b-f815b089caab) | Four extracted CSVs now local: metadata and text/audio/video embeddings; counts verified in notebook |
| `TIDES_Influencer_TikTok_dataset_analysis.ipynb` | `downloaded_datasets/tides_influencer/` | [TIDES GitHub](https://github.com/skmtr1/TIDES-TikTok-Influencer-dataset) | All nine TikTok CSV files from `TikTok/dataset/` |
| `EDTok_TikTok_dataset_analysis.ipynb` | `downloaded_datasets/EDTok-A-Dataset-for-Eating-Disorder-Content-on-TikTok-main/` | [EDTok GitHub](https://github.com/cbickham3232/EDTok-A-Dataset-for-Eating-Disorder-Content-on-TikTok) | Full public repository: 43,040 IDs, a 50-ID sample, README and scripts; no comment/media rows |

To refresh the public releases, use the file URLs on the source pages above. The PoliTok-DE files are `data/saxony_2024/post_ids.parquet`, `data/federal_2025/post_ids.parquet`, and `data/saxony_2024/annotations.parquet`. The climate record has `videos.json`, `profiles.csv`, `network.csv`, `topics.json`, and `READ-ME.md`. Despite its extension, the released `topics.json` contains CSV text; the notebook reads it accordingly. TIDES uses `tiktok_influencers.csv`, `tiktok_videos-1.csv`, `tiktok_videos-2.csv`, and six feature files. EDTok publishes only IDs, so its comment and content analyses are marked unavailable.

Do not confuse paper-held data with public files. PoliTok-DE's raw media and detailed metadata need separate hydration or restricted access. EDTok's reported video and comment corpus is not distributed in its CSV. TIDES has comment-count fields but no individual comment rows.
