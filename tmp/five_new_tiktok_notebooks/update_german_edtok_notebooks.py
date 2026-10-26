"""Refresh the two existing English notebooks after local files became available."""

from pathlib import Path

import nbformat as nbf


ROOT = Path(__file__).resolve().parents[2]
NOTEBOOKS = ROOT / "Oct 9"


def md(text):
    return nbf.v4.new_markdown_cell(text)


def code(text):
    return nbf.v4.new_code_cell(text.strip())


def section(cells, title, purpose, source, interpretation):
    cells.extend([
        md(f"## {title}\n\n**Purpose:** {purpose}"),
        code(source),
        md(f"**What this shows:** {interpretation}"),
    ])


german_path = NOTEBOOKS / "German_Multimodal_TikTok_dataset_analysis.ipynb"
german = nbf.read(german_path, as_version=4)
cells = [md(
    "# German multimodal TikTok archive: analysis of the local CSV release\n\n"
    "[Weizenbaum data record](https://www.weizenbaum-library.de/items/04482f4d-3f73-44e9-859b-f815b089caab) · "
    "[Data report](https://www.weizenbaum-library.de/bitstreams/54049d98-d6c8-4c66-a890-6360118c22f9/download). "
    "This source is a data report, not a peer-reviewed paper. Its reported collection used a German IP and a logged-out TikTok Explore page from 31 July to 4 August 2023. "
    "The four released CSVs are now stored locally. We distinguish **Explore appearances** from **unique videos**, **comment-count snapshots** from **individual comments**, and **embeddings** from raw media. "
    "Run this notebook from the repository root or its `Oct 9` folder."
)]
section(cells, "1. Local files and schema", "Verify the four CSVs on disk and identify the metadata fields and analytical unit.", """
from pathlib import Path
import pandas as pd
from IPython.display import display

ROOT = Path.cwd()
if not (ROOT / 'downloaded_datasets').exists() and (ROOT.parent / 'downloaded_datasets').exists():
    ROOT = ROOT.parent
DATA = ROOT / 'downloaded_datasets' / 'german_multimodal'
names = ['meta_data.csv', 'text_embeddings.csv', 'audio_embeddings.csv', 'video_embeddings.csv']
files = pd.DataFrame([{'file': name, 'present': (DATA / name).is_file(),
                       'size_MB': round((DATA / name).stat().st_size / 1e6, 2) if (DATA / name).is_file() else None}
                      for name in names])
display(files)
missing = files.loc[~files.present, 'file'].tolist()
if missing:
    raise FileNotFoundError(f'Missing required local CSV files: {missing}')
metadata = pd.read_csv(DATA / 'meta_data.csv', dtype={'id_hash': str, 'author_hash': str}, low_memory=False)
print('Metadata columns:', metadata.columns.tolist())
print('Metadata rows:', len(metadata), 'distinct video hashes:', metadata.id_hash.nunique())
display(metadata.isna().sum().rename('missing_rows').to_frame())
""", "The metadata file contains engagement-count fields (`likes`, `comments`, `shares`, `plays`), categories, dates, hashtags and hashed IDs. It does not contain comment text or raw videos. Do not treat the 19 metadata columns as 19 independent variables with complete information: `hashtags` has missing values.")
section(cells, "2. Paper/release count reconciliation", "Reproduce the source's 11,242 appearance rows and 5,137 unique-video count, and check repeated appearances.", """
overview = pd.DataFrame([{
    'source_reported_appearance_rows': 11242,
    'local_appearance_rows': len(metadata),
    'difference_in_appearance_rows': len(metadata) - 11242,
    'source_reported_unique_videos': 5137,
    'local_unique_video_hashes': metadata.id_hash.nunique(),
    'difference_in_unique_videos': metadata.id_hash.nunique() - 5137,
    'unique_creator_hashes_across_appearances': metadata.author_hash.nunique(),
    'exact_duplicate_rows': int(metadata.duplicated().sum()),
}])
display(overview)
appearances = metadata.groupby('id_hash').size()
display(appearances.describe(percentiles=[.25, .5, .75, .9, .99]).to_frame('appearances_per_video'))
print('Videos appearing more than once:', int(appearances.gt(1).sum()))
""", "Both source-reported headline counts are exactly reproduced. A video appears 2.19 times on average; 3,676 video hashes occur more than once. Repeated appearances are not extra distinct videos or automatically duplicate data errors.")
section(cells, "3. Publication and scraping dates", "Separate when a video was posted from when researchers captured its Explore-page appearance.", """
metadata['scrape_date'] = pd.to_datetime(metadata.date_scraping, format='%d_%m_%Y', errors='coerce')
metadata['posted_at'] = pd.to_datetime(metadata.timestamp, errors='coerce')
print('Unparseable scrape dates:', int(metadata.scrape_date.isna().sum()))
print('Unparseable posting timestamps:', int(metadata.posted_at.isna().sum()))
print('Observed post-publication range:', metadata.posted_at.min(), 'to', metadata.posted_at.max())
display(metadata.groupby('scrape_date').agg(
    appearance_rows=('id_hash', 'size'), unique_videos=('id_hash', 'nunique'),
    unique_creators=('author_hash', 'nunique')).reset_index())
""", "The file covers five scraping days, 31 July–4 August 2023. The observed video publication timestamps range from 10 April to 31 July 2023. These are two different time windows.")
section(cells, "4. Categories and repeat observations", "Describe which Explore categories were captured and whether videos cross categories.", """
display(metadata.category.value_counts(dropna=False).rename_axis('category').to_frame('appearance_rows'))
print('Number of distinct categories:', metadata.category.nunique())
print('Videos observed in more than one category:',
      int(metadata.groupby('id_hash').category.nunique().gt(1).sum()))
print('Video-date pairs with multiple appearance rows:',
      int(metadata.duplicated(['id_hash', 'scrape_date']).sum()))
""", "There are 11 category labels with roughly 1,000 appearance rows each. In this release, a video hash is not observed under multiple category labels, and the same video is not repeated twice on a single scraping day. The labels `comedy_drame` and `entertaiment` are retained exactly as released.")
section(cells, "5. One observation per video and comment-count distribution", "Avoid counting repeated daily snapshots as different videos; use the last available scrape for each video.", """
latest = metadata.sort_values(['scrape_date', 'id_hash']).drop_duplicates('id_hash', keep='last').copy()
assert latest.id_hash.is_unique
print('Unique videos in latest-snapshot table:', len(latest))
print('Unique creators in latest-snapshot table:', latest.author_hash.nunique())
print('Video hashes associated with more than one creator hash:',
      int(metadata.groupby('id_hash').author_hash.nunique().gt(1).sum()))
print('Videos whose recorded comment count changed between observed days:',
      int(metadata.groupby('id_hash').comments.nunique().gt(1).sum()))
display(latest[['comments', 'likes', 'shares', 'plays']]
        .describe(percentiles=[.25, .5, .75, .9, .99]).round(2))
print('Videos with zero recorded comments:', int(latest.comments.eq(0).sum()))
""", "For the 5,137 unique videos, the last observed comment-count snapshot has a mean of about 3,187 and a median of about 1,254. These are **counts of comments attached to videos**, not rows of comment text. 2,698 videos have different comment counts on different observed days, so the choice of snapshot matters. The Explore sample strongly favors visible/popular material and should not be generalized to all TikTok videos.")
section(cells, "6. Comments by category", "Find descriptive differences across Explore categories using one snapshot per video.", """
by_category = latest.groupby('category').comments.agg(
    videos='count', mean_comment_count='mean', median_comment_count='median',
    zero_comment_share_percent=lambda s: 100 * s.eq(0).mean())
display(by_category.sort_values('median_comment_count', ascending=False).round(2))
print('Spearman rank correlation: comment count versus play count:',
      round(latest[['comments', 'plays']].corr(method='spearman').iloc[0, 1], 3))
""", "The `entertaiment` category has the highest median comment count (4,339); `cars` has the lowest (327). The comment–play Spearman correlation is about 0.682. These are associations in a selected Explore-page sample, not evidence that a category causes comments or that comment text is available.")
section(cells, "7. Creator concentration", "Check how many distinct sampled videos are associated with each hashed creator.", """
per_creator = latest.groupby('author_hash').size()
display(per_creator.describe(percentiles=[.25, .5, .75, .9, .99]).to_frame('unique_sampled_videos_per_creator'))
print('Creators with exactly one sampled video:', int(per_creator.eq(1).sum()))
""", "The one-video-per-creator median reflects this Explore sample, **not** a creator's complete posting history. The full appearance table has 2,992 creator hashes; the latest one-row-per-video table has 2,986. Six video hashes have different creator hashes across appearances. This is a data-quality caveat, not a reason to silently rewrite IDs.")
section(cells, "8. Text, audio and video embedding coverage", "Verify the dimensions, uniqueness, and metadata overlap of each derived modality without loading hundreds of megabytes of vectors.", """
embedding_rows = []
metadata_ids = set(metadata.id_hash)
for name in ['text_embeddings.csv', 'audio_embeddings.csv', 'video_embeddings.csv']:
    path = DATA / name
    header = pd.read_csv(path, nrows=0).columns.tolist()
    hashes = pd.read_csv(path, usecols=['id_hash'], dtype=str).id_hash
    embedding_rows.append({
        'file': name, 'rows': len(hashes), 'unique_video_hashes': hashes.nunique(),
        'numeric_embedding_dimensions': len(header) - 1,
        'repeated_video_hash_rows': int(hashes.duplicated().sum()),
        'overlap_with_metadata_videos': len(set(hashes) & metadata_ids),
        'coverage_of_metadata_videos_percent': 100 * len(set(hashes) & metadata_ids) / len(metadata_ids),
    })
display(pd.DataFrame(embedding_rows).round(2))
""", "All three embedding files contain exactly one row for each of the 5,137 hashed videos and join to the metadata at 100% by `id_hash`. Their dimensions are 512 (text), 4,096 (audio), and 2,304 (video). These vectors are derived numeric features, not descriptions, comment text, audio files, or playable videos.")
cells.append(md(
    "## Findings and limits\n\n"
    "- **Locally verified:** 11,242 appearance rows, 5,137 unique video hashes, 11 category labels, and 2,992 distinct creator hashes across appearance rows. The first two counts match the data report.\n"
    "- **Repeated observations:** 3,676 videos appear on more than one scraping day. Comment counts change across days for 2,698 videos. For video-level summaries, this notebook uses each video's **last observed scrape**, yielding 5,137 rows.\n"
    "- **Comments:** the last-snapshot mean is about **3,187** comments per video and the median is about **1,254**. These are metadata counts; there are **no individual comment rows**. Category comparisons and correlations are descriptive only.\n"
    "- **Multimodal data:** text/audio/video embeddings cover all 5,137 hashed videos, with 512/4,096/2,304 numeric dimensions respectively. They cannot reconstruct or substitute for raw media.\n"
    "- **Limits:** the collection is a logged-out German Explore-page sample, not all TikTok. Video URLs, descriptions, and unhashed IDs are not released. Six creator hashes present in the appearance table do not remain in the last-snapshot table; inspect such inconsistencies before creator-level linkage."
))
german.cells = cells
nbf.write(german, german_path)


edtok_path = NOTEBOOKS / "EDTok_TikTok_dataset_analysis.ipynb"
edtok = nbf.read(edtok_path, as_version=4)
cells = [md(
    "# EDTok: audit of the complete downloaded public repository\n\n"
    "[Paper](https://arxiv.org/html/2505.02250) · "
    "[Official GitHub repository](https://github.com/cbickham3232/EDTok-A-Dataset-for-Eating-Disorder-Content-on-TikTok). "
    "The complete repository is now present locally. The authors' public README states that only video IDs are distributed to comply with TikTok's terms; the paper's comments, creator metadata, and raw media are **not** in the downloaded repository. "
    "This notebook checks exactly what can be reproduced from that public release. Run it from the repository root or its `Oct 9` folder."
)]
section(cells, "1. Downloaded repository inventory", "Verify the actual files in the newly downloaded EDTok repository, including scripts and the sample ID file.", """
from pathlib import Path
import pandas as pd
from IPython.display import display

ROOT = Path.cwd()
if not (ROOT / 'downloaded_datasets').exists() and (ROOT.parent / 'downloaded_datasets').exists():
    ROOT = ROOT.parent
DATA = ROOT / 'downloaded_datasets' / 'EDTok-A-Dataset-for-Eating-Disorder-Content-on-TikTok-main'
required = [DATA / 'README.md', DATA / 'data' / 'metadata.csv',
            DATA / 'data' / 'sample_metadata.csv',
            DATA / 'scripts' / 'metadata_collection.py',
            DATA / 'scripts' / 'download_videos.py']
display(pd.DataFrame([{'file': str(p.relative_to(DATA)), 'present': p.is_file(),
                       'size_KB': round(p.stat().st_size / 1e3, 2) if p.is_file() else None}
                      for p in required]))
if not all(p.is_file() for p in required):
    raise FileNotFoundError('One or more expected public-repository files are missing.')
""", "This is the full downloaded public repository, not just a copied CSV. The Python scripts describe how to retrieve data under the appropriate access conditions; their presence does not mean they contain the authors' comments or videos.")
section(cells, "2. Full ID list versus sample ID list", "Check both CSV schemas, uniqueness, and whether the sample contains any new videos.", """
ids = pd.read_csv(DATA / 'data' / 'metadata.csv', dtype=str)
sample = pd.read_csv(DATA / 'data' / 'sample_metadata.csv', dtype=str)
old = pd.read_csv(ROOT / 'downloaded_datasets' / 'edtok' / 'metadata.csv', dtype=str)
display(pd.DataFrame([
    {'file': 'data/metadata.csv', 'rows': len(ids), 'columns': ', '.join(ids.columns),
     'unique_ids': ids.id.nunique(), 'blank_ids': int(ids.id.isna().sum())},
    {'file': 'data/sample_metadata.csv', 'rows': len(sample), 'columns': ', '.join(sample.columns),
     'unique_ids': sample.id.nunique(), 'blank_ids': int(sample.id.isna().sum())},
]))
print('Sample IDs also in full list:', len(set(sample.id) & set(ids.id)), 'out of', len(sample))
print('Full-list IDs identical to earlier local copy:', set(ids.id) == set(old.id))
""", "The full file contains 43,040 unique video IDs and the 50-row sample contains only IDs already in that full list. The new repository does **not** add content, comment rows, creator fields, or engagement metadata. The full ID set is identical to the earlier local copy.")
section(cells, "3. ID format and paper-count check", "Compare the public ID total with the paper's final-video count; do not infer inaccessible attributes from IDs.", """
clean = ids.id.fillna('').str.strip()
display(pd.DataFrame([{
    'public_rows': len(ids), 'unique_nonblank_ids': clean[clean.ne('')].nunique(),
    'paper_final_videos': 43040, 'difference_from_paper': len(ids) - 43040,
    'blank_ids': int(clean.eq('').sum()),
    'extra_duplicate_rows': int(clean[clean.ne('')].duplicated().sum()),
    'non_numeric_ids': int((~clean.str.fullmatch(r'\\d+')).sum()),
}]))
display(clean.str.len().value_counts().sort_index().rename_axis('id_length').to_frame('rows'))
""", "The 43,040 released IDs are distinct, nonblank, and 19 digits long, matching the paper's final-video count. An ID is a pointer, not a comment count or a claim that the post is still available today.")
section(cells, "4. What the repository does not contain", "Test whether substantive statistics can be calculated from its actual released columns.", """
requirements = {
    'Per-video comment mean and median': ['comment_count', 'comments'],
    'Unique creator count': ['author_id', 'username'],
    'Publication-month distribution': ['create_time', 'publish_time'],
    'Individual comment themes': ['comment_text', 'text'],
    'Views and likes': ['view_count', 'like_count'],
}
display(pd.DataFrame([{'analysis': name,
                       'needed_field_in_public_full_csv': any(col in ids.columns for col in columns)}
                      for name, columns in requirements.items()]))
print('Paper-reported: 10,897 users, 388,332 top-level comments and 188,739 replies.')
print('Locally reproducible from released CSVs: 43,040 distinct video IDs only.')
""", "All five substantive analyses remain unavailable from the downloaded repository. The paper's 577,071 comments-plus-replies total is a **paper-reported** number, not locally downloaded comment rows. Do not divide it by 43,040 and call the result an observed per-video mean.")
section(cells, "5. What the scripts would require", "State which files are scripts and what extra access or retrieval would be needed for richer data.", """
readme = (DATA / 'README.md').read_text(encoding='utf-8')
print('README says only video IDs are publicly released:',
      'only publicly releasing the TikTok Video IDs' in readme)
print('README mentions TikTok Research API:', 'TikTok Research API' in readme)
print('Local comment-row files:', [p.name for p in DATA.rglob('*')
                                  if p.is_file() and 'comment' in p.name.lower()])
print('Local raw video files:', [p.name for p in DATA.rglob('*')
                                if p.is_file() and p.suffix.lower() in {'.mp4', '.mov', '.webm'}])
""", "The README confirms an ID-only public release and says TikTok Research API access is required to retrieve metadata. There are no comment datasets or raw video files in this folder. Running the scripts would be a **new collection**, with possible access loss and platform-policy requirements, not analysis of already downloaded data.")
cells.append(md(
    "## Findings and limits\n\n"
    "- The complete local EDTok repository contains **43,040 distinct video IDs** in `data/metadata.csv`, matching the paper's final-video count. `sample_metadata.csv` contains **50 IDs**, all already in the full list.\n"
    "- The public repository adds scripts and documentation, **not** the authors' creator metadata, comment rows, engagement measurements, or raw videos. The earlier local ID copy has the same 43,040 IDs.\n"
    "- The paper reports **10,897 users**, **388,332 top-level comments**, and **188,739 replies**. Those figures cannot be independently verified from this ID-only release. Per-video comment mean and median are **not calculated**.\n"
    "- Recollection would need TikTok Research API access and a new retrieval date. It might not reproduce the paper's original corpus because availability and engagement can change."
))
edtok.cells = cells
nbf.write(edtok, edtok_path)

print(german_path)
print(edtok_path)
