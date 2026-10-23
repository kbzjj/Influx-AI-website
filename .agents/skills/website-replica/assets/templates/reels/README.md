# Reels 前端本地学习副本

参考站：https://reels-wbs.webflow.io/  
保存日期：2026-10-23

本目录保留参考站公开输出的 HTML、CSS、Webflow 运行时及 GSAP 动效配置，并将站内链接、图片、字体、视频和脚本改为本地路径。保留原始动画节点 ID 和页面 ID，以复现原站视觉与交互，而非重新近似绘制。

共 **22 个公开页面、245 个资源文件**，其中 **8 个 MP4 视频**及对应的 WebM / 封面。本目录独立于 `versions/方案二/`，没有替换 Influx AI 现有官网。

## 启动

双击本目录的 `启动Reels预览.command`，在浏览器打开：

<http://127.0.0.1:4175/>

或在项目根目录执行：

```sh
python3 -m http.server 4175 --bind 127.0.0.1 --directory references/reels-webflow
```

如果已经通过项目原有的 `启动预览.command` 启动 4174 端口，直接打开：

<http://127.0.0.1:4174/references/reels-webflow/>

无需 npm 安装或构建。请使用 HTTP 预览，保留终端窗口，结束时按 Control+C。

## 页面与文件

| 路径 | 内容 |
| --- | --- |
| `index.html` | 完整首页 |
| `about/index.html` | About |
| `case-studies/index.html` | 案例列表 |
| `case-study/*/index.html` | 4 个案例详情 |
| `blog/index.html` | 博客列表 |
| `blog/*/index.html` | 7 篇博客详情 |
| `faqs/index.html` | FAQ 折叠面板 |
| `contact/index.html` | 联系表单 |
| `privacy-policy/index.html` | 隐私页面 |
| `utility-pages/*/index.html` | Style Guide、Instructions、Licenses、Changelog |
| `assets/` | 本地样式、字体、图片、视频及脚本 |
| `asset-manifest.json` | 原始 URL → 本地文件映射与下载结果 |
| `local-study.js` | 本地表单演示适配 |
| `study/scroll-and-nav.js` | 导航和平滑滚动代码的可读摘录，不在页面重复执行 |
| `STUDY_GUIDE.md` | 视觉、布局和动画的源码学习索引 |
| `scripts/mirror.py` | 可复用的公开前端保存脚本，仅执行 GET 请求 |
| `qa/` | 资源检查结果、页面尺寸对照与截图 |

## 本地适配与范围

- 保留原站 Webflow 结构、设计变量、响应式断点、GSAP 时间线、ScrollTrigger 和 Lenis。
- Boldonse 与 Inter Display 字体本地化，避免依赖在线字体服务。
- 内页链接改为相对路径；菜单、页内锚点和 Tabs 的 `#` 链接保留。
- 原站的设计署名、模板推广卡片及 Licenses 页面保留。隐藏了 Webflow 仅在本地主机额外注入的徽标，使其与线上演示外观一致。
- 表单只显示明确的本地演示反馈，不发送给原站，也不保存输入数据。
- 博客中的 YouTube iframe 保留原始嵌入地址，需要联网。社交媒体、作者、Webflow 等外链也保留。
- 这是公开前端的本地快照；不包含 Webflow Designer 工程、CMS 管理后台或原站业务服务。

## 验证记录

- 22 页的 268 个去重本地引用检查通过，无缺失文件，HTTP 请求均返回 200。
- 1280 × 720 浏览器下，首页 11 个 section 的宽高，以及主标题宽高和字体与原站逐项一致。详见 `qa/geometry-comparison.json`。
- 已在浏览器验证菜单开关及背景模糊、首屏视频播放/暂停、案例轮播、月付/年付切换、FAQ 展开、本地表单反馈。
- 已检查 390px 手机首屏及 1280px 桌面布局。主要页面的浏览器控制台无脚本错误。
- 动画播放时刻、视频帧、设备字体渲染、浏览器滚动条可能影响截图；尺寸一致不代表所有设备、所有帧都完成逐像素验收。

重新抓取会更新本目录页面和资源，不要在手工修改页面后直接运行。源码更新命令：

```sh
python3 references/reels-webflow/scripts/mirror.py
```
