# Influx AI 官网预览

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
- `references/veo-public/`：Veo 公开参考快照。
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

## 网站复刻 Skill

项目级技能位于 [`.agents/skills/website-replica/SKILL.md`](.agents/skills/website-replica/SKILL.md)，仅保存在本项目中。之后可在本项目的聊天中调用：

```text
使用 $website-replica 复刻 https://example.com/ 的前端视觉和动效，请先让我确认复刻范围。
```

技能会先确认页面范围，优先保留原站公开前端与素材，在独立目录中完成本地化、视觉与动效对照、本地预览及学习文档。不能完整获取时先说明具体缺口并求证，不默认改成近似实现或发布上线。附带的 Python 工具无需第三方依赖；静态下载和文件审计不能代替浏览器视觉验收。

该目录使用 [Codex 官方文档的项目级 skill 位置](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills)。如技能列表尚未出现，可直接提供上述 `SKILL.md` 路径要求使用，或重新打开 Codex。


## Reels 方向 · 方案三首页（2026-10-23）

按本轮确认范围新增独立方案三，仅重做首页；方案二和默认入口保留。

- 预览：<http://127.0.0.1:4174/versions/%E6%96%B9%E6%A1%88%E4%B8%89/>。
- 双击 `versions/方案三/启动方案三预览.command` 或使用根目录原有预览服务。
- 延续品牌紫蓝渐变，采用 Reels 参考的大字号、错落视频、滚动叠卡、逐词显现和合作流程。
- 人物与视频按用户授权暂用 Reels 参考素材，仅供本地视觉评审。中英文、截图放大、咨询弹窗、联系表单与法律提示保留。
- 定价与工具入口仍使用方案二；本轮没有发布或接入后端。
- 设计说明、素材映射及验证记录：`versions/方案三/README.md`、`versions/方案三/ASSET_SOURCES.json`、`versions/方案三/qa/`。
