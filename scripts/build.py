#!/usr/bin/env python3
"""Build a dependency-free, subpath-safe Chinese course reference site."""
from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs'
ORIGIN = 'https://eecs498-aase.github.io/'
CHECKED = '2026-10-21'
CAL = 'c_9df0ad5ebcf778747b62541cd1fd9c4ec6016fe57b3114b1e6345afe8a980fa5%40group.calendar.google.com'
CALENDAR = 'https://calendar.google.com/calendar/embed?src=' + CAL + '&ctz=America%2FDetroit'
ADD_CAL = 'https://calendar.google.com/calendar/render?cid=' + CAL
ICAL = 'https://calendar.google.com/calendar/ical/' + CAL + '/public/basic.ics'
STAFF = 'eecs-aase-staff@umich.edu'
NAV = [('index.html','课程概览'),('syllabus.html','教学大纲'),('faq.html','常见问题'),('podcast/index.html','课程播客')]

def link(url, text, cls=''):
    external = url.startswith('https://')
    attrs = ' target="_blank" rel="noopener noreferrer"' if external else ''
    return f'<a href="{escape(url, quote=True)}" class="{cls}"{attrs}>{text}</a>'

def section(id, no, label, title, body):
    return f'<section id="{id}" class="section"><p class="eyebrow">{no} / {label}</p><h2>{title}</h2>{body}</section>'

def cards(items):
    return '<div class="cards">'+''.join(f'<article class="card"><h3>{a}</h3><p>{b}</p></article>' for a,b in items)+'</div>'

def bullets(items):
    return '<ul>'+''.join(f'<li>{s}</li>' for s in items)+'</ul>'

def page(path, title, body, source=None):
    depth = path.count('/')
    rel = '../'*depth
    source = source or ('index.html' if path == '404.html' else path)
    nav = ''.join(f'<a href="{rel}{p}"'+(' aria-current="page"' if path==p else '')+f'>{t}</a>' for p,t in NAV)
    original = ORIGIN + source
    base = '<base href="https://yuyaxiong.github.io/eecs498-aase-zh/">' if path == '404.html' else ''
    text = f'''<!doctype html>
<html lang="zh-Hans"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
{base}<title>{title} · AASE 非官方中文课程资料</title><meta name="description" content="密歇根大学 EECS 498-016 AASE 2026秋季课程的非官方中文资料整理。课程概览、大纲、课表、常见问题和英文播客入口。政策以原站为准。">
<meta name="theme-color" content="#00274c"><meta property="og:title" content="{title} · AASE 非官方中文课程资料"><meta property="og:type" content="website">
<link rel="icon" href="{rel}assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="{rel}assets/style.css">
<script defer src="{rel}assets/app.js"></script></head><body>
<a class="skip" href="#main">跳到正文</a><header><div class="wrap head"><a class="brand" href="{rel}index.html"><span class="brand-symbol" aria-hidden="true">A²</span><span><strong>AASE <small>中文</small></strong><span class="brand-sub">EECS 498 · 2026 秋季</span></span></a>
<button class="menu-toggle" aria-controls="nav" aria-expanded="false" aria-label="展开导航菜单" hidden>菜单 <span aria-hidden="true">☰</span></button><nav id="nav" aria-label="主导航">{nav}</nav></div></header>
<div class="notice"><div class="wrap"><strong>非官方中文资料整理</strong><span>课程信息以英文原站为准 · 核对日期 {CHECKED}</span>{link(original,'对应原文 ↗')}{link(rel+'about.html','来源与译注')}</div></div>
<main id="main" class="wrap">{body}</main><footer><div class="wrap"><div class="footer-top"><div><strong>AASE / 应用智能体软件工程</strong><p>独立中文学习参考 · 非校方网站</p></div><div class="footer-links">{link(rel+'about.html','来源与译注')}{link(ORIGIN,'英文原站 ↗')}{link('https://github.com/eecs498-aase','课程 GitHub ↗')}{link('mailto:'+STAFF,'联系原课程团队')}</div></div><p class="fine">原课程内容版权标示：© 2026 University of Michigan · EECS 498-016。课程名称、人物及第三方资料归原权利人所有。本项目不代表密歇根大学或原课程团队，中文整理可能存在误差。</p></div></footer></body></html>'''
    dest=OUT/path
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(text, encoding='utf-8')

def hero(kicker, title, desc):
    return f'<div class="page-hero"><p class="eyebrow">{kicker}</p><h1>{title}</h1><p class="lede">{desc}</p></div>'

def calendar_links():
    return '<div class="link-row">'+link(CALENDAR,'查看答疑日历 ↗')+link(ADD_CAL,'添加到 Google 日历 ↗')+link(ICAL,'订阅 iCal（Apple / Outlook）')+'</div>'

PHASES=[('01','应用 / Apply','第1–3周 · 项目延续至第6周','18%','Aider、16个引导练习、结对编程工具。L01–L06；项目截止：10月6日（周二）。'),('02','分析 / Analyze','第4–7周','22.5%','直接使用 LLM API，自建工具调用、审批、智能体循环与评测。L07–L14；Agent v0 截止：第7周末。'),('03','创造 / Create','第8–15周','49.5%','知识库、设计技能、权限与上下文加固、会话记忆、Web服务与部署。L15–L28；展示：12月10日。')]
phase_html='<div class="phase-grid">'+''.join(f'<article class="phase"><span class="phase-num">{n}</span><p class="meta">{when}</p><h3>{name}</h3><p>{desc}</p><strong class="weight">{weight}</strong></article>' for n,name,when,weight,desc in PHASES)+'</div>'
intro='''<section class="hero"><div><p class="eyebrow">UNIVERSITY OF MICHIGAN / EECS 498-016</p><h1>应用<span class="yellow">智能体</span><br>软件工程</h1><p class="english">Applied Agentic Software Engineering</p><p class="lede">2026 秋季 · 4 学分<br>围绕编程智能体，学习使用、分析与构建。</p><div class="actions"><a class="button primary" href="syllabus.html">阅读教学大纲 <span aria-hidden="true">→</span></a><a class="text-link" href="faq.html">先看常见问题</a></div></div><div class="terminal" aria-label="编程智能体流程示意，非实际运行终端"><div class="terminal-bar"><span>● ● ●</span> aase / learning with agents</div><pre><span class="yellow">$</span> aider --model ollama/qwen3.5:9b

<span class="muted">01</span> 提供需求与上下文
<span class="muted">02</span> 审查工具调用与代码修改
<span class="muted">03</span> 运行测试，定位失败

<span class="green">✓</span> 用验证结果检验实现
<span class="muted">课程流程示意</span></pre></div></section><div class="facts"><div><b>4 学分</b><span>计算机高阶技术选修</span></div><div><b>周二 / 周四</b><span>讲座 15:00–16:30</span></div><div><b>周一或周二</b><span>每周 2 小时实验</span></div><div><b>无考试</b><span>项目、实验与现场展示</span></div></div><p class="fine timezone">课程日期与时间均按美国底特律当地时间（America/Detroit）；不是北京时间。</p>'''
intro+=section('premise','01','课程定位','从使用工具，到理解系统',cards([('面向谁','先修 EECS 281 和 EECS 201，或具有高阶计算机课程资格（ULCS），或获得教师许可。'),('学习方式','28次讲座、13次实验、3次晚间黑客松。项目均独立完成，使用 AI 是课程要求。')]))
intro+=section('phases','02','三个阶段','一个项目，持续演进',phase_html+'<p class="note">另有 10% 平时管理成绩。三阶段分别占总成绩的 18%、22.5%、49.5%；详情见教学大纲。</p>')
intro+=section('outcomes','03','学习目标','你将练习的核心能力',bullets(['利用上下文、模型、提示词三个维度定位编程智能体的问题。','设计并实现结对编程工具，编写规格、架构图与测试。','实现工具调用、审批层、停止条件及自主运行循环。','用任务集、成功率、成本和延迟评估智能体，建立回归检查。','为助手接入知识库、持久记忆、设计方法、Web服务和终端之外的交互渠道。']))
intro+=section('tools','04','工具与成本','本地模型优先', '<p>工具包括 Aider、Ollama / llama.cpp、Python、git / GitHub、pytest、LLM API 与 PrairieLearn。课程无必购教材、模型 API 或编程助手订阅；硬件不足可向课程团队咨询 CAEN 机房。</p><div class="chips">'+''.join(f'<span>{x}</span>' for x in ['Aider','Ollama','Qwen3.5','Python','GitHub','pytest','PrairieLearn'])+'</div>')
people=[('Marcus Darden','授课教师','mmdarden@umich.edu'),('Rafe Symonds','研究生助教 / GSI','rsymonds@umich.edu'),('Zilin Wang','研究生助教 / GSI','zilinwan@umich.edu'),('Rushil Kagithala','本科教学助理 / IA','ksrushil@umich.edu')]
intro+=section('staff','05','教学团队','联系与答疑','<div class="people">'+''.join(f'<article><h3>{n}</h3><p class="meta">{r}</p>{link("mailto:"+m,m)}</article>' for n,r,m in people)+'</div><p>课程团队统一邮箱：'+link('mailto:'+STAFF,STAFF)+'</p><h3>答疑时间</h3><p>地点与时间由课程日历维护；请查看原始日历中的最新安排。</p>'+calendar_links())
intro+='<div class="callout"><div><h2>查看完整课程安排</h2><p>学期：2026年8月31日–12月11日。选课学生须同时关注 Ed 上的官方通知。</p></div><a class="button" href="syllabus.html">查看大纲与课表 →</a></div>'
page('index.html','课程概览',intro)

# Calendar facts, independently rendered rather than copying source markup.
weeks=[
['8/31–9/4','Lab 00：环境配置，启动模型并连接 Aider；首次讲座前完成','L01 课程导论与 AI 编程概况','L02 大语言模型生成代码的原理','周二发放个人仓库'],
['9/7–9/11','劳动节（9/7），无实验','L03 上下文、模型、提示词','L04 规格驱动开发','9/11（周五）：环境验收与引导练习截止'],
['9/14–9/18','Lab 01：Aider 内部机制、黑客松说明与项目公布','L05 现代智能体命令行工具','L06 从结对编程到智能体编排','开始结对编程工具项目'],
['9/21–9/25','Lab 02：有助教支持的项目开发','L07 LLM API 与客户端内部机制','L08 工具使用、函数调用与智能体循环','9/24（周四）晚：黑客松1'],
['9/28–10/2','Lab 03：工具、函数调用与循环','L09 停止条件与审批层','L10 本地模型服务概览','本周末形成可运行的智能体'],
['10/5–10/9','Lab 04：无人值守运行与代价测量','L11 编辑格式与解析器评测','L12 为运行框架设计提示词','10/6（周二）：Apply项目截止；Analyze规格发布'],
['10/12–10/16','Lab 05：评测框架与 Agent v0 加固','L13 评测：任务集、成功率、成本与延迟','L14 安全约束与失败模式','Analyze本周末截止；黑客松2日期原文待公布'],
['10/19–10/23','秋季学习假（周一、周二），无实验','学习假，无课','L15 LLM Wiki、OKF 与 RAG 替代方案','开始构建知识库'],
['10/26–10/30','Lab 06：知识库 ingest / query / lint','L16 将大象—金鱼模型实现为技能','L17 设计与软件开发',''],
['11/2–11/6','Lab 07：为现有编程智能体构建 EGM 技能','L18 权限策略及其失效方式','L19 仓库提示注入攻击',''],
['11/9–11/13','Lab 08：加固第5周的审批层','L20 上下文管理与压缩','L21 工具接口与小模型的工程要求',''],
['11/16–11/20','Lab 09：上下文窗口满时的处理','L22 会话与记忆','L23 开发过程证据记录',''],
['11/23–11/27','Lab 10：会话、记录与基线验收','L24 测试智能体与回归验收','感恩节，无课','11/25–11/27：感恩节假期'],
['11/30–12/4','Lab 11：智能体测试与回归套件','L25 Web服务与交互渠道','L26 接入 Wiki 记忆与 EGM 方法',''],
['12/7–12/11','Lab 12：集成实验','L27 部署与演示准备','L28 项目展示与课程总结','黑客松3日期原文待公布；12/11结课']]

def schedule():
    rows=''.join(f'<tr><th scope="row">第{i+1}周<small>{w[0]}</small></th>'+''.join(f'<td>{c or "—"}</td>' for c in w[1:])+'</tr>' for i,w in enumerate(weeks))
    return '<p class="fine">小屏幕可左右滑动表格。周一与周二实验内容相同，每周选择一个时段参加。</p><div class="table-scroll" role="region" tabindex="0" aria-label="15周课程安排，可横向滚动"><table><caption>2026 秋季课表 · 15周 / 28次讲座 / 13次实验</caption><thead><tr><th scope="col">周次 / 日期</th><th scope="col">实验</th><th scope="col">周二讲座</th><th scope="col">周四讲座</th><th scope="col">里程碑</th></tr></thead><tbody>'+rows+'</tbody></table></div><p class="note">第4周同时包含 Apply 项目支持和 Analyze 讲座；Apply 项目延续到第6周。原站说明后半学期讲题可能微调。黑客松2、3的具体日期仍以官方公告为准，本译注不推测补全。</p>'

syllabus=hero('EECS 498-016 / FALL 2026','教学大纲','课程时间、每周主题、项目、成绩与政策。此页整理公开课程事实；正式要求请核对对应英文原文。')
chapters=[('glance','课程速览'),('description','课程介绍'),('schedule','每周课表'),('projects','项目与交付'),('hackathons','黑客松'),('grading','评分'),('policies','课程政策'),('tools','工具与费用'),('resources','课程资源')]
syllabus+='<nav class="toc" aria-label="大纲章节">'+''.join(link('#'+p,t) for p,t in chapters)+'</nav>'
syllabus+=section('glance','01','课程速览','安排与先修要求','<dl class="definition">'+''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k,v in [('课程','EECS 498-016 · 应用智能体软件工程'),('学分','4 · 计算机高阶技术选修'),('学期','2026年8月31日–12月11日'),('讲座','周二、周四 15:00–16:30 · LCSIB 2365'),('实验','周一 15:30–17:30 · GGBL 2153；或周二 12:30–14:30 · DOW 1005'),('时区','America/Detroit（美国底特律当地时间，随夏令时变化）'),('考核','项目、实验、黑客松；无考试'),('先修','EECS 281 与 EECS 201；或 ULCS 资格；或教师许可'),('语言','Python、Shell、git'),('联系',link('mailto:'+STAFF,STAFF))])+'</dl>')
syllabus+=section('description','02','课程介绍','应用 → 分析 → 创造',phase_html+'<p>全学期围绕一个持续演进的代码仓库。使用 AI、规格设计、测试、评测和解释实现都是学习与考核的一部分。项目不仅要求能运行，也要求能解释设计与失败原因。</p>')
syllabus+=section('schedule','03','每周课表','15周课程安排',schedule())
syllabus+=section('projects','04','项目与交付','三阶段的交付要求', '''<p>第3周起的工作在同一 git 仓库演进。个人课程仓库通过 GitHub 邀请发放；一般作业按截止时仓库快照评分，黑客松在 PrairieLearn 提交。</p>
<article class="project"><p class="meta">APPLY / 18%</p><h3>引导练习与结对编程工具</h3><p>第1–2周共16个 Aider 练习，涉及任务管理 CLI 和基于同一数据的 Web 前端；9月11日截止。第3–6周实现结对编程工具：7项功能、YAML配置；10月6日截止。项目负担原文标记为重新设计中。</p><h4>评分细目（项目内分值）</h4><div class="two-col"><div><h4>规格与设计：50分</h4>'''+bullets(['需求10；架构/接口10；Aider分步实现计划10。','图示10：组件图4、时序图3、生命周期图3。','先写规格后写代码5；说明变更与原因5。'])+'''</div><div><h4>实现与测试：50分</h4>'''+bullets(['功能正确性25；自定义测试9；失败路径测试8。','端到端运行与现场证据5；操作说明3。'])+'''</div></div><p>交付包含系统/增量规格、三种图、学生编写的测试、YAML示例、开发与运行说明、会话记录、AI_LOG.md、设计与实现对照。模型披露与证据索引是核验依据，不单独计分。测试按能否发现合理缺陷计分；正确揭示失败的测试仍可获得测试分。同一缺陷不跨其他合格产物重复扣分。</p></article>
<article class="project"><p class="meta">ANALYZE / 22.5%</p><h3>Agent v0</h3><p>10月6日发布，第7周末截止；预计3周共22–27小时。工具层需支持读、写、执行，通过真实函数调用接入；危险操作先人工审批，再加入规则审批和决策日志。实现6个停止条件、自主循环及评测套件。</p>'''+bullets(['验收任务随规格公开，可在提交前持续调优。','至少8个评测任务，每个至少运行3次，报告成功率。','提供失败分析报告，说明仍无法完成的任务。','第7周黑客松包含无人值守验收。'])+'''</article>
<article class="project"><p class="meta">CREATE / 49.5%</p><h3>知识库、设计技能与可部署助手</h3><p>第8–15周。构建可 ingest / query / lint 的 Markdown 知识库；实现设计优先技能；加固权限、抗注入、上下文、会话及回归检查；最后接入 Web服务与至少一个终端以外的渠道。</p>'''+bullets(['每阶段通过可计分的基线验收。','第14–15周加入自选渠道，以及第7周失败分析中提出的一项能力。','期末交付格式及细分比例待课程公告；全部为个人项目。'])+'</article>')
syllabus+=section('hackathons','05','黑客松','3次晚间现场实践',cards([('第1次 · 9月24日（周四）','第4周；现场公布任务，在即将提交的项目代码上开发。'),('第2次 · 第7周','Agent v0 无人值守验收；原文仍标为具体日期待公布。'),('第3次 · 第15周','最终助手的现场展示；原文仍标为具体日期待公布。')])+'''<p>课程提供浏览器 VS Code、Aider、模型端点及已克隆仓库。活动计分。预约时段2小时，教室额外开放1小时，可在同场提供最多150%的延时；更长延时、低干扰环境或替代时间请第一周联系团队。因工作、照护或其他课程无法到场，应提前安排受监督的补做场次。</p>''')
syllabus+=section('grading','06','评分','成绩构成与等级', '''<div class="grade-bar" role="img" aria-label="平时10%，应用18%，分析22.5%，创造49.5%"><span style="flex:10">10</span><span style="flex:18">18</span><span style="flex:22.5">22.5</span><span style="flex:49.5">49.5</span></div>'''+cards([('平时管理 · 10%','讲座出勤占本项60%，实验占40%，分别计算。Poll Everywhere核验现场出勤；激励加分以课程公告为准。'),('Apply · 18%','本阶段内：16个练习25%（含环境验收），结对编程项目25%（总评4.5%），黑客松1占50%。'),('Analyze · 22.5%','Agent v0验收、评测与测量、失败分析、黑客松2；细分以官方公告为准。'),('Create · 49.5%','知识库/技能/加固智能体的阶段验收、最终助手及黑客松3；细分随期末格式公布。')])+'''<p>非平时部分占90%，按20:25:55分配。验收按任务完成比例评分，并非仅通过/不通过。截止前可反复测试；没有截止后的重做期。</p><h3>出勤计算</h3><p>讲座20/28次、实验10/13次分别达到全额出勤分要求；不足70%时，按实际出勤率÷70%计算对应项得分。原站将8次讲座和3次实验的余量作为一般缺勤安排。</p><h3>等级下限</h3><div class="scale">'''+''.join(f'<span><b>{g}</b>{v}</span>' for g,v in [('A+','97–100'),('A','93–96'),('A−','90–92'),('B+','87–89'),('B','83–86'),('B−','80–82'),('C+','77–79'),('C','73–76'),('C−','70–72'),('D','60–69'),('F','低于60')])+'''</div><p class="fine">原站说明这些是保证的最低边界，只可能向有利于学生的方向调整。</p>''')
syllabus+=section('policies','07','课程政策','提交、出勤与协作规则', '''<div class="policy-list"><article><h3>学术诚信与 AI 使用</h3>'''+bullets(['必须使用 AI，并理解、能解释提交的每行代码；规格、图、实现和测试均遵守阶段模型/工具规则。','记录工具、模型和提示词；不得复制其他学生的代码、提示词或报告；引用往届或外部成果须注明来源。','实验验收和黑客松现场验证理解；违规按工程学院荣誉准则处理。'])+'''</article><article><h3>出勤</h3><p>讲座、实验、黑客松均为必参加环节。讲座与实验使用 Poll Everywhere；实验按任务说明完成。Lab01、Lab02支持项目，不另设项目分提交。未经事先批准缺席实验的验收，FAQ说明该次验收为零分。</p></article><article><h3>迟交与延期</h3>'''+bullets(['无可自由使用的迟交天数，也无重做期。','项目每迟交一个自然日扣10%，最多接受3天，超过3天不计分。','按截止时仓库快照评分；黑客松在现场通过PrairieLearn提交。','有证明的紧急情况逐案考虑延期，须在截止前联系团队。'])+'''</article><article><h3>协作</h3><p>全部工作独立完成。可讨论概念、共同排查问题，不得共享提交用的代码、提示词或报告。</p></article><article><h3>无障碍支持</h3><p>请联系 '''+link('https://ssd.umich.edu/','Services for Students with Disabilities（SSD）')+'''，并在开学前两周内向教师提供支持信；黑客松特殊安排见上文。</p></article><article><h3>学生支持</h3><p>原站政策页列有 Counseling and Psychological Services（CAPS）与 Dean of Students Office 等支持资源。联系方式请直接核对 '''+link(ORIGIN+'syllabus.html#policies','官方课程政策与学生支持资源')+'''。</p></article></div>''')
syllabus+=section('tools','08','工具与费用','配置要求与模型政策', '''<h3>环境</h3>'''+bullets(['macOS、Linux或Windows+WSL笔记本；不要求独立GPU。','大纲要求Python 3.12、git、GitHub账号。FAQ另写Python 3.11+，存在原文差异；建议按大纲并向团队核实。','Ollama或llama.cpp提供模型服务；Aider用于初期工具使用。第1周配置实验提供现场帮助，第2周另有监督配置窗口。','不要求付费订阅；可选托管服务的凭证依服务而异，放在git之外。'])+'''<h3>Stage 1 模型限制</h3><p>允许 qwen3.5:4b 与 qwen3.5:9b，推荐9B；现场监督环节还可使用课程宣布的模型。同一限制覆盖规格起草与审查、图、说明、代码、测试和辅助模型；其他模型须有正式政策修订。</p><p>允许模型可部署在实现作业所需 OpenAI-compatible Chat Completions 合约的端点上。YAML应配置API base、model ID、凭证变量名、预算、超时和temperature；应用中不硬编码Ollama专用API或主机名。换服务商不意味着允许换模型。</p><h3>费用</h3><p>除可运行小模型的机器外，无必购教材、必需LLM支出。CAEN机房是免费硬件替代方案；需要支持请第一周告知团队。黑客松模型端点由课程提供。</p>''')
syllabus+=section('resources','09','课程资源','代码、日历与沟通', '''<div class="resource-grid"><article><h3>公开课程资料</h3>'''+bullets([link('https://github.com/eecs498-aase','课程 GitHub 组织 ↗'),link('https://github.com/eecs498-aase/materials','已公开讲座与实验课件 ↗'),link('https://github.com/eecs498-aase/aider-ollama','Aider / Ollama 与 CAEN 连接资料 ↗')])+'''<p>个人课程仓库在第1周配置实验后通过邀请发放，请留意邮箱并接受邀请。本中文站不提供私有仓库的副本。</p></article><article><h3>沟通与答疑</h3>'''+bullets([link('https://edstem.org','Ed 讨论平台 ↗'),link('mailto:'+STAFF,STAFF)])+calendar_links()+'''</article></div><h3>录制与播客</h3><p>课程使用 CAEN capture 与 Zoom 录制讲座。播客含课前 Brief、课后 Deep Dive，使用课程材料与去标识化讲座转录生成 AI 音频。学生不应可被识别。删除请求可发原课程团队；已被客户端下载的音频不受取消发布影响。</p>'''+link('podcast/index.html','前往课程播客 →')+'''<h3>原站致谢</h3><p>Dan Disler（IndyDevDan）、Aider 作者 Paul Gauthier、Andrew DeOrio、Suraj Rampure。详细贡献说明见英文原站。</p>''')
page('syllabus.html','教学大纲',syllabus)

FAQ=[
('课程内容',[
('AASE 怎么读？','原课程读作“A two S E”。前两个A分别对应Applied、Agentic。'),
('这门课学什么？','三阶段：Apply用Aider做结对编程工具；Analyze实现Agent v0；Create接入知识库、技能和部署。详情见教学大纲。'),
('能替代传统软件工程课程吗？','它建立在已有软件工程与编程能力上，重点增加AI工具控制、智能体系统设计及评测。'),
('内容会过时吗？','原站说明每期开课会修订工具；核心主题包括上下文、工具调用、循环、审批、评测与架构。'),
('使用什么编程语言？','Python，并使用Shell与git；需要能够自行学习库，课程不讲基本语法。')]),
('工具与模型',[
('会使用哪些工具？','初期使用Aider，可由Ollama等兼容端点提供允许模型；后续直接调用Chat Completions API并实现自己的智能体。不要求付费编程助手。'),
('可以换用最新模型吗？','Stage 1仅允许qwen3.5:4b、qwen3.5:9b（推荐9B），以及监督环节宣布的课程模型；其他模型须有正式政策修订。设计、代码、测试和辅助模型均受限制，AI_LOG.md记录实际模型ID与托管方式。'),
('能选择哪些LLM服务商？','使用作业规定的OpenAI-compatible Chat Completions接口；可本地Ollama/llama.cpp，也可选择托管的合规模型。YAML配置端点，不能硬编码供应商。'),
('开课前需要准备API key吗？','不要求购买API服务；本地托管无需供应商账号。可选托管服务可能需要凭证，不能提交到git。第1周配置实验有现场帮助，第2周提供额外监督窗口。'),
('能用LangChain做最终项目吗？','不能用框架替代要求自行实现的智能体循环、工具层、审批层、状态和评测。httpx、sqlite3、CLI工具库等实用库可以使用。')]),
('先修与准备',[
('需要AI编程工具经验吗？','不需要；第1–2周16个Aider引导练习用于建立基础。'),
('需要机器学习背景吗？','不需要训练模型或推导梯度；第2讲介绍LLM原理。需要扎实编程能力与学习库的能力。'),
('EECS 281是硬性先修吗？','公开要求为EECS 281与EECS 201，或ULCS资格，或教师许可。有同等经验者可联系教师询问许可。')]),
('安排与工作量',[
('每周要投入多久？','平均12–15小时：讲座3小时、实验2小时、练习/项目与调试6–8小时；另有3次晚间黑客松。学期末可能每周15–20小时。'),
('软硬件要求是什么？','Python、git、编辑器、Ollama/llama.cpp及Aider；macOS、Linux或Windows+WSL，不要求GPU。大纲写Python 3.12，FAQ写3.11+，请按大纲并向团队核实。机器不足可用CAEN或询问课程端点。'),
('可以旁听吗？','EECS 498试验课程阶段不开放正式旁听。原站说明教室容量允许时可到场听讲，部分材料可能公开；具体权限请联系教师。'),
('有考试吗？','没有。第4、7、15周有3次计分黑客松，使用课程提供的环境。第1次为9月24日晚；无法参加须提前安排补做。最多150%延时可同场完成，其他支持另行安排。'),
('成绩怎么分配？','平时10%、Apply 18%、Analyze 22.5%、Create 49.5%。Apply内部：练习25%、项目25%、黑客松1占50%；项目本身规格设计50%、实现测试50%。等级阈值见大纲。'),
('期末展示是什么形式？','FAQ列第15周12月8–10日，每人约30分钟：现场演示（建议备录像）、设计取舍、实现问答、评测与成本。首页展示日期列12月10日，具体个人时段以公告为准。'),
('实验验收如何进行？','通常5–10分钟，向助教展示成果并答问。未完成也应到场，能够解释的部分进展仍有价值。')]),
('课程政策',[
('可以结对交项目吗？','所有阶段项目均独立提交。可讨论概念、一起调试，不可共享要提交的代码、提示词与报告。'),
('AI使用如何考核？','必须使用AI，记录工具、模型、提示词；需要理解并解释提交内容，实验和期末展示会核验。'),
('必须出勤吗？','讲座与实验强制，分别占平时项60%/40%；20/28讲、10/13实验达到全额要求。低于70%按比例计算。Poll Everywhere核验现场；实验验收缺席规则见大纲。'),
('跟不上怎么办？','尽早联系教学团队和参加答疑。有证明的紧急情况可申请个别调整；在截止前提出申请。')]),
('费用',[
('课程需要额外花钱吗？','无必购教材与LLM费用。本地模型或CAEN提供免费路径，托管服务可选。仍需测量token用量、运行耗时和每秒token数；Lab01起使用Aider /tokens，Analyze评估成本和延迟。')])]
faq=hero('QUESTIONS / ANSWERS','常见问题','按课程内容、工具、先修、安排、政策与费用分组。答案为中文事实整理；有歧义时请返回原文并联系课程团队。')
faq+='<div class="filter-tools" hidden><label for="faq-search">搜索问题与答案</label><div class="search-row"><input id="faq-search" type="search" placeholder="例如：模型、截止、Python" autocomplete="off"><button id="faq-clear" type="button">清空搜索</button></div><p id="faq-count" class="fine" role="status" aria-live="polite"></p></div>'
for i,(cat,items) in enumerate(FAQ,1):
    faq+=f'<section class="faq-group section"><p class="eyebrow">{i:02} / {cat}</p>'+''.join(f'<details class="faq-item"><summary>{q}<span aria-hidden="true">+</span></summary><div class="faq-answer"><p>{a}</p></div></details>' for q,a in items)+'</section>'
faq+='<p id="faq-empty" class="empty" hidden>没有找到匹配的问题。请换个关键词，或清空搜索查看全部问题。</p>'
faq+=section('contact','07','联系','仍有疑问',cards([('课程团队',link('mailto:'+STAFF,STAFF)+' · 行政、延期与私人事项。'),('公开课程资料',link('https://github.com/eecs498-aase','课程 GitHub 组织 ↗')),('授课教师',link('mailto:mmdarden@umich.edu','Marcus Darden · mmdarden@umich.edu')),('研究生助教',link('mailto:rsymonds@umich.edu','Rafe Symonds · rsymonds@umich.edu'))])+'<p class="note">原FAQ末尾仍将讨论平台与答疑标为待公布，而大纲已列出Ed与课程日历。此处将此差异作为译注保留，最新安排请查大纲与原日历。</p>'+calendar_links())
page('faq.html','常见问题',faq)

EPISODES=[
(1,'L01','brief','课程导论与 AI 编程概况','1:31','1_fzbfsvw9'),
(2,'L02','brief','大语言模型如何生成代码','1:39','1_dcs6iy8q'),
(3,'L03','brief','上下文、模型与提示词','1:30','1_3gu2d6ny'),
(4,'L01','deep','课程导论与 AI 编程概况','19:47','1_c4v8h3b6'),
(5,'L01','deep','课程导论与 AI 编程概况（完整版）','49:10','1_t0ocv3yl'),
(6,'L04','brief','规格驱动编程','1:39','1_bhtxs9i6'),
(7,'L05','brief','现代智能体命令行工具','1:29','1_bpaomshh')]
podcast=hero('EECS AASE PODCAST / SEASON 1','课程播客','原课程的英文 AI 生成音频。Brief 是课前导听，Deep Dive 是课后深入回顾。此站整理节目索引，音频与逐字稿均链接原站。')
podcast+='<section class="subscribe"><div><h2>订阅原版 RSS</h2><p>复制或打开原始订阅地址，在播客客户端添加。节目来源于课程材料与去标识化讲座转录。</p><p class="url">'+link(ORIGIN+'podcast/feed.xml',ORIGIN+'podcast/feed.xml')+'</p></div>'+link(ORIGIN+'podcast/feed.xml','打开 RSS ↗','button primary')+'</section><p class="note">Apple Podcasts 与 Spotify 的目录链接在原站仍待公布。RSS已提供。未制作中文配音或中文逐字稿。</p>'
podcast+='<section class="section"><p class="eyebrow">EPISODES</p><h2>节目列表 <small>7期</small></h2><div class="episode-tools" hidden><label for="episode-filter">节目类型</label><select id="episode-filter"><option value="all">全部节目</option><option value="brief">课前导听 / Brief</option><option value="deep">课后回顾 / Deep Dive</option></select><span id="episode-count" role="status" aria-live="polite" class="fine"></span></div><div class="episodes">'
for n,lecture,typ,title,duration,key in EPISODES:
    audio=f'https://www.mivideo.it.umich.edu/media/t/{key}/417405562'
    transcript=f'{ORIGIN}podcast/transcripts/s1e{n}.txt'
    podcast+=f'<article class="episode" data-type="{typ}"><div class="episode-number">{n:02}</div><div><p class="meta">第1季 · 第{n}期 · {lecture} · '+('课前导听 / Brief' if typ=='brief' else '课后回顾 / Deep Dive')+f'</p><h3>{title}</h3><p class="fine">英文 · AI生成音频 · {duration}</p><div class="link-row">'+link(audio,f'收听英文音频（{duration}）↗')+link(transcript,'英文逐字稿 ↗')+'</div></div></article>'
podcast+='</div></section><p class="fine">节目列表以核对日原站可见的7期为准，不推测尚未发布的节目。音频删除或隐私相关请求请联系原课程团队。</p>'
page('podcast/index.html','课程播客',podcast,'podcast/')

about=hero('SOURCES / TRANSLATION NOTES','来源与译注','这是独立维护的简体中文课程资料整理，不代表密歇根大学、EECS 498课程团队或任何第三方工具厂商。')
about+=section('source','01','原始来源','页面与资料归属',bullets([link(ORIGIN+'index.html','课程概览（英文）'),link(ORIGIN+'syllabus.html','教学大纲（英文）'),link(ORIGIN+'faq.html','FAQ（英文）'),link(ORIGIN+'podcast/','播客索引（英文）'),link('https://github.com/eecs498-aase','原课程 GitHub 组织')])+'<p>核对日期：2026年10月21日（Asia/Shanghai）。页面内容、外链和节目清单可能继续更新；选课、作业与政策均以官方通知为准。</p>')
about+=section('scope','02','整理范围','中文站包含与保留的内容',bullets(['中文页面覆盖公开主站的课程事实、安排、项目、成绩、政策、FAQ与节目入口。','未发现原站整站开放许可。中文正文采用独立编写的事实整理，不是逐字全文翻译；未复制原站长篇表达、照片、徽标、课件和音视频。','标题与技术术语采用必要中文释义；Aider、模型ID、API名、文件名、人员姓名、邮箱保持原有标识。','外部资料、英文播客、逐字稿、原RSS及日历继续访问原地址。本地不镜像第三方媒体，也不承诺外站免登录可用。']))
about+=section('notes','03','原文差异','需要留意的原站信息',cards([('Python版本','大纲：Python 3.12；FAQ：Python 3.11+。本中文站分别注明，请向团队核实。'),('讨论与答疑','FAQ末尾仍写TBD；大纲已列Ed与课程日历。两个原文入口均保留。'),('黑客松日期','第2、3次活动原文仍写9月5日前公布，但可见页面未补充具体日。此站保持“待公布”，不自行推定。'),('期末展示','概览列12月10日；FAQ列12月8–10日的个人展示安排。具体分配以官方公告为准。')]))
about+=section('rights','04','版权与致谢','原课程与资源保留原权利','<p>原站版权标示：© 2026 University of Michigan · EECS 498-016。原课程团队包括 Marcus Darden、Rafe Symonds、Zilin Wang、Rushil Kagithala。课程设计致谢 Dan Disler（IndyDevDan）、Paul Gauthier、Andrew DeOrio、Suraj Rampure。</p><p>本项目仅对独立编写的网站代码提供MIT许可，不改变课程资料、商标、人物信息或第三方资源的权利。若权利人提出更正或移除要求，应由中文站维护者处理；课程行政问题请联系原课程团队。</p>')
page('about.html','来源与译注',about,'index.html')
page('404.html','页面未找到',hero('404 / PAGE NOT FOUND','没有找到这个页面','链接可能已经变更。你可以返回课程概览，或打开官方原站继续查找。')+'<p><a class="button primary" href="index.html">返回课程概览</a></p><p>'+link(ORIGIN,'前往英文原站 ↗')+'</p>')
(OUT/'.nojekyll').write_text('')
(OUT/'data').mkdir(exist_ok=True)
(OUT/'data/course.json').write_text(json.dumps({'code':'EECS 498-016','term':'Fall 2026','credits':4,'timezone':'America/Detroit','checkedAt':CHECKED,'source':ORIGIN,'weeks':weeks,'faqCount':sum(len(items) for _,items in FAQ),'episodes':[{'number':n,'lecture':lecture,'type':typ,'title':title,'duration':duration,'audioUrl':f'https://www.mivideo.it.umich.edu/media/t/{key}/417405562','transcriptUrl':f'{ORIGIN}podcast/transcripts/s1e{n}.txt'} for n,lecture,typ,title,duration,key in EPISODES]},ensure_ascii=False,indent=2))
print('Built 6 HTML pages, 15 schedule weeks,',sum(len(x) for _,x in FAQ),'FAQ items, 7 episodes.')
