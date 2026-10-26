"""Build five independent English notebooks from locally downloaded TikTok data."""

from pathlib import Path
import nbformat as nbf

ROOT = Path(__file__).resolve().parents[2]


def make(title, intro, folder, sections, findings, filename):
    nb = nbf.v4.new_notebook()
    nb.metadata.kernelspec = {"display_name": "Python 3", "language": "python", "name": "python3"}
    nb.metadata.language_info = {"name": "python"}
    nb.cells.append(nbf.v4.new_markdown_cell(f"# {title}\n\n{intro}"))
    nb.cells.append(nbf.v4.new_markdown_cell("## Local files and setup\n\n**Purpose:** Confirm which public files are actually present on this computer. File presence does not imply that raw media or comment rows are included."))
    nb.cells.append(nbf.v4.new_code_cell(f"""from pathlib import Path
import pandas as pd
from IPython.display import display

ROOT = Path.cwd()
if not (ROOT / 'downloaded_datasets').exists() and (ROOT.parent / 'downloaded_datasets').exists():
    ROOT = ROOT.parent
DATA = ROOT / 'downloaded_datasets' / '{folder}'
print('Local data folder:', DATA.resolve())
if DATA.exists():
    display(pd.DataFrame([{{'file': p.name, 'size_MB': round(p.stat().st_size / 1e6, 2)}}
                          for p in sorted(DATA.iterdir()) if p.is_file()]))
else:
    print('Local data folder is missing. Download the files first.')"""))
    for heading, purpose, code, interpretation in sections:
        nb.cells.append(nbf.v4.new_markdown_cell(f"## {heading}\n\n**Purpose:** {purpose}"))
        nb.cells.append(nbf.v4.new_code_cell(code.strip()))
        nb.cells.append(nbf.v4.new_markdown_cell(f"**What this shows:** {interpretation}"))
    nb.cells.append(nbf.v4.new_markdown_cell("## Findings and limits\n\n" + findings))
    nbf.write(nb, ROOT / filename)
    print(ROOT / filename)


make(
    "PoliTok-DE: German election TikTok data",
    "[Paper, arXiv v2](https://arxiv.org/html/2509.15860) · [Public ID release](https://huggingface.co/datasets/tomasruiz/PoliTok-DE). "
    "This notebook analyses released post IDs, availability snapshots, and Saxony annotation rows. "
    "Raw media, creator metadata, and comment rows are not in these public files. `DELETED` means not publicly accessible on a later check, not a confirmed policy violation.",
    "politok_de",
    [
        ("1. Structure and paper counts", "Compare the number of public post IDs with the revised paper, and distinguish annotation rows from annotated posts.", """
sax = pd.read_parquet(DATA / 'saxony_post_ids.parquet')
fed = pd.read_parquet(DATA / 'federal_post_ids.parquet')
ann = pd.read_parquet(DATA / 'saxony_annotations.parquet')
overview = pd.DataFrame([
    {'collection': 'Saxony 2024', 'public_rows': len(sax), 'unique_post_ids': sax.post_id.nunique(), 'paper_posts': 195373},
    {'collection': 'Federal 2025', 'public_rows': len(fed), 'unique_post_ids': fed.post_id.nunique(), 'paper_posts': 743588},
])
overview['difference_from_paper'] = overview.public_rows - overview.paper_posts
display(overview)
print('Overlapping post IDs:', len(set(sax.post_id) & set(fed.post_id)))
print('Annotation rows:', len(ann), 'unique annotated posts:', ann.post_id.nunique())
print('Public ID-file columns:', sax.columns.tolist(), fed.columns.tolist())
""", "Both public post counts match the paper's v2 counts. The 935 annotation rows refer to only 360 posts; a row is not necessarily a distinct post."),
        ("2. Final availability checks", "Calculate accessibility at each collection's last reported recheck; show the denominator explicitly.", """
rows = []
for name, frame, col in [('Saxony 2024', sax, 'availability_2025_01_13'),
                         ('Federal 2025', fed, 'availability_2026_06_11')]:
    counts = frame[col].value_counts()
    rows.append({'collection': name, 'recheck_date': col.replace('availability_', ''),
                 'all_ids': len(frame), 'AVAILABLE': int(counts.get('AVAILABLE', 0)),
                 'DELETED': int(counts.get('DELETED', 0)),
                 'UNKNOWN_ERROR': int(counts.get('UNKNOWN_ERROR', 0)),
                 'deleted_share_of_all_ids_percent': 100 * counts.get('DELETED', 0) / len(frame)})
display(pd.DataFrame(rows).round(2))
""", "The final `DELETED` shares are 18.74% (Saxony) and 39.69% (federal). The recheck dates differ, so the difference is not automatically an election effect. Saxony also has 2,014 `UNKNOWN_ERROR` IDs."),
        ("3. Saxony recheck waves", "Show how the number of conclusive checks changes across snapshots.", """
waves = []
for col in [x for x in sax.columns if x.startswith('availability_')]:
    counts = sax[col].value_counts()
    conclusive = int(counts.get('AVAILABLE', 0) + counts.get('DELETED', 0))
    waves.append({'recheck_date': col.replace('availability_', ''),
                  'AVAILABLE': int(counts.get('AVAILABLE', 0)), 'DELETED': int(counts.get('DELETED', 0)),
                  'NOT_RESCRAPED': int(counts.get('NOT_RESCRAPED', 0)),
                  'UNKNOWN_ERROR': int(counts.get('UNKNOWN_ERROR', 0)),
                  'conclusive_checks': conclusive,
                  'deleted_share_of_conclusive_percent': 100 * counts.get('DELETED', 0) / conclusive if conclusive else float('nan')})
display(pd.DataFrame(waves).round(2))
""", "The first wave has 92,420 `NOT_RESCRAPED` posts and only 102,949 conclusive results. Coverage differs across waves; a change in percentage is not a same-sample risk trend."),
        ("4. Human annotation and disagreement", "Separate individual votes from posts, and count posts with conflicting yes/no votes.", """
labels = ['is_political', 'is_saxony_election', 'is_intolerant',
          'is_hedonic_entertainment', 'is_eudaimonic_entertainment']
rows = []
for col in labels:
    votes = ann[col].str.lower().str.strip()
    valid = votes.isin(['yes', 'no'])
    per_post = ann.assign(vote=votes.where(valid)).groupby('post_id')['vote']
    rows.append({'label': col, 'valid_votes': int(valid.sum()),
                 'yes_share_of_valid_votes_percent': 100 * votes.eq('yes').sum() / valid.sum(),
                 'posts_with_disagreement': int((per_post.nunique(dropna=True) > 1).sum()),
                 'annotated_posts': ann.post_id.nunique()})
display(pd.DataFrame(rows).round(2))
display(ann.groupby('post_id').size().value_counts().sort_index()
        .rename_axis('annotation_rows_per_post').to_frame('post_count'))
""", "`is_intolerant=yes` accounts for about 20.49% of valid votes in this selected sample, not 20.49% of all election posts. Three posts have five annotation rows, while the paper says one to four annotators per post; the cause is not established."),
        ("5. Status-code combinations", "Inspect the technical codes accompanying inaccessible posts without treating all of them as platform takedowns.", """
for name, frame, av, sc in [('Saxony', sax, 'availability_2025_01_13', 'status_codes_2025_01_13'),
                            ('Federal', fed, 'availability_2026_06_11', 'status_codes_2026_06_11')]:
    codes = frame.loc[frame[av].eq('DELETED'), sc].fillna('')
    print(name, 'most common status-code combinations among DELETED IDs:')
    display(codes.value_counts().head(10).rename_axis('code_combination').to_frame('post_count'))
""", "The paper uses code patterns to infer creator withdrawals versus platform removal. A simple `DELETED` flag alone does not identify the reason."),
    ],
    "- The two ID files contain **195,373** and **743,588** distinct posts, matching paper v2; total **938,961**, with no overlap.\n"
    "- The last reported `DELETED` snapshots contain **36,617** Saxony posts (18.74% of all IDs) and **295,101** federal posts (39.69%). Recheck timing differs.\n"
    "- Saxony's first wave has **92,420** `NOT_RESCRAPED` posts; always specify the denominator.\n"
    "- The annotation file has **935** rows for **360** posts. The intolerance-vote share is **20.49%** among valid votes in a selected subsample, not the full corpus.\n"
    "- Public files omit creator metadata, captions, comments, and media; the paper's content-level analyses cannot be reproduced from these files alone.",
    "PoliTok_DE_dataset_analysis.ipynb",
)


make(
    "Climate change on TikTok: released-data analysis",
    "[Paper](https://arxiv.org/html/2505.03813) · [Zenodo release](https://zenodo.org/records/15131067). "
    "The release contains video topic/hashtag records, creator topic vectors, and a follower network, but no raw video, comment text, or engagement counts. "
    "This is a keyword- and language-filtered collection, not a random TikTok sample.",
    "climate_change",
    [
        ("1. File units and paper counts", "Identify the unit of each file, check duplicates, and inspect the actual format of `topics.json`.", """
import json
import numpy as np
from collections import Counter
with (DATA / 'videos.json').open(encoding='utf-8') as handle:
    videos = pd.DataFrame(json.load(handle))
profiles = pd.read_csv(DATA / 'profiles.csv')
network = pd.read_csv(DATA / 'network.csv')
topics = pd.read_csv(DATA / 'topics.json')  # Despite the extension, the released file is CSV text.
display(pd.DataFrame([
    {'file': 'videos.json', 'rows': len(videos), 'unit': 'video record'},
    {'file': 'profiles.csv', 'rows': len(profiles), 'unit': 'creator topic vector'},
    {'file': 'network.csv', 'rows': len(network), 'unit': 'directed following edge'},
    {'file': 'topics.json', 'rows': len(topics), 'unit': 'topic index (CSV text)'},
]))
print('Video columns:', videos.columns.tolist())
print('Unique video IDs:', videos.video_id.nunique(), 'unique author IDs:', videos.author_id.nunique())
print('Unique profile users:', profiles.user_ID.nunique())
print('Topic labels:', len(topics), 'includes Outliers:', topics.Label.eq('Outliers').any())
""", "The 590,361 video rows match the paper's filtered set, but only 590,360 video IDs are unique. There are 18,041 video author IDs and 14,047 profile users; these are not identical populations."),
        ("2. Topic distribution", "Identify the largest published topic groups and the unassigned share.", """
display(videos.topic.value_counts(dropna=False).head(15).rename_axis('topic').to_frame('video_rows'))
print('Outliers share:', f'{100 * videos.topic.eq("Outliers").mean():.2f}%')
print('Distinct observed labels:', videos.topic.nunique(), 'topic-index labels:', len(topics))
""", "267,718 rows (45.35%) are `Outliers`, meaning no specific topic was assigned by the model. This is not a climate opinion. Lifestyle is the largest named topic (80,861 rows)."),
        ("3. Videos per creator", "Check whether a few active creators dominate the video-level sample.", """
per_creator = videos.groupby('author_id').size()
display(per_creator.describe(percentiles=[.25, .5, .75, .9, .99]).to_frame('video_rows_per_author'))
top_n = max(1, int(np.ceil(len(per_creator) * .01)))
print('Share of videos from most prolific 1% of authors (%):',
      round(100 * per_creator.nlargest(top_n).sum() / len(videos), 2))
print('Video author IDs also in profiles:', len(set(videos.author_id) & set(profiles.user_ID)))
""", "The median is 14 videos per author, the mean is 32.72, and the top 1% of authors supply 10.32% of rows. These figures describe the selected collection, not all TikTok creators."),
        ("4. Hashtags", "Count author-provided hashtags per video and list common tags.", """
tag_lists = videos.hashtags.apply(lambda value: value if isinstance(value, list) else [])
tag_counts = tag_lists.map(len)
display(tag_counts.describe(percentiles=[.25, .5, .75, .9, .99]).to_frame('hashtags_per_video'))
tags = Counter(str(tag).lower() for row in tag_lists for tag in row)
display(pd.Series(dict(tags.most_common(15)), name='video_occurrences').to_frame())
print('Videos with no hashtags:', int(tag_counts.eq(0).sum()))
""", "The median is 10 hashtags; 20,008 rows have none. `fyp` occurs 153,012 times. A broad reach tag does not establish a video's position on climate change."),
        ("5. Follower-network structure", "Calculate nodes and directed edges, and test whether network names can be joined to video author IDs.", """
nodes = set(network.source.astype(str)) | set(network.target.astype(str))
out_degree = network.groupby('source').size()
in_degree = network.groupby('target').size()
display(pd.DataFrame([{'edge_rows': len(network),
                       'unique_directed_edges': len(network.drop_duplicates(['source', 'target'])),
                       'unique_nodes': len(nodes), 'mean_outgoing_edges_per_node': len(network) / len(nodes)}]))
display(pd.DataFrame({'out_degree': out_degree.describe(percentiles=[.5, .9, .99]),
                      'in_degree': in_degree.describe(percentiles=[.5, .9, .99])}))
print('Direct overlap: numeric video author IDs vs network source names:',
      len(set(videos.author_id.astype(str)) & set(network.source.astype(str))))
""", "There are 161,891 unique directed edges and 13,867 nodes. The network uses username-like strings, while videos use numeric IDs; direct overlap is zero, so these files cannot safely be joined as-is."),
        ("6. Creator topic vectors", "Check vector dimension and missing-information vectors before finding the dominant topic.", """
import ast
vectors = profiles.profile.map(ast.literal_eval)
lengths = vectors.map(len)
print('Vector lengths:', lengths.value_counts().to_dict())
matrix = np.array(vectors[lengths.eq(26)].tolist(), dtype=float)
print('Quantiles of vector sums:', np.round(np.quantile(matrix.sum(axis=1), [0, .25, .5, .75, 1]), 3))
nonzero = matrix.sum(axis=1) > 0
print('All-zero vectors:', int((~nonzero).sum()))
labels_by_id = dict(zip(topics.Topic_id, topics.Label))
dominant = pd.Series([labels_by_id.get(int(index), 'unknown') for index in matrix[nonzero].argmax(axis=1)])
display(dominant.value_counts().head(12).rename_axis('largest_vector_topic').to_frame('creators'))
""", "All published vectors have 26 elements; 650 are all zero and are excluded from dominant-topic analysis. Lifestyle leads among 3,778 nonzero profiles. A topic vector is not an attitude measure."),
    ],
    "- `videos.json` contains **590,361** rows, **590,360** unique IDs, and **18,041** distinct author IDs; it lacks comment counts and raw media.\n"
    "- **267,718** rows (45.35%) are topic-model `Outliers`; these are not a climate stance.\n"
    "- The author-level video median is **14**, mean **32.72**; the most prolific 1% supply **10.32%** of video rows.\n"
    "- `fyp` occurs **153,012** times as a hashtag; generic reach tags remain in the release.\n"
    "- The follower network has **161,891** distinct directed edges among **13,867** nodes, but its names do not directly match numeric video author IDs.\n"
    "- **650** creator topic vectors are all-zero. The file named `topics.json` is actually CSV text with 26 named topics plus `Outliers`.",
    "Climate_Change_TikTok_dataset_analysis.ipynb",
)


make(
    "German multimodal TikTok archive: access and conditional analysis",
    "[Weizenbaum data record](https://www.weizenbaum-library.de/items/04482f4d-3f73-44e9-859b-f815b089caab) · "
    "[Data report](https://www.weizenbaum-library.de/bitstreams/54049d98-d6c8-4c66-a890-6360118c22f9/download). "
    "This is a data report, not a peer-reviewed paper. The source reports 11,242 Explore-page appearances of 5,137 unique videos, collected from a German IP while logged out, 31 July–4 August 2023. "
    "Automated ZIP download was blocked by the site on 9 October 2026, so reported counts are **not local measurements**. "
    "If you manually obtain the four ZIPs and put them in `downloaded_datasets/german_multimodal/`, the following cells will analyse them.",
    "german_multimodal",
    [
        ("1. Local file availability", "Separate download links on the source page from ZIPs actually saved locally.", """
expected = ['meta_data.zip', 'audio_embeddings.zip', 'text_embeddings.zip', 'video_embeddings.zip']
display(pd.DataFrame([{'file': name, 'present_locally': (DATA / name).is_file()} for name in expected]))
if not (DATA / 'meta_data.zip').exists():
    print('Not calculated: the reported 11,242 rows and 5,137 videos cannot yet be checked locally.')
""", "A publicly listed download is not the same as a locally acquired file. The remaining cells deliberately report `Not calculated` until the files exist."),
        ("2. Metadata schema and count", "After a manual download, inspect the real CSV inside the metadata ZIP before selecting analytical columns.", """
import zipfile

def read_csv_from_zip(path):
    with zipfile.ZipFile(path) as archive:
        names = [name for name in archive.namelist() if name.lower().endswith('.csv')]
        if len(names) != 1:
            raise ValueError(f'{path.name}: expected one CSV, found {names}')
        with archive.open(names[0]) as handle:
            return pd.read_csv(handle, low_memory=False)

metadata = None
if (DATA / 'meta_data.zip').exists():
    metadata = read_csv_from_zip(DATA / 'meta_data.zip')
    print('Measured metadata rows:', len(metadata), 'source-reported rows: 11242')
    print('Columns:', metadata.columns.tolist())
    display(metadata.isna().mean().sort_values(ascending=False).head(15)
            .rename('missing_share').to_frame())
else:
    print('Not calculated: meta_data.zip is missing.')
""", "Inspect actual column names first. Do not claim that the source-reported counts were measured from the file before the ZIP is present."),
        ("3. Repeated appearances and categories", "If metadata is present, determine how often videos reappear and which categories are represented.", """
if metadata is None:
    print('Not calculated: meta_data.zip is needed. Source reports 11,242 appearances and 5,137 videos.')
else:
    print('Possible ID columns:', [x for x in metadata if 'id' in x.lower()])
    print('Possible category columns:', [x for x in metadata if 'categor' in x.lower() or 'section' in x.lower()])
    id_col = next((x for x in metadata if 'video' in x.lower() and 'id' in x.lower()), None)
    if id_col is None:
        id_col = next((x for x in metadata if 'post' in x.lower() and 'id' in x.lower()), None)
    if id_col is not None:
        per_video = metadata.groupby(id_col, dropna=True).size()
        print('Measured unique videos:', len(per_video), 'source-reported videos: 5137')
        display(per_video.describe(percentiles=[.5, .9, .99]).to_frame('appearances_per_video'))
    else:
        print('Unique videos not calculated: confirm the video-ID field against the data report.')
    category_col = next((x for x in metadata if 'categor' in x.lower()), None)
    if category_col is not None:
        display(metadata[category_col].value_counts(dropna=False).to_frame('appearance_rows'))
    else:
        print('Categories not calculated: confirm the category field.')
""", "Appearance rows can exceed unique videos because one video may be observed more than once. A real video-ID field is needed to verify the 5,137 figure."),
        ("4. Coverage of the three modalities", "If ZIPs are present, inspect text, audio, and video embedding tables and their ID overlap with metadata.", """
for filename in expected[1:]:
    path = DATA / filename
    if not path.exists():
        print(filename, ': Not calculated; ZIP is missing locally.')
        continue
    frame = read_csv_from_zip(path)
    print(filename, ':', len(frame), 'rows,', len(frame.columns), 'columns; first column:', frame.columns[0])
    if metadata is not None and id_col is not None:
        overlap = len(set(frame.iloc[:, 0].astype(str)) & set(metadata[id_col].astype(str)))
        print('Direct video-ID overlap with metadata:', overlap)
""", "Embeddings are numerical model features, not raw media. If ID overlap is zero, check whether identifiers have been hashed or reformatted before joining tables."),
    ],
    "- The data record reports **11,242** Explore appearances of **5,137** distinct videos, collected with a German IP while logged out. These numbers remain **source-reported, not locally verified**.\n"
    "- The ZIPs could not be downloaded automatically on 9 October 2026 because the site presented an access challenge. The notebook intentionally produces no invented file-based statistics.\n"
    "- The data description says video links and descriptions are withheld, while creator/music identifiers are hashed. Embeddings cannot reconstruct raw media or comments.",
    "German_Multimodal_TikTok_dataset_analysis.ipynb",
)


make(
    "TIDES: TikTok influencer tiers and engagement",
    "[Paper](https://ojs.aaai.org/index.php/ICWSM/article/view/31405) · "
    "[Authors' dataset repository](https://github.com/skmtr1/TIDES-TikTok-Influencer-dataset). "
    "This notebook analyses only the TikTok tables and keeps video-level and creator-level summaries separate. "
    "`comments` is an engagement-count field per video, **not** individual comment text. Tier differences are descriptive, not causal.",
    "tides_influencer",
    [
        ("1. Structure and paper/release counts", "Compare the public CSV release with the paper snapshot and test ID uniqueness.", """
import numpy as np
users = pd.read_csv(DATA / 'tiktok_influencers.csv', dtype={'id': str})
parts = [pd.read_csv(DATA / f'tiktok_videos-{j}.csv', dtype={'id': str, 'authorId': str}, low_memory=False)
         for j in [1, 2]]
videos = pd.concat(parts, ignore_index=True)
display(pd.DataFrame([{'creator_rows': len(users), 'unique_creator_ids': users.id.nunique(),
                       'video_rows': len(videos), 'unique_video_ids': videos.id.nunique(),
                       'paper_creators': 5000, 'paper_videos': 230406,
                       'release_minus_paper_video_rows': len(videos) - 230406}]))
print('Video authors found in creator table:', len(set(videos.authorId) & set(users.id)))
print('Released video columns:', len(videos.columns))
""", "The release has 233,994 unique video IDs, 3,588 above the paper's 230,406-video snapshot. All 5,000 creators join. Do not delete rows simply to force the paper and release counts to match."),
        ("2. Tier sizes", "Check whether equal numbers of creators also mean equal numbers of videos.", """
user_tiers = users.tier.value_counts()
video_tiers = videos.authorTier.value_counts()
display(pd.DataFrame({'creators': user_tiers, 'videos': video_tiers,
                      'mean_videos_per_creator': video_tiers / user_tiers}).sort_index().round(2))
""", "Each of the five tiers has 1,000 creators, but the video totals differ. A pooled video statistic gives more weight to prolific creators."),
        ("3. Comments per video", "Compare the mean, median, zero share, and upper tail of the released comment-count snapshot.", """
for col in ['comments', 'views', 'likes', 'shares', 'duration']:
    videos[col] = pd.to_numeric(videos[col], errors='coerce')
summary = videos.groupby('authorTier')['comments'].agg(
    video_count='count', mean_comments='mean', median_comments='median',
    zero_comment_share_percent=lambda x: 100 * x.eq(0).mean(),
    p90_comments=lambda x: x.quantile(.9))
display(summary.sort_index().round(2))
print('All-video mean comments:', round(videos.comments.mean(), 2),
      'median comments:', videos.comments.median())
""", "The all-video mean is 201.66 comments, but the median is only 16. Tier medians are 3, 6, 14, 31, and 88 (Nano to Mega). A small highly engaged tail raises the mean."),
        ("4. Creator-level comparison", "Give each creator one summary instead of allowing prolific creators to dominate the tier comparison.", """
by_author = videos.groupby(['authorId', 'authorTier']).agg(
    videos_published=('id', 'size'), creator_median_comments=('comments', 'median'),
    creator_median_views=('views', 'median')).reset_index()
display(by_author.groupby('authorTier').agg(
    creators=('authorId', 'nunique'), median_videos_per_creator=('videos_published', 'median'),
    median_of_creator_comment_medians=('creator_median_comments', 'median'),
    median_of_creator_view_medians=('creator_median_views', 'median')).round(2))
""", "The medians of creator-level comment medians are 3, 6, 13, 30.5, and 85.5. The tier pattern remains descriptive; it cannot prove how to gain followers."),
        ("5. Duration and engagement", "Describe duration bands and rank correlations without claiming causation.", """
bands = pd.cut(videos.duration, bins=[-1, 15, 30, 60, 180, float('inf')],
               labels=['0-15 s', '16-30 s', '31-60 s', '61-180 s', '>180 s'])
display(videos.groupby(bands, observed=True)['comments'].agg(
    video_count='count', median_comments='median', mean_comments='mean').round(2))
display(videos[['comments', 'views', 'likes', 'shares', 'duration']]
        .corr(method='spearman').round(3))
""", "The comments–likes Spearman coefficient is about 0.838 and comments–views is about 0.796. Duration-band comment medians rise from 10 to 42. Author size, topic, and timing may confound these associations."),
        ("6. Released content and missingness", "Check whether media URLs and derived multimodal fields are populated.", """
columns = ['caption', 'hashtags', 'videoURL', 'musicName', 'musicURL',
           'danceability', 'video_hasText', 'comments', 'authorTier']
display(pd.DataFrame({'field': columns,
                      'non_missing_rows': [int(videos[x].notna().sum()) for x in columns],
                      'non_missing_share_percent': [100 * videos[x].notna().mean() for x in columns]}).round(2))
print('No raw MP4 or individual comment-text files are included in these local public CSVs.')
""", "Every row has a `videoURL` value, but that does not prove the link still works. Spotify `danceability` is present for only 14.24% of videos; comment counts are not comment rows."),
    ],
    "- The creator table contains **5,000** creators, 1,000 in each tier. The public CSVs contain **233,994** unique videos, versus **230,406** reported in the paper; both snapshots are retained.\n"
    "- Per-video comment-count mean is **201.66** and median **16**. Tier medians are **3, 6, 14, 31, 88**; author-first summaries give **3, 6, 13, 30.5, 85.5**.\n"
    "- Duration and engagement relationships are associations only; this sample cannot establish that longer videos cause more comments.\n"
    "- Spotify `danceability` is available in only **14.24%** of released video rows. The public CSVs have comment counts, not individual comments or raw MP4s.",
    "TIDES_Influencer_TikTok_dataset_analysis.ipynb",
)


make(
    "EDTok: audit of the public eating-disorder TikTok release",
    "[Paper](https://arxiv.org/html/2505.02250) · "
    "[Public repository](https://github.com/cbickham3232/EDTok-A-Dataset-for-Eating-Disorder-Content-on-TikTok). "
    "The paper analysed videos, metadata, and comments, but the public CSV contains video IDs only. "
    "This notebook checks the released ID list; it never presents the paper's comment totals as downloaded comment rows.",
    "edtok",
    [
        ("1. Released columns and size", "Check whether content, creator, date, and comment fields are actually distributed.", """
ids = pd.read_csv(DATA / 'metadata.csv', dtype=str)
print('Released columns:', ids.columns.tolist())
print('Released rows:', len(ids), 'paper final videos:', 43040,
      'row difference:', len(ids) - 43040)
print('Data types:', ids.dtypes.astype(str).to_dict())
""", "The CSV has exactly 43,040 rows, matching the paper's final-video count, but its only column is `id`. Reading IDs as strings protects long identifiers from numerical rounding."),
        ("2. ID quality", "Count blank, duplicate, and malformed IDs without making claims about unavailable video content.", """
clean = ids.id.fillna('').str.strip()
display(pd.DataFrame([{'all_rows': len(ids), 'unique_nonblank_ids': clean[clean.ne('')].nunique(),
                       'blank_ids': int(clean.eq('').sum()),
                       'extra_duplicate_rows': int(clean[clean.ne('')].duplicated().sum()),
                       'non_numeric_ids': int((~clean.str.fullmatch(r'\\d+')).sum())}]))
display(clean.str.len().value_counts().sort_index()
        .rename_axis('id_character_count').to_frame('rows'))
""", "All 43,040 IDs are nonblank, distinct, and 19 digits long. This does not show topic, current accessibility, or comment volume."),
        ("3. What cannot be reproduced", "Make the missing variables and denominator of each proposed analysis explicit.", """
requirements = {
    'Mean or median comments per video': ['comment_count', 'comments'],
    'Unique creator count': ['author_id', 'username'],
    'Videos by publication month': ['create_time', 'publish_time'],
    'Comment-text themes': ['comment_text', 'text'],
    'Engagement distributions': ['view_count', 'like_count'],
}
display(pd.DataFrame([{'analysis': name, 'required_field_present': any(col in ids.columns for col in cols)}
                      for name, cols in requirements.items()]))
print('Paper reports 43,040 videos, 10,897 users, 388,332 top-level comments and 188,739 replies.')
print('These paper figures are not comment rows measured from the public CSV.')
""", "All five substantive analyses are unavailable from the public ID file. The paper's 577,071 comments-plus-replies total cannot be independently checked from this release."),
        ("4. Optional later hydration", "If an authorised metadata file is later obtained, match IDs before computing comment-count summaries.", """
hydrated_path = DATA / 'hydrated_videos.csv'
if not hydrated_path.exists():
    print('Not calculated: hydrated_videos.csv is absent; there is no real per-video comment statistic.')
else:
    hydrated = pd.read_csv(hydrated_path, dtype={'id': str}, low_memory=False)
    required = {'id', 'comment_count'}
    if not required.issubset(hydrated.columns):
        print('Missing required columns:', required - set(hydrated.columns))
    else:
        matched = hydrated[hydrated.id.isin(set(clean))].drop_duplicates('id')
        counts = pd.to_numeric(matched.comment_count, errors='coerce').dropna()
        print('Released IDs:', clean.nunique(), 'matched hydrated videos:', len(matched))
        display(counts.describe(percentiles=[.25, .5, .75, .9, .99])
                .to_frame('comment_count_snapshot_per_video'))
""", "Only calculate if a real, ID-matched metadata file exists. Report match rate and crawl date, because missing videos may be systematically different."),
    ],
    "- The public `metadata.csv` has **43,040** distinct, nonblank 19-digit video IDs, matching the paper's final video total.\n"
    "- There are **no content, publication-date, creator, or comment fields** in this release, so no substantive topic or comment pattern can be observed locally.\n"
    "- The paper's **10,897** users and **577,071** comments plus replies are source-reported, not independently reproducible from the released CSV. Comment mean and median remain **not calculated** until an authorised, matched metadata file exists.",
    "EDTok_TikTok_dataset_analysis.ipynb",
)
