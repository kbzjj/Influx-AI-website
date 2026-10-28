# 方案四源码与动效学习索引

## 修改日志

| 版本 | 日期 | 修改内容 |
| --- | --- | --- |
| 1.5 | 2026-10-27 | 更新项目实体目录与本地快照重建路径，清除构建对 skill 的读写依赖。 |
| 1.4 | 2026-10-26 | 右侧资源图片与徽章再下移30px，总错位更新为80px。 |
| 1.3 | 2026-10-26 | 补充资源媒体独立高度及原模板响应式断点。 |
| 1.2 | 2026-10-26 | 更新流程照片结构与选择器；删除旧图表、徽章和示例图注说明。 |
| 1.1 | 2026-10-26 | 更新资源合并选择器、首屏头像昵称、轮播中线测量与提交按钮说明。 |

## 先看哪些文件

1. 打开本地预览，再阅读 `index.html`。页面保留原始 Reels class 与时间线目标；紧凑 HTML 是源站公开输出的结构。
2. 阅读 `influx.css`：品牌覆盖集中在这里，不改原始资产 CSS。
3. 阅读 `copy.js` 与 `influx.js`：文案与前端本地逻辑独立于原始动效。
4. 原始布局：`assets/8541643a1d-reels-wbs.webflow.shared.c930502d8.css`。
5. 原始时间线：`assets/ebe1d0e61c-webflow.ae5bb349.bb882b5f4ad9a603.js`；可搜索 `service-card`、`step-title`、`scroll-item`、`button`、`scrub`、`timelineIds`。

## 区块对照

| 页面 / 区域 | 实际入口 | 原模板来源与调整 |
| --- | --- | --- |
| 顶部导航 | `.site-header`、`.desktop-nav`、`.mobile-navigation` | 按用户要求延续方案三；手机有可收起的三项导航。 |
| 首屏 | `#home .hero-title-wrap`、`.hero-reels-info`、`.hero-creator-card` | Reels 首屏原节点；保留三段视频、中心卡和胶囊跑马灯，恢复模板头像与昵称，移除认证和粉丝量及首屏演示图注。 |
| 平台条 | `.hero-social-platform .marquee-item` | Reels ticker，平台限制为 TikTok、YouTube、Instagram、X。 |
| 服务 | `#managed .service-sticky .service-card` | 原四卡滚动结构与时间线；内容替换为四项已确认服务，数字改为 01–04 顺序号。 |
| 服务报价 | `#project-quote .quote-summary` | 将报价信息放在独立容器，避免与原服务 sticky 容器互相覆盖；属于 Influx 内容适配。 |
| 全球资源 | `#resources .grid-mission`、`.mission-right .counter-right`、`.counter-marquee` | 将原 mission 双影像与 counter 指标白卡合并，保留 210M+、120+、4、3 和平台条；移除独立 network 区。 |
| 技术能力 | `#capabilities .case-study-slider`、`.w-slide` | 原三页案例轮播扩为四页产品能力；图片保留 2880×1800 intrinsic size 避免懒加载前高度为零。 |
| 合作流程 | `#how-it-works .step-info`、`.step-card-item` | 保留原分词标题与流程卡旋转/位移；四卡顶部统一为 `.workflow-photo` 照片，复用 Reels `.step-image-wrap` 圆角边框，移除原列表、图表、徽章、图注与最后的 CTA。 |
| 联系 | `#contact .grid-hero-contact`、`#contact-form` | 原 Contact 布局及字段，精简为统一四字段；提交按钮移除左侧圆形图标，右侧保留普通箭头。 |
| 工具价格 | `pricing.html .pricing-content .pricing-card` | 原三卡；移除不适用的月/年开关及其负 margin，保留内容所需的三个展示单元。 |
| 计算器 | `free-tools.html #engagement-calculator`、`#engagement-result` | Contact 布局适配；公式和展示逻辑在 `influx.js`。 |

## 动画初始化顺序

页头加载源 CSS、字体和品牌覆盖。页尾依次加载 `copy.js`、`influx.js`，先完成翻译，再加载原 jQuery、Webflow chunks、页面配置、GSAP、ScrollTrigger、SplitText 和 Lenis。

保留原 `data-wf-page`、`data-wf-site`、class 及原动画顺序。Lenis 只初始化一次，使用原 `lerp: 0.1`、`wheelMultiplier: 1`，由 GSAP ticker 推进，滚动事件同步到 ScrollTrigger。

源页的 `[data-scroll="load"] [scroll-item="show"]` 用于滚动进场。工具及计算器成为独立首屏后，改用原 `[data="show"]` 加载时间线，避免首屏还在等待滚动触发。这是触发方式适配，没有另写一套进场动画。

`runtime-bridge.js` 在字体完成及 load 后刷新测量，处理进入深层锚点的初始位置。查看截图、法律预览时暂停 Lenis，关闭后恢复。

## 可调整参数

- 资源图片高度由 `#resources .mission-left` 的 `--resource-media-height` 独立控制：默认 390px，991px 以下 300px，479px 以下 250px，均沿用原模板视频高度；第二张保留原50px内边距，增加30px顶部外边距，使图片与徽章整体下移，总错位为80px，不依赖数据卡高度。
- 品牌色与字号在 `influx.css` 的 CSS 变量和对应区块规则；不要修改原压缩动画文件来改颜色。
- Reels 在手机断点会在 `body` 重声明字体变量，因此品牌覆盖同时作用于 `body.influx-site`，确保英文仍使用方案三的 Inter Display。
- 中英文文本在 `copy.js`，DOM 通过 `data-copy` 绑定。按钮上下两个文本节点共同使用一个文案 key，第二份对辅助技术隐藏。
- 原按钮文本高度与本次字体不同，`influx.css` 将可视窗限制为一行，使 hover 时上下两行交换且不露出下一行。
- 源服务卡末态实测缩放为 0.55 / 0.65 / 0.75 / 0.85，并横向错位；源与适配版使用同一时间线。
- 技术截图用原 Slider 的箭头、分页与过渡。两侧箭头位于可见 `.grid-case-card` 的竖直中点；`runtime-bridge.js` 通过 ResizeObserver 与 aria-hidden 变化同步 `--capability-control-y`，适配语言、断点和卡片高度。完整图片展示使用原生 dialog。
- 流程四张照片来自模板原服务图片，复用现有资源；仅作为设计素材，不表示真实团队或项目。图注已按用户本轮要求移除。

## 本地业务逻辑

表单在 document capture 阶段拦截 submit，校验通过后最多保存 20 条到 `influx-v4-inquiries`；不触发原 Webflow 的远程提交。未提交草稿放在会话存储，语言切换前保存；用户输入不因套餐来源预填而被覆盖。

工具来源通过 `?intent=free` 或 `?intent=plus` 进入首页联系模块；来源不构成开通或付费授权。计算器用有限、非负整数输入，粉丝数大于零，结果保留最多两位小数。

## 修改和重建

直接改 HTML、CSS、文案和脚本即可刷新预览。`scripts/build.py` / `scripts/dom.py` 保存了从 Reels 原始节点抽取和文案装配的步骤；如需重建，可执行 `python3 versions/方案四/scripts/build.py`，脚本自动定位项目根目录，读取本目录 `_source/index.html.txt` 和 `_source/contact-index.html.txt`；不读取或写入 skill 目录，也不创建符号链接。重建会覆盖三个 HTML 和 `copy.js`，请先保存手工编辑，不会重建或覆盖 `influx.css` / `influx.js`。

## 验证入口

见 `qa/verification.md`。`qa/static-audit.json` 由技能自带审计器生成；`qa/scheme-three-baseline.json` 用于确认旧方案未改。截图为实际浏览器输出，不是生成示意图。
