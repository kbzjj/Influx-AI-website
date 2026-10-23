# Influx AI 官网预览

当前仅保留方案二，源码位于 `versions/方案二/`。方案一及其相同的 `preview/` 副本已于 2026-10-23 按用户要求删除。

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

- `versions/方案二/`：当前唯一的官网方案，包含页面、样式、交互及本地素材。
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
