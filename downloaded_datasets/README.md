# Download the four TikTok datasets

This guide reproduces the public downloads used by the four analysis notebooks. Run the commands from the repository root (`/Users/wang/Documents/tiktok`). You need `curl`, about **10 GB of free disk space**, and a stable connection for TikTok-10M. No TikTok account is needed for the files below.

The commands save files into the directories expected by the notebooks. They download only published dataset files; they do not fetch live TikTok posts.

## Quick start

```bash
cd /Users/wang/Documents/tiktok
mkdir -p downloaded_datasets/ukraine downloaded_datasets/dehate downloaded_datasets/reliance downloaded_datasets/tiktok_10m
```

### 1. Ukraine invasion dataset

Source: [Network Dynamics Lab repository](https://github.com/networkdynamics/ukraine-tiktok).

```bash
curl -L --fail --retry 3 https://raw.githubusercontent.com/networkdynamics/ukraine-tiktok/main/video_ids.csv -o downloaded_datasets/ukraine/video_ids.csv
curl -L --fail --retry 3 https://raw.githubusercontent.com/networkdynamics/ukraine-tiktok/main/additional_data/raw_video_ids.csv -o downloaded_datasets/ukraine/raw_video_ids.csv
curl -L --fail --retry 3 https://raw.githubusercontent.com/networkdynamics/ukraine-tiktok/main/additional_data/video_coding.csv -o downloaded_datasets/ukraine/video_coding.csv
curl -L --fail --retry 3 https://raw.githubusercontent.com/networkdynamics/ukraine-tiktok/main/ukraine_tiktok_dataset.zip -o downloaded_datasets/ukraine/ukraine_tiktok_dataset.zip
curl -L --fail --retry 3 https://raw.githubusercontent.com/networkdynamics/ukraine-tiktok/main/README.md -o downloaded_datasets/ukraine/README.md
```

The ZIP contains the same ID and coding files plus the authors' collection scripts. The separate CSV files are convenient for [the Ukraine notebook](../Ukraine_TikTok_dataset_analysis.ipynb). The public package has **9,503 filtered video IDs**, not the paper's 4.4 million comment rows. To reconstruct current video metadata or comments, you would need to use TikTok access separately. The present [PyTok instructions](https://github.com/networkdynamics/pytok) require a logged-in account, and older collection scripts may need updating before they work with the current library. Deleted videos cannot be recovered by hydration.

### 2. DeHate

Source: [DeHate repository](https://github.com/Multimodal-Intelligence-Lab-MIL/DeHate).

```bash
curl -L --fail --retry 3 https://raw.githubusercontent.com/Multimodal-Intelligence-Lab-MIL/DeHate/main/DeHate.xlsx -o downloaded_datasets/dehate/DeHate.xlsx
curl -L --fail --retry 3 https://raw.githubusercontent.com/Multimodal-Intelligence-Lab-MIL/DeHate/main/README.md -o downloaded_datasets/dehate/README.md
```

The workbook has annotations for **6,689 videos**, including **1,637 TikTok videos**. It can be read by [the DeHate notebook](../DeHate_TikTok_dataset_analysis.ipynb). Raw videos are available only after the authors approve an application linked from their repository. The workbook has no comment counts or comment text.

### 3. RELIANCE

Source: [RELIANCE repository](https://github.com/realize-lab/RELIANCE).

```bash
curl -L --fail --retry 3 https://raw.githubusercontent.com/realize-lab/RELIANCE/main/data.json -o downloaded_datasets/reliance/data.json
curl -L --fail --retry 3 https://raw.githubusercontent.com/realize-lab/RELIANCE/main/README.md -o downloaded_datasets/reliance/README.md
```

The JSON has **409 annotated text units**. [The RELIANCE notebook](../RELIANCE_TikTok_dataset_analysis.ipynb) reads it directly. The released file has no source video IDs, URLs, raw videos, or comment fields.

### 4. TikTok-10M

Source: [TikTok-10M on Hugging Face](https://huggingface.co/datasets/The-data-company/TikTok-10M/tree/main/data).

Each of the ten Parquet files is about 1 GB. Download all ten for the full [TikTok-10M notebook](../TikTok_10M_dataset_analysis.ipynb):

```bash
for n in $(seq 0 9); do
  name=$(printf 'train-%05d-of-00010.parquet' "$n")
  curl -L --fail --retry 5 --retry-delay 2 \
    "https://huggingface.co/datasets/The-data-company/TikTok-10M/resolve/main/data/${name}?download=true" \
    -o "downloaded_datasets/tiktok_10m/${name}"
done
```

The ten files total **9,778,507,336 bytes (9.11 GiB)** in the copy downloaded on 22 September 2026. They contain **10,000,000 rows** with post IDs, creator IDs, descriptions, engagement counts, and other metadata. They do **not** contain raw video files or individual comments. The `comment_count` column lets the notebook calculate comments per video from a stored metadata snapshot. If a download is interrupted, rerun the affected file's `curl` command; `-o` replaces that file with a fresh download.

## Check your downloads

Check file sizes and compare SHA-256 hashes with [DOWNLOAD_MANIFEST.md](DOWNLOAD_MANIFEST.md):

```bash
du -sh downloaded_datasets/ukraine downloaded_datasets/dehate downloaded_datasets/reliance downloaded_datasets/tiktok_10m
shasum -a 256 downloaded_datasets/ukraine/video_ids.csv downloaded_datasets/dehate/DeHate.xlsx downloaded_datasets/reliance/data.json
shasum -a 256 downloaded_datasets/tiktok_10m/*.parquet
```

The manifest records the hashes of the downloaded 22 September 2026 versions. If an author updates a file, a new valid download may have a different hash. Check the official repository's current version before treating a mismatch as corruption. A successful `curl` response alone does not establish that a Parquet file is complete; the analysis notebook checks that all ten files open and reports their row counts.

## Run the notebooks

Open the notebook for the dataset you want in Jupyter and run all cells. The code expects the folder structure above. For a fresh Python environment, the required packages are `pandas`, `numpy`, `openpyxl`, `pyarrow`, `jupyterlab`, and `ipykernel`. Ukraine, DeHate, and RELIANCE do not need `pyarrow`; TikTok-10M does.

```bash
python3 -m pip install pandas numpy openpyxl pyarrow jupyterlab ipykernel
jupyter lab
```

These four notebooks analyse their datasets separately. Only TikTok-10M's public files support direct mean and median calculations for `comment_count`. The other public downloads do not provide per-video comment counts.
