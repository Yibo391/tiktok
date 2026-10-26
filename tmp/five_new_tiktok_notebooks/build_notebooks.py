"""Build five independent, locally executable TikTok dataset notebooks."""

from pathlib import Path

import nbformat as nbf


ROOT = Path(__file__).resolve().parents[2]


def notebook(title, intro):
    nb = nbf.v4.new_notebook()
    nb.metadata.kernelspec = {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3",
    }
    nb.metadata.language_info = {"name": "python"}
    nb.cells = [nbf.v4.new_markdown_cell(f"# {title}\n\n{intro}")]
    return nb


def section(nb, heading, purpose, code, observation):
    nb.cells.append(nbf.v4.new_markdown_cell(f"## {heading}\n\n**目的：**{purpose}"))
    nb.cells.append(nbf.v4.new_code_cell(code.strip()))
    nb.cells.append(nbf.v4.new_markdown_cell(f"**怎样看结果：**{observation}"))


def setup(nb, folder):
    section(
        nb,
        "本地文件与分析环境",
        "确认 notebook 正在读取本机公开数据文件，并显示文件大小。",
        f"""
from pathlib import Path
import pandas as pd
from IPython.display import display

ROOT = Path.cwd()
if not (ROOT / 'downloaded_datasets').exists() and (ROOT.parent / 'downloaded_datasets').exists():
    ROOT = ROOT.parent
DATA = ROOT / 'downloaded_datasets' / '{folder}'
print('数据目录:', DATA.resolve())
if DATA.exists():
    display(pd.DataFrame([{{'文件': p.name, 'MB': round(p.stat().st_size/1e6, 2)}}
                          for p in sorted(DATA.iterdir()) if p.is_file()]))
else:
    print('本地目录不存在。请先下载源文件。')
""",
        "这些是本机文件清单；其存在不等于每一字段都包含论文所用的原始媒体或评论。",
    )


def save(nb, name):
    path = ROOT / name
    nbf.write(nb, path)
    print(path)


# 1. PoliTok-DE
p = notebook(
    "PoliTok-DE：德国选举 TikTok 数据分析",
    "论文：[Ruiz et al., PoliTok-DE, arXiv v2 (2026)](https://arxiv.org/abs/2509.15860)。"
    "公开数据：[Hugging Face](https://huggingface.co/datasets/tomasruiz/PoliTok-DE)。"
    "本 notebook 分析公开的帖子 ID、可访问状态快照与萨克森人工标注。"
    "原始视频、音频和完整元数据未随公开文件发布。`DELETED` 表示该次复查无法公开访问，"
    "不等于确认存在违规内容。\n\n"
    "运行：从 `/Users/wang/Documents/tiktok` 打开 notebook 并逐格运行。依赖 `pandas`、`pyarrow`、`IPython`。",
)
setup(p, "politok_de")
section(p, "1. 文件结构和论文数量", "核对本地 ID 行数与论文修订版的两场选举数量，并检查 ID 是否重复。", """
sax = pd.read_parquet(DATA / 'saxony_post_ids.parquet')
fed = pd.read_parquet(DATA / 'federal_post_ids.parquet')
ann = pd.read_parquet(DATA / 'saxony_annotations.parquet')
overview = pd.DataFrame([
    {'集合':'萨克森 2024', '公开行数':len(sax), '不同帖子ID':sax.post_id.nunique(), '论文报告':195373},
    {'集合':'联邦 2025', '公开行数':len(fed), '不同帖子ID':fed.post_id.nunique(), '论文报告':743588},
])
overview['与论文行数差'] = overview['公开行数'] - overview['论文报告']
display(overview)
print('两集合 ID 重叠数:', len(set(sax.post_id) & set(fed.post_id)))
print('萨克森标注行数:', len(ann), '不同被标注帖子:', ann.post_id.nunique())
print('公开 ID 文件字段:', sax.columns.tolist(), fed.columns.tolist())
""", "两集合与论文 v2 的行数差都是 **0**，ID 集合也没有交叉。标注文件有 **935** 行，但只有 **360** 个帖子；标注行不是不同帖子数。")
section(p, "2. 两场选举的最终可访问状态", "计算每场选举在已公布复查日期的可访问与不可访问数量。", """
rows = []
for name, frame, col in [('萨克森 2024', sax, 'availability_2025_01_13'),
                          ('联邦 2025', fed, 'availability_2026_06_11')]:
    c = frame[col].value_counts()
    rows.append({'集合':name, '复查日期':col.replace('availability_', ''),
                 '总ID':len(frame), 'AVAILABLE':int(c.get('AVAILABLE', 0)),
                 'DELETED':int(c.get('DELETED', 0)),
                 'UNKNOWN_ERROR':int(c.get('UNKNOWN_ERROR', 0)),
                 'DELETED占全部ID%':100*c.get('DELETED', 0)/len(frame)})
final_state = pd.DataFrame(rows)
display(final_state.round(2))
""", "萨克森为 **18.74%**，联邦为 **39.69%**；联邦复查得更晚，所以这两个比例不能直接当成选举内容差异。萨克森的 **2,014** 个 `UNKNOWN_ERROR` 是未确定结果。")
section(p, "3. 萨克森的多次复查", "看同一集合随时间复查时，已知状态的分布如何变化。", """
wave = []
for col in [x for x in sax.columns if x.startswith('availability_')]:
    c = sax[col].value_counts()
    checked = int(c.get('AVAILABLE', 0) + c.get('DELETED', 0))
    wave.append({'复查日期':col.replace('availability_', ''), 'AVAILABLE':int(c.get('AVAILABLE',0)),
                 'DELETED':int(c.get('DELETED',0)), 'NOT_RESCRAPED':int(c.get('NOT_RESCRAPED',0)),
                 'UNKNOWN_ERROR':int(c.get('UNKNOWN_ERROR',0)),
                 '有明确结果的帖子':checked,
                 'DELETED占有明确结果%':100*c.get('DELETED',0)/checked if checked else float('nan')})
display(pd.DataFrame(wave).round(2))
""", "首次有 **92,420** 条 `NOT_RESCRAPED`，明确得到结果的只有 **102,949** 条。之后观察到的删除数增加，但各次覆盖率不同，不能把这些比例看作完全相同样本的风险变化。")
section(p, "4. 人工标注：标签与意见分歧", "区分标注行与被标注视频，并了解哪些标签较易出现分歧。", """
labels = ['is_political','is_saxony_election','is_intolerant',
          'is_hedonic_entertainment','is_eudaimonic_entertainment']
result = []
for col in labels:
    votes = ann[col].str.lower().str.strip()
    per_post = ann.assign(vote=votes.where(votes.isin(['yes','no']))).groupby('post_id')['vote']
    counts = per_post.nunique(dropna=True)
    result.append({'标签':col, '有效投票':int(votes.isin(['yes','no']).sum()),
                   'yes投票%':100*votes.eq('yes').sum()/votes.isin(['yes','no']).sum(),
                   '有分歧的帖子':int((counts>1).sum()),
                   '被标注帖子':ann.post_id.nunique()})
display(pd.DataFrame(result).round(2))
print('每个帖子有多少条标注记录:')
display(ann.groupby('post_id').size().value_counts().sort_index().rename_axis('标注行数').to_frame('帖子数'))
""", "不宽容 `yes` 占 **20.49%** 的有效投票；关于享乐型/意义型娱乐，分别有 **88/120** 个帖子出现不同投票。此处只涉及被抽样标注的 360 帖；3 帖各有 5 行标注，值得与论文描述对照。")
section(p, "5. 删除状态码", "查看不可访问帖子对应的原始状态码是否单一或复杂。", """
for name, frame, av, sc in [('萨克森',sax,'availability_2025_01_13','status_codes_2025_01_13'),
                             ('联邦',fed,'availability_2026_06_11','status_codes_2026_06_11')]:
    codes = frame.loc[frame[av].eq('DELETED'), sc].fillna('')
    print(name, 'DELETED中的常见状态码组合:')
    display(codes.value_counts().head(10).rename_axis('代码组合').to_frame('帖子数'))
""", "状态码组合只是平台返回的技术信号。论文根据这些组合提出‘创作者撤回’和‘平台处置’的划分；这里没有把简单的 `DELETED` 标记直接解释为平台处罚。")
p.cells.append(nbf.v4.new_markdown_cell("## 本次发现与边界\n\n- 公开 ID 文件分别有 **195,373** 和 **743,588** 行，与论文 v2 一致，合计 **938,961** 个不重叠的帖子 ID。\n- 萨克森截至 2025-01-13 有 **36,617** 个 `DELETED`（占全部 ID 的 **18.74%**），还有 **2,014** 个 `UNKNOWN_ERROR`。联邦截至 2026-06-11 有 **295,101** 个 `DELETED`（**39.69%**）。复查间隔不同，不能直接归因为两场选举的内容差异。\n- 萨克森最早一次仅 **102,949** 条得到明确结果，另有 **92,420** 条未复查。比较删除比例时必须写清楚分母。\n- 标注文件有 **935** 行、**360** 个不同帖子；不宽容 `yes` 投票占有效投票约 **20.49%**。它是选取的子样本，并非全部政治帖子的不宽容率。公开文件中有 **3** 个帖子各有 5 条标注记录，与论文‘每帖 1–4 名标注者’的描述不完全一致；这可能是发布版本差异，不能擅自解释。\n- 公开文件不含创作者、正文、评论或媒体，因而无法从这里复现论文的内容与互动分析。"))
save(p, "PoliTok_DE_dataset_analysis.ipynb")


# 2. Climate change
c = notebook(
    "Mapping the climate change landscape on TikTok：公开数据分析",
    "论文：[Galdeman & Aiello, ICWSM 2025 / arXiv](https://arxiv.org/abs/2505.03813)。"
    "数据：[Zenodo 15131067](https://zenodo.org/records/15131067)。"
    "本地文件有视频主题/标签、创作者主题向量、关注网络；没有评论正文、互动计数或原始视频。"
    "论文分析的是按关键词和英文描述筛过的集合，不是随机抽取的全平台视频。"
    "运行依赖 `pandas`、`numpy`、`IPython`。",
)
setup(c, "climate_change")
section(c, "1. 结构与论文数量", "核对公开文件单位和大小，并检查扩展名与实际格式。", """
import json
import numpy as np
from collections import Counter
with (DATA / 'videos.json').open(encoding='utf-8') as handle:
    videos = pd.DataFrame(json.load(handle))
profiles = pd.read_csv(DATA / 'profiles.csv')
network = pd.read_csv(DATA / 'network.csv')
topics = pd.read_csv(DATA / 'topics.json')  # 源文件虽叫 .json，内容实际上是 CSV
display(pd.DataFrame([
    {'文件':'videos.json', '行数':len(videos), '主要单位':'视频记录'},
    {'文件':'profiles.csv', '行数':len(profiles), '主要单位':'创作者主题向量'},
    {'文件':'network.csv', '行数':len(network), '主要单位':'有向关注关系'},
    {'文件':'topics.json', '行数':len(topics), '主要单位':'主题标签索引，实际 CSV 格式'},
]))
print('视频字段:',videos.columns.tolist())
print('不同视频ID:',videos.video_id.nunique(), '不同视频作者ID:',videos.author_id.nunique())
print('不同 profile 用户:',profiles.user_ID.nunique())
print('主题标签总数:',len(topics),'含 Outliers:',topics.Label.eq('Outliers').any())
""", "视频文件的 **590,361** 行与论文英文描述子集相符，但只有 **590,360** 个不同视频 ID。作者 ID 为 **18,041** 个，profile 只有 **14,047** 个；这些属于不同筛选阶段。`topics.json` 实际要按 CSV 读取。")
section(c, "2. 主题分布和未归类项", "找出发布文件中最常见的主题，衡量 `Outliers` 所占比例。", """
topic_counts = videos.topic.value_counts(dropna=False)
display(topic_counts.head(15).rename_axis('主题').to_frame('视频数'))
print('Outliers 占比:', f'{100*videos.topic.eq("Outliers").mean():.2f}%')
print('有标签的不同主题数:',videos.topic.nunique())
print('索引表标签数:',len(topics))
""", "最大一组是 **267,718** 个 `Outliers`（**45.35%**）；最大具体主题是 Lifestyle（**80,861** 个）。`Outliers` 代表模型未分配具体主题，不是一种气候观点；比例也不代表 TikTok 全平台。")
section(c, "3. 每位作者的视频量", "检查视频是否集中在少数创作者，避免把高产创作者等同于多数用户。", """
per_creator = videos.groupby('author_id').size()
display(per_creator.describe(percentiles=[.25,.5,.75,.9,.99]).to_frame('每位作者的视频记录数'))
top_n = max(1, int(np.ceil(len(per_creator)*.01)))
print('最多产的 1% 作者占全部视频%:', round(100*per_creator.nlargest(top_n).sum()/len(videos),2))
print('作者ID出现在 profile 文件中的人数:',len(set(videos.author_id)&set(profiles.user_ID)))
""", "作者视频数中位数 **14**、均值 **32.72**，最多产的 1% 作者贡献 **10.32%** 的视频。少数高产作者明显提高均值；采样围绕标签与活跃账号，不能推广到一般 TikTok 创作者。")
section(c, "4. 标签使用", "计算一个视频附带多少个作者标签，并展示频率最高的标签。", """
tag_lists = videos.hashtags.apply(lambda z: z if isinstance(z,list) else [])
tag_counts = tag_lists.map(len)
display(tag_counts.describe(percentiles=[.25,.5,.75,.9,.99]).to_frame('每视频 hashtags 数'))
tags = Counter(str(tag).lower() for row in tag_lists for tag in row)
display(pd.Series(dict(tags.most_common(15)),name='视频出现数').to_frame())
print('没有标签的视频数:',int(tag_counts.eq(0).sum()))
""", "每视频标签中位数 **10**，约 **20,008** 条没有标签；`fyp` 出现 **153,012** 次。作者标签可多个并存，且可能是引流标签，不足以判定视频立场或科学准确性。")
section(c, "5. 关注网络的结构", "描述已发布网络的节点、边和出入度，确认是否能与视频作者 ID 连接。", """
nodes = set(network.source.astype(str)) | set(network.target.astype(str))
out_degree = network.groupby('source').size()
in_degree = network.groupby('target').size()
display(pd.DataFrame([{'关注关系行数':len(network),'不同有向边':len(network.drop_duplicates(['source','target'])),
                       '不同节点':len(nodes),'平均每节点出边数':len(network)/len(nodes)}]))
display(pd.DataFrame({'出度':out_degree.describe(percentiles=[.5,.9,.99]),
                      '入度':in_degree.describe(percentiles=[.5,.9,.99])}))
print('视频作者ID与网络 source 直接同值的数量:',len(set(videos.author_id.astype(str))&set(network.source.astype(str))))
""", "共有 **161,891** 条不同有向边和 **13,867** 个节点。网络使用用户名样式的字符串，视频使用数字作者 ID；直接可匹配的 source 数是 **0**。没有可信连接键时，不应把网络度数并入视频作者表。")
section(c, "6. 作者主题向量", "确认每条 profile 向量的维度与取值，再看作者最突出的主题分布。", """
import ast
vectors = profiles.profile.map(ast.literal_eval)
lengths = vectors.map(len)
print('向量长度分布:',lengths.value_counts().to_dict())
valid = profiles.loc[lengths.eq(26)].copy()
matrix = np.array(vectors[lengths.eq(26)].tolist(),dtype=float)
print('26维向量各项和的分位数:',np.round(np.quantile(matrix.sum(axis=1),[0,.25,.5,.75,1]),3))
nonzero = matrix.sum(axis=1)>0
print('全零向量:',int((~nonzero).sum()))
labels_by_id = dict(zip(topics.Topic_id,topics.Label))
dominant = pd.Series([labels_by_id.get(int(i),'未知') for i in matrix[nonzero].argmax(axis=1)])
display(dominant.value_counts().head(12).rename_axis('作者向量最高的主题').to_frame('作者数'))
""", "全部 profile 向量都是 26 维，但有 **650** 个全零向量，本节已排除它们。其余作者最常见的最高主题是 Lifestyle（**3,778** 人）。向量表达已发布视频的主题份额，不是个人态度。")
c.cells.append(nbf.v4.new_markdown_cell("## 本次发现与边界\n\n- `videos.json` 有 **590,361** 行、**590,360** 个不同视频 ID 和 **18,041** 个作者 ID；有 **1** 个额外重复视频 ID 行。它不包含评论数或互动计数。\n- 主题模型将 **267,718** 条视频（**45.35%**）标为 `Outliers`。所以不能只看已经分配具体主题的视频，也不能把 `Outliers` 解读为一种气候立场。\n- 每作者视频数中位数为 **14**，均值约 **32.72**；最多产的 1% 作者贡献 **10.32%** 的视频。\n- 视频标签中 `fyp` 最常见（**153,012** 次），说明保留下来的原始标签包括通用流量标签。\n- 关注网络有 **161,891** 条不同有向边、**13,867** 个节点；网络字符串节点和视频数字作者 ID 没有直接匹配。\n- 主题向量有 **650** 条全零记录，计算‘最高主题’时已经排除。`topics.json` 实际是 CSV，含 26 个具体主题与 1 个 `Outliers` 标签。"))
save(c, "Climate_Change_TikTok_dataset_analysis.ipynb")


# 3. German multimodal archive
g = notebook(
    "德国多模态 TikTok 分类数据：可获取性与条件分析",
    "来源：[Wedel, A categorized multimodal TikTok dataset (2023)](https://www.weizenbaum-library.de/items/04482f4d-3f73-44e9-859b-f815b089caab)，"
    "[数据报告 PDF](https://www.weizenbaum-library.de/bitstreams/54049d98-d6c8-4c66-a890-6360118c22f9/download)。"
    "馆藏页称 2023-07-31 至 2023-08-04 的德国 IP、未登录 Explore 页面共 11,242 条展示记录、5,137 条不同视频。"
    "2026-10-09 自动下载受到站点访问限制；这里不把馆藏页数字写成我对本地数据的实测。"
    "如果您从馆藏页手动下载 `meta_data.zip`、`audio_embeddings.zip`、`text_embeddings.zip`、`video_embeddings.zip`"
    "放到 `downloaded_datasets/german_multimodal/`，以下代码会自动分析实际文件。",
)
setup(g, "german_multimodal")
section(g, "1. 是否有实际数据文件", "明确区分公开页面提供的文件名和已经落在本机的文件。", """
expected = ['meta_data.zip','audio_embeddings.zip','text_embeddings.zip','video_embeddings.zip']
availability = pd.DataFrame([{'文件':name, '本地存在':(DATA/name).is_file()} for name in expected])
display(availability)
if not (DATA/'meta_data.zip').exists():
    print('目前不能验证 11,242 行和 5,137 个视频；以下实测结果均应保持“未计算”。')
""", "只有 `本地存在=True` 才能开始对相应文件计算。网页显示可以下载，并不代表本地文件已经拿到。")
section(g, "2. 读取元数据并核对行数", "若手动取得压缩包，统计记录数、视频 ID 数和字段结构。", """
import zipfile
from io import BytesIO
def read_csv_from_zip(path):
    with zipfile.ZipFile(path) as archive:
        names = [name for name in archive.namelist() if name.lower().endswith('.csv')]
        if len(names) != 1:
            raise ValueError(f'{path.name}: 预期 1 个 CSV，实际 {names}')
        with archive.open(names[0]) as handle:
            return pd.read_csv(handle,low_memory=False)

metadata = None
if (DATA/'meta_data.zip').exists():
    metadata = read_csv_from_zip(DATA/'meta_data.zip')
    print('实际记录数:',len(metadata),'馆藏页报告: 11242')
    print('字段:',metadata.columns.tolist())
    display(metadata.isna().mean().sort_values(ascending=False).head(15).rename('缺失比例').to_frame())
else:
    print('未计算：缺少 meta_data.zip')
""", "先检查字段，再选择视频 ID、分类和互动统计的列；不要靠猜测列名填入论文数量。")
section(g, "3. 视频 ID 重复展示与分类", "在有元数据时检验一个视频是否多次出现在 Explore 列表及分类中。", """
if metadata is None:
    print('未计算：需要 meta_data.zip。馆藏页只报告 11,242 条展示记录和 5,137 个视频。')
else:
    print('可能的 ID 字段:',[x for x in metadata if 'id' in x.lower()])
    print('可能的分类字段:',[x for x in metadata if 'categor' in x.lower() or 'section' in x.lower()])
    id_col = next((x for x in metadata if 'video' in x.lower() and 'id' in x.lower()),None)
    if id_col is None:
        id_col = next((x for x in metadata if 'post' in x.lower() and 'id' in x.lower()),None)
    if id_col is not None:
        per_video = metadata.groupby(id_col,dropna=True).size()
        print('不同视频:',len(per_video),'馆藏页报告: 5137')
        display(per_video.describe(percentiles=[.5,.9,.99]).to_frame('每视频被收录次数'))
    else:
        print('未计算不同视频：必须先依据数据报告确认哪个字段是视频 ID。')
    category_col = next((x for x in metadata if 'categor' in x.lower()),None)
    if category_col is not None:
        display(metadata[category_col].value_counts(dropna=False).to_frame('展示记录数'))
    else:
        print('未计算分类：必须先确认类别列名。')
""", "展示记录数可以大于不同视频数，因为同一视频可能在多个时间或类别出现。只有找到真实视频 ID 列，才能核对 5,137。")
section(g, "4. 三种模态的覆盖率", "若压缩包已下载，核对文本、音频、视频向量文件的行列数和与元数据的 ID 交集。", """
for filename in expected[1:]:
    path = DATA/filename
    if not path.exists():
        print(filename, ': 未计算，文件不在本地')
        continue
    frame = read_csv_from_zip(path)
    print(filename, ':',len(frame),'行，',len(frame.columns),'列；首列:',frame.columns[0])
    if metadata is not None and id_col is not None:
        overlap = len(set(frame.iloc[:,0].astype(str)) & set(metadata[id_col].astype(str)))
        print('与元数据视频ID的直接匹配数:',overlap)
""", "向量是模型提取的数字特征，不是原始音频或视频。若不同模态覆盖率不同，需要以实际交集为分母；匹配数为 0 时先核对 ID 是否经过哈希或格式转换。")
g.cells.append(nbf.v4.new_markdown_cell("## 当前发现\n\n- 馆藏记录报告 11,242 条 Explore 展示记录和 5,137 个不同视频，使用德国 IP、未登录访问。\n- 当前机器未成功自动取得站点压缩包；本 notebook 对这些数字只作来源说明，没有冒充实测。\n- 公开说明称视频链接和描述未发布，创作者及音乐名称采用哈希；即使取得向量文件，也无法由向量直接还原媒体或评论。"))
save(g, "German_Multimodal_TikTok_dataset_analysis.ipynb")


# 4. TIDES influencers
i = notebook(
    "TIDES：TikTok 网红等级与互动统计",
    "论文：[Tricomi et al., ICWSM 2024](https://ojs.aaai.org/index.php/ICWSM/article/view/31405)。"
    "数据与代码：[TIDES GitHub](https://github.com/skmtr1/TIDES-TikTok-Influencer-dataset)。"
    "本 notebook 只分析 TikTok 表；作者级别和视频级别分开计算。"
    "`comments` 是每个视频的评论数快照，不包含评论文字。"
    "等级按关注者规模构造，不能用等级差异证明某种拍摄方式能增加关注者。"
    "运行依赖 `pandas`、`numpy`、`IPython`。",
)
setup(i, "tides_influencer")
section(i, "1. 结构、唯一性与论文计数", "核对网红数量和视频数量，并报告公开文件与论文数值的差异。", """
import numpy as np
users = pd.read_csv(DATA/'tiktok_influencers.csv',dtype={'id':str})
parts = [pd.read_csv(DATA/f'tiktok_videos-{j}.csv',dtype={'id':str,'authorId':str},low_memory=False) for j in [1,2]]
videos = pd.concat(parts,ignore_index=True)
display(pd.DataFrame([{'作者行数':len(users),'不同作者ID':users.id.nunique(),
                       '视频行数':len(videos),'不同视频ID':videos.id.nunique(),
                       '论文作者数':5000,'论文视频数':230406,
                       '公开文件比论文多的视频行':len(videos)-230406}]))
print('视频作者可匹配作者表:',len(set(videos.authorId)&set(users.id)))
print('公开视频字段数:',len(videos.columns))
""", "公开 CSV 有 **233,994** 个不同视频 ID，较论文正文的 **230,406** 多 **3,588**。五千名作者均可匹配。两种规模需同时报告；不能为了对齐论文而无依据地删行。")
section(i, "2. 每等级作者与视频数量", "检查等级是否有均衡的作者样本，以及每等级的视频样本是否也均衡。", """
user_tiers = users.tier.value_counts()
video_tiers = videos.authorTier.value_counts()
display(pd.DataFrame({'作者数':user_tiers,'视频数':video_tiers,
                      '每作者平均视频数':video_tiers/user_tiers}).sort_index().round(2))
""", "五级各 **1,000** 作者，但 Nano 只有 **39,408** 条视频，Mega 有 **49,774** 条。视频层面的总体均值会给视频更多的作者更大权重。")
section(i, "3. 每视频的评论分布", "比较平均数、中位数和高分位数，避免少数热门视频遮蔽常见视频。", """
for col in ['comments','views','likes','shares','duration']:
    videos[col] = pd.to_numeric(videos[col],errors='coerce')
summary = videos.groupby('authorTier')['comments'].agg(
    视频数='count',平均评论数='mean',中位评论数='median',
    零评论比例=lambda x:100*x.eq(0).mean(),
    第90百分位=lambda x:x.quantile(.9))
display(summary.sort_index().round(2))
print('全数据评论数：均值',round(videos.comments.mean(),2),'中位数',videos.comments.median())
""", "全表评论数均值 **201.66**、中位数 **16**；Nano/Micro/Mid/Macro/Mega 的中位数依次是 **3/6/14/31/88**。少数高互动视频拉高均值，等级差异也受账号规模与抽样影响。")
section(i, "4. 以作者为单位重看评论", "每位作者先取自己视频的评论中位数，再按等级汇总，避免高产作者控制比较。", """
by_author = videos.groupby(['authorId','authorTier']).agg(
    发布视频数=('id','size'),作者视频评论中位数=('comments','median'),
    作者视频观看中位数=('views','median')).reset_index()
display(by_author.groupby('authorTier').agg(
    作者数=('authorId','nunique'),每作者视频数中位数=('发布视频数','median'),
    作者评论中位数的中位数=('作者视频评论中位数','median'),
    作者观看中位数的中位数=('作者视频观看中位数','median')).round(2))
""", "按作者先求视频评论中位数后，五级作者的对应中位数为 **3/6/13/30.5/85.5**，阶梯仍可见，但与按视频计算的值略有差异。这个比较不提供涨粉因果方法。")
section(i, "5. 时长与互动关系", "观察短视频长度与评论数是否一起变化，并看评论与点赞/观看的排序相关。", """
bands = pd.cut(videos.duration,bins=[-1,15,30,60,180,float('inf')],
               labels=['0–15秒','16–30秒','31–60秒','61–180秒','180秒以上'])
display(videos.groupby(bands,observed=True)['comments'].agg(
    视频数='count',中位评论数='median',平均评论数='mean').round(2))
display(videos[['comments','views','likes','shares','duration']].corr(method='spearman').round(3))
""", "评论与点赞 Spearman 相关约 **0.838**，与观看约 **0.796**；时长组的评论中位数从 **10** 到 **42**。它们是同批数据中的关联，不能证明点赞或长视频导致评论增长。")
section(i, "6. 可用内容与缺失", "确认与 AI 多模态研究有关的字段是否真的有值。", """
columns = ['caption','hashtags','videoURL','musicName','musicURL','danceability',
           'video_hasText','comments','authorTier']
display(pd.DataFrame({'字段':columns,'非空行数':[int(videos[x].notna().sum()) for x in columns],
                      '非空比例%':[100*videos[x].notna().mean() for x in columns]}).round(2))
print('原始 mp4 文件在本地公开 CSV 中不存在；只提供 URL 和派生特征。')
""", "`videoURL` 有值的比例是 **100%**，但 Spotify `danceability` 仅 **14.24%**。URL 可能失效；字段存在也不代表已下载原始媒体或逐条评论。")
i.cells.append(nbf.v4.new_markdown_cell("## 本次发现与边界\n\n- 作者表是 **5,000** 人，五个等级各 **1,000** 人。公开 CSV 有 **233,994** 个不同视频 ID，比论文正文报告的 **230,406** 多 **3,588**；本 notebook 保留并说明这个版本差异。\n- 每视频评论数均值约 **201.66**，中位数 **16**，表明少数高互动视频拉高平均数。Nano 到 Mega 的评论中位数依次是 **3、6、14、31、88**；作者级中位数分析也有类似阶梯，但不证明等级或视频特征造成评论增加。\n- 视频时长分组的评论中位数从 0–15 秒的 **10** 增至 180 秒以上的 **42**；这只是同一批数据中的关联，题材、作者规模和发布时间都可能影响结果。\n- Spotify `danceability` 特征仅 **14.24%** 的视频非空；有 `videoURL` 也不意味着媒体文件可直接使用。公开表有评论数量，没有逐条评论文本。"))
save(i, "TIDES_Influencer_TikTok_dataset_analysis.ipynb")


# 5. EDTok
e = notebook(
    "EDTok：饮食失调话题 TikTok 数据发布审计",
    "论文：[Bickham et al., EDTok (2025)](https://arxiv.org/abs/2505.02250)。"
    "公开仓库：[EDTok GitHub](https://github.com/cbickham3232/EDTok-A-Dataset-for-Eating-Disorder-Content-on-TikTok)。"
    "公开 CSV 只有视频 ID。论文使用过视频、元数据与评论，但这些内容没有随仓库公开。"
    "本 notebook 可核对公开 ID 清单；不会把论文中的评论数当作已下载评论。"
    "运行依赖 `pandas`、`IPython`。",
)
setup(e, "edtok")
section(e, "1. 实际发布字段", "查看 CSV 是否真的包含正文、账号、日期或评论字段。", """
ids = pd.read_csv(DATA/'metadata.csv',dtype=str)
print('字段:',ids.columns.tolist())
print('公开行数:',len(ids))
print('论文最终视频数: 43040')
print('行数差:',len(ids)-43040)
print('数据类型:',ids.dtypes.astype(str).to_dict())
""", "公开 CSV 恰好有 **43,040** 行，与论文最终视频数一致。字段只有 `id`；保持字符串格式可防止长整数被四舍五入，也说明评论与账号统计不能从本文件直接计算。")
section(e, "2. ID 完整性与重复", "确认释放的唯一视频数、空值和明显格式问题。", """
clean = ids.id.fillna('').str.strip()
checks = pd.DataFrame([{
    '全部行':len(ids), '不同非空ID':clean[clean.ne('')].nunique(),
    '空ID':int(clean.eq('').sum()), '额外重复行':int(clean[clean.ne('')].duplicated().sum()),
    '非纯数字ID':int((~clean.str.fullmatch(r'\\d+')).sum()),
}])
display(checks)
display(clean.str.len().value_counts().sort_index().rename_axis('ID字符数').to_frame('行数'))
""", "全部 **43,040** 个 ID 非空、互不重复、均为 19 位数字。清单格式整齐，但 ID 长度不能揭示视频主题，也不保证今天仍可访问。")
section(e, "3. 哪些论文统计无法从公开文件复算", "用可用字段表明确分析能力的边界。", """
requirements = {
    '每视频评论均值/中位数':['comment_count','comments'],
    '作者数量':['author_id','username'],
    '按月发布数量':['create_time','publish_time'],
    '评论内容主题':['comment_text','text'],
    '互动数分布':['view_count','like_count'],
}
display(pd.DataFrame([{'分析':name,'公开 CSV 所需字段存在':any(col in ids.columns for col in cols)}
                      for name,cols in requirements.items()]))
print('论文报告：43,040 个视频；10,897 个用户；388,332 条主评论和 188,739 条回复。')
print('以上论文数字不是此 CSV 的实测评论记录。')
""", "本节五项内容/互动分析全部显示 `False`，因此没有可从公开 CSV 观察到的主题或评论分布。论文报告的 **577,071** 条评论不能作为下载文件的实测评论行使用。")
section(e, "4. 可选：将来加入已授权取得的元数据", "若以后取得与这些 ID 相连的公开可用元数据，可安全地重算评论数量分布。", """
hydrated_path = DATA/'hydrated_videos.csv'
if not hydrated_path.exists():
    print('未计算：本地没有 hydrated_videos.csv；当前没有真实的每视频评论统计。')
else:
    hydrated = pd.read_csv(hydrated_path,dtype={'id':str},low_memory=False)
    required = {'id','comment_count'}
    if not required.issubset(hydrated.columns):
        print('文件缺少必须字段:',required-set(hydrated.columns))
    else:
        matched = hydrated[hydrated.id.isin(set(clean))].drop_duplicates('id')
        counts = pd.to_numeric(matched.comment_count,errors='coerce').dropna()
        print('清单 ID 数:',clean.nunique(),'成功匹配元数据的视频:',len(matched))
        display(counts.describe(percentiles=[.25,.5,.75,.9,.99]).to_frame('每视频评论数快照'))
""", "只有文件真实存在且成功匹配 ID 时才输出统计；匹配比例与抓取日期应同时报告，因为无法获取的视频可能系统性不同。")
e.cells.append(nbf.v4.new_markdown_cell("## 本次发现与边界\n\n- 本地 `metadata.csv` 有 **43,040** 行，全部是非空、不同的 19 位数字视频 ID，与论文最终视频数一致。\n- 由于没有任何内容、发布时间、账号或评论字段，**没有可以从公开文件观察到的话题或评论现象**。论文报告的 10,897 名用户和 577,071 条评论不能用这个 CSV 复核。\n- `hydrated_videos.csv` 是可选后续输入；未取得之前，评论均值与中位数明确记为‘未计算’。"))
save(e, "EDTok_TikTok_dataset_analysis.ipynb")
