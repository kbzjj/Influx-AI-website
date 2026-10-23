# 静态前端本地化

用于公开 HTML 输出可以独立运行的页面。工具只做资源迁移，不承诺处理任意站点的动态运行时。

## 执行工具

在用户确认范围后，将已批准的**完整页面 URL 列表**传入工具。它不会遍历站内链接，也不会因为页面出现一个链接就扩大范围。

```sh
python3 <skill-dir>/scripts/snapshot.py \
  --url https://example.com/ \
  --url https://example.com/about \
  --output <skill-dir>/assets/templates/example-replica
```

第一个 URL 是本地首页；其他页面保存为有唯一标识的 `pages/*/index.html`。页面链接通过完整 URL 映射，查询参数不同的页面不会互相覆盖。资源名使用 URL 哈希与可读文件名，防止跨 CDN 同名文件覆盖。输出目录必须为空或不存在；失败时保留部分结果及错误清单，不能把重复运行当作覆盖修复手段。

仅下载被页面实际引用的常见资源以及 CSS 的 `url()` / `@import` 依赖。可用重复的 `--asset URL` 添加从原站浏览器中观察到的必要资源；额外字体 CSS 可能还需要手动接入页面。第三方 iframe 保留远程地址并列入报告，不自动下载其整个网站。

默认上限为 600 个资源、单文件 64 MiB、合计 256 MiB。这些是防止无意过量下载的操作上限，达到上限会报告未完成并以非零状态退出；不是用户同意的范围。确需扩大时，依据实际页面和媒体大小向用户说明后调整 `--max-assets`、`--max-file-mb`、`--max-total-mb`。

工具产物包括：

- 页面、`assets/` 和普通表单的本地演示适配脚本。
- `asset-manifest.json`：来源、最终重定向地址、本地路径、大小、文件哈希、失败项和需运行时复核项。
- `_source/`：重写前的 HTML / CSS 文本，仅供比对与学习，不参与预览。

工具退出 0 仅表示它识别的依赖成功保存。仍需审查运行时请求、字体和动画。

## 迁移时保留的语义

- `href="#"`、`href="#panel"`、空链接不改成页面路径；否则菜单按钮可能刷新整页。带资源 URL 的 SVG fragment，如 `sprite.svg#arrow`，重写文件路径后保留 `#arrow`。
- 分别处理导航、资源、`srcset`、背景图、视频封面和 `<source>`。资源可能没有扩展名；不要单凭后缀决定是否下载。
- 以资源实际所在 URL 为基准解析相对路径。CSS 的相对字体路径相对于 CSS 文件，不是页面。页面重定向、`<base>` 和查询参数均会影响解析。
- 不用对整个 HTML 的 URL 正则替换去改脚本内容；JSON-LD、脚本配置、原点检查和 API URL 需要各自理解。保存原始快照便于比较。
- CSS 被改写后，引用它的原始 `integrity` 会失效；仅移除/更新对应校验。字节未改变的第三方 JS 保留 SRI。浏览器报告 CSP 失败时，根据本地实际资源修正页面自身策略，不修改用户浏览器安全设置。
- 原始 CSS / JS 里的节点 ID、页面 ID、class 和脚本加载顺序可能是动画的目标映射，不能随意格式转换或删掉。
- 凡是修改源码后重建 snapshot，都应使用新目录或经审查的增量脚本；不要覆盖已修复的页面。

## 动态资源与外部行为

浏览器 Network 中确认实际字体、模块、媒体、Lottie / Spline / WebGL 资源。保留字体格式和字重，不用系统字体替代。Google WebFont 等可能运行时才加载 CSS；根据当前站点实际字体配置迁移，不能硬编码本次 Reels 的 Boldonse。

工具不会重写 JS 中的 `fetch`、ESM import、动态 import、webpack publicPath、Service Worker、`<picture>` 之外的自定义懒加载协议或签名媒体 URL。它会提示部分可识别情形，但不可能穷尽；仍需实际浏览器检查。已知缺口保留在清单并按主流程处理。

普通 HTML submit 由附带脚本拦截并给出本地反馈。自定义 SDK / 点击事件可能直接请求接口，必须检查原站行为并在本地适配其数据与反馈。搜索、筛选、分页等若属于用户确认的前端范围，可用已保存数据实现；不要将业务 API 接入或真实提交当作视觉复刻的一部分。

静态资源检查命令：

```sh
python3 <skill-dir>/scripts/audit.py --root <skill-dir>/assets/templates/example-replica
```

这会验证 manifest 中的文件、已识别的页面/CSS本地引用，列出外部依赖和需要预览服务器解释的本地路由。`missing` 为非空时以非零状态退出；`external` 和 `runtime_review` 必须进一步判断，不应一概删除。

修改工具后可运行隔离的本地 HTTP 回归用例，不访问真实参考站，也不改动现有页面：

```sh
PYTHONDONTWRITEBYTECODE=1 python3 <skill-dir>/scripts/test_snapshot.py
```

用例覆盖明确页面范围、菜单锚点、查询参数、同名资源、CSS 递归依赖、SVG fragment、数据 URL、重定向、`<base>`、SRI、缺失资源、大小限制、拒绝覆盖，以及命令行与审计产物。它们验证本地化工具的行为，不是对任意网站的视觉验收。
