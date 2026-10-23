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
