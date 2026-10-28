# Influx AI 官网预览

## 修改日志

| 版本 | 日期 | 修改内容 |
| --- | --- | --- |
| 1.1 | 2026-10-27 | 补充方案四项目独立存储与预览、构建入口，区分业务版本与参考模板库。 |

默认预览为方案二，源码位于 `versions/方案二/`。2026-10-23 新增 Reels 方向的独立首页方案三，位于 `versions/方案三/`。方案一及其相同的 `preview/` 副本已于 2026-10-23 按用户要求删除。

## 启动预览

双击 `启动预览.command`，然后打开 <http://127.0.0.1:4174/>，会直接进入方案二。预览运行时保留终端窗口，结束时按 Control+C。

也可以在项目根目录运行（无需安装 npm 依赖）：

```sh
python3 -m http.server 4174 --bind 127.0.0.1 --directory .
```

若端口已占用，可先打开预览地址。

## 页面入口

- 首页：<http://127.0.0.1:4174/versions/%E6%96%B9%E6%A1%88%E4%BA%8C/>
- 定价：<http://127.0.0.1:4174/versions/%E6%96%B9%E6%A1%88%E4%BA%8C/pricing.html>
- 免费工具：<http://127.0.0.1:4174/versions/%E6%96%B9%E6%A1%88%E4%BA%8C/free-tools.html>

## 项目内容

- `versions/方案二/`：现有官网方案，包含页面、样式、交互及本地素材。
- `.agents/skills/website-replica/assets/templates/`：Reels、Veo、Shinta 与 Relab 的模板实体及本地素材。
- `references/reels-webflow/`、`references/veo-public/`：指向技能内模板的兼容链接。
- `work/original/`：原站前端文件快照。
- `work/backups/`：方案二开发过程中的历史备份。
- `INFLUX_AI_VISUAL_REDESIGN.md` 和 `versions/方案二/README.md`：需求与历次实施记录，其中方案一的描述仅为历史记录。

当前为前端本地预览，未发布或接入后端。表单内容仅保存在浏览器本地。PC 视觉优先，移动端仍待统一调整及验收。


## Vercel 预览

2026-10-23 已将当前方案二部署为 Vercel Preview（READY）：

- 部署地址：<https://influx-ai-website-ff0bert1c-kb-zjj-5066s-projects.vercel.app>
- Vercel 默认访问保护保留；本次免登录分享链接见聊天记录，有效至 2026-10-30 10:31（Asia/Shanghai）。
- 已在线验证首页、定价、工具页面、头像图集加载，以及三个页面导航保持相同宽度。没有浏览器脚本错误或站内资源加载失败。
- 部署源码目录为 `versions/方案二/`，该目录包含 `vercel.json` 与 `.vercelignore`。使用 Vercel CLI 执行预览部署；本地认证与环境文件已加入忽略规则。

## Reels 前端学习参考

2026-10-23 新增 `references/reels-webflow/`，保存 Reels 公开演示站的 22 个页面及 245 个本地资源，保留原站布局、字体、视频和 Webflow / GSAP / Lenis 动效。原有官网方案保持不变。

- 双击 `references/reels-webflow/启动Reels预览.command` 后打开 <http://127.0.0.1:4175/>。
- 如果已使用本项目 4174 端口预览，打开 <http://127.0.0.1:4174/references/reels-webflow/>。
- 说明与验证记录：`references/reels-webflow/README.md`。
- 源码与动效学习索引：`references/reels-webflow/STUDY_GUIDE.md`。

## 网站模板中心

双击项目根目录的 `启动模板中心.command`，打开 <http://127.0.0.1:4176/>。点击封面即可启动并查看模板，也可搜索、按类别筛选、访问原站和学习指南；没有收藏、备注、重命名或删除管理。

- Reels：22 个公开页面，保留 Webflow / GSAP / Lenis 运行时。
- Veo：19 个公开页面，包含首页、Features、Gallery、Pricing、Contact、博客及法律页面，保留 Framer 运行时与本地 CMS 数据。
- Shinta：6 个一级公开页面：首页、Projects、About Us、Blog、Contact、404，保留 Framer / Motion / Lenis 运行时及原始动效。
- Relab：11 个一级公开页面，保留 Webflow / GSAP / Lenis 及创作者卡片、轮播和品牌分类交互。
- 所有模板实体统一保存到 `.agents/skills/website-replica/assets/templates/`；旧的 references 入口通过符号链接兼容，不另存重复副本。
- 后续调用此 skill 完成复刻后，模板与真实封面会登记入库，刷新中心即可看到。

无需安装 npm 依赖。手动启动：

```sh
python3 .agents/skills/website-replica/scripts/library.py --port 4176
```

保留服务窗口；Control+C 停止中心及由中心启动的模板预览。Veo 的 CMS 分段读取依赖此服务器，请优先从中心打开。详细验证记录位于各模板 `qa/verification.md`。

## 网站复刻 Skill

项目级技能位于 [`.agents/skills/website-replica/SKILL.md`](.agents/skills/website-replica/SKILL.md)，仅保存在本项目中。之后可在本项目的聊天中调用：

```text
使用 $website-replica 复刻 https://example.com/ 的前端视觉和动效，请先让我确认复刻范围。
```

技能会先确认页面范围，优先保留原站公开前端与素材，在技能内 `assets/templates/<site-slug>/` 完成本地化、视觉与动效对照、本地预览及学习文档，并自动登记到模板中心。不能完整获取时先说明具体缺口并求证，不默认改成近似实现或发布上线。附带的 Python 工具无需第三方依赖；静态下载和文件审计不能代替浏览器视觉验收。

该目录使用 [Codex 官方文档的项目级 skill 位置](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills)。如技能列表尚未出现，可直接提供上述 `SKILL.md` 路径要求使用，或重新打开 Codex。


## Reels 方向 · 方案三首页（2026-10-23）

按本轮确认范围新增独立方案三，仅重做首页；方案二和默认入口保留。

- 预览：<http://127.0.0.1:4174/versions/%E6%96%B9%E6%A1%88%E4%B8%89/>。
- 双击 `versions/方案三/启动方案三预览.command` 或使用根目录原有预览服务。
- 延续品牌紫蓝渐变，采用 Reels 参考的大字号、错落视频、滚动叠卡、逐词显现和合作流程。
- 人物与视频按用户授权暂用 Reels 参考素材，仅供本地视觉评审。中英文、截图放大、咨询弹窗、联系表单与法律提示保留。
- 定价与工具入口仍使用方案二；本轮没有发布或接入后端。
- 设计说明、素材映射及验证记录：`versions/方案三/README.md`、`versions/方案三/ASSET_SOURCES.json`、`versions/方案三/qa/`。

## 方案四官网设计

方案四实体位于 `versions/方案四/`，包含首页、工具与价格、免费计算器及全部运行素材。该目录是项目文件，不是参考模板，不加入 skill 模板中心。

- 当前预览：[方案四官网](http://localhost:3000/versions/%E6%96%B9%E6%A1%88%E5%9B%9B/)。
- 在项目根目录执行 `node scripts/serve.mjs` 启动 3000 端口服务；根路径仍保留原默认跳转，方案四使用上述地址。
- 内容装配工具为 `versions/方案四/scripts/build.py`，直接读取本地 `_source/` 快照；执行 `python3 versions/方案四/scripts/build.py` 可重建，无需 skill 目录。
- 详细说明与验证记录位于 `versions/方案四/README.md`、`versions/方案四/qa/verification.md`。
