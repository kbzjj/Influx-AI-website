# 方案五源码学习索引

## 从哪里修改

先运行本目录预览，结合浏览器查看实际页面。`scripts/content.py` 管理中文业务文案、能力清单、联系表单、计算器与页脚片段；`scripts/build.py` 读取项目内 `_source/shinta/`，组合原始组件并生成三页。`influx.css`、`influx.js` 不会被重建覆盖。

原始编译模块保存在 `_source/shinta/runtime/c2348627c3/`，页面实际加载的是 `runtime/c2348627c3/`。两者分开保留，方便核对原组件与业务适配。压缩模块可用编辑器格式化阅读，通常无需修改 React、Framer 或 Motion 库。

## 运行入口

`runtime/c2348627c3/script_main.D3Et_y6-.mjs` 注册原始路由与共享外层，包含导航和页脚视差。方案五的三页均使用原首页的共享外层，根据 `body[data-page]` 选择业务内容。跨页导航由 `influx.js` 处理，避免原模板路由把访客带到原站栏目。

`runtime/c2348627c3/E7Gy02fTtRRJl6hMB7qcE2rxgwCUbKrxzEbR3iwtkZQ.B9xiGkhW.mjs` 包含首页及原定价、服务等组件。生成器选择和组合它们，保留原组件的 class、布局、动画参数和运行依赖。

## 区块与动效

| 区块 | 页面选择器 / 模块 | 本次调整与主要参数 |
| --- | --- | --- |
| 首屏 | `.framer-15cgbio` | 原三列构图、视频卡堆叠和播放控件。标题按中文分行，右上案例推广位换为 210M+。 |
| 波浪文字 | 首页模块搜索 `textPath`、`svgPath`、`wCNhpJhlJ` | 保留 SVG 路径与更新逻辑。页面传入 `speed:28`、`pathSize:30`、`direction:backward`。 |
| 视频卡堆叠 | 首页模块搜索 `depthSpacing`；播放器 `jM2srQejd.CZUn5pvg.mjs` | 页面参数为 `depthSpacing:40`、`xOffset:-80`、`tiltAngle:-6`、`swipeThreshold:150`；原视频、封面和 spring 保留。 |
| 营销问题转场 | `.framer-1d0bx8m`、`#pain-point` | 原滚动背景、浮动问题卡、逐词进场。将错误图标对应的文本适配为业务问题。 |
| 全球资源 | `.framer-r66ymc`、`.framer-dcnr8z`、`.framer-ad94ku` | 原影像、视频、手绘曲线与数据卡；数字替换为 210M+、120+，补充 4、3 与平台授权口径。 |
| 产品能力 | `.framer-f62vvo`、`.influx-cap-grid` | 原项目卡来自 `iAPt8OKTt.dv23ykkj.mjs`，保留 hover 变换。`CAPABILITIES` 控制四项标题、说明和图片。 |
| 服务叠卡 | `#services`、`.framer-1nyhg89` | 原 sticky 结构与四种配色、图像和折页标签；原效果数字位置改为服务关键词与标签。 |
| 项目报价 | `.framer-zrxo4b-container`、`u0cuUnpe6.Ciz4rbX0.mjs` | 复用原收尾行动组件，替换标题、说明和咨询入口。 |
| 合作流程 | `#process`、`.framer-thgd3i` | 原四色流程卡、图标与 stagger；文本明确品牌方和 Influx 分工。 |
| 联系表单 | `#contact`、`.contact-layout`、`.shinta-form` | 以原双栏表单视觉作最小扩展，四字段统一入口；本地反馈由 `influx.js` 控制。 |
| 工具价格 | `.influx-pricing-cards` | 首页原定价组件 `qr`，保留普通/深色卡和按钮组件。三种方案在生成器 `plans` 数组配置；移除不适用的年付切换。 |
| 计算器 | `#calculator-form`、`#engagement-result` | 同一表单视觉；公式、输入验证和旧结果清除在 `influx.js`。 |
| 页脚 | `.framer-hyu1hp`、`.influx-footer` | 保留原外层视差、粉色背景和紫色图形，内容换为 Influx 品牌与真实页面链接。 |

原始的动画引擎只初始化一次，没有再添加 GSAP 或第二套平滑滚动。涉及位置变动时，应实际检查向下、反向与锚点跳转后的状态。

## 字体与布局

`influx.css` 用 `InfluxDigits` 字体族指定本地 D-DIN 两个字重，并通过 `unicode-range` 仅接管数字及价格符号。其他英文沿用模板 Open Sauce One / Geist，中文由系统中文字体承载。

本轮按用户要求只交付桌面版。`build.py` 的 `desktop_only()` 将原模板断点限定为桌面分支，CSS 最小页面宽度为 1200px。以后制作响应式时应恢复原断点，再独立调整中文、三列套餐和业务表单，不能将当前横向滚动当作手机适配完成。

## 业务交互

`influx.js` 将原 Projects / About / Blog / Contact 入口分别映射到服务、资源、工具与价格、联系表单。Free / Plus 来源放在查询参数中；咨询内容已有文字时不会被覆盖。

姓名、邮箱和咨询内容必填，公司选填。草稿使用 `sessionStorage` 的 `influx-v5-draft`；提交记录使用 `localStorage` 的 `influx-v5-enquiries`，无业务请求。页面反馈只表示浏览器保存成功。完整截图与法律说明使用原生 `dialog`，支持关闭按钮与 Escape。

`serve.py` 支持 MP4 HTTP Range 与 `.framercms?range=...` 多段读取。`cms-assets.js` 保留原读取器解码后的素材映射，未改写 CMS 二进制。不要用不支持这些读取方式的服务替代后，直接认定视频和运行时等价。

`qa/desktop-preview.html` 只是固定 1280 × 900 iframe 的构图检查工具，显示时缩小到 58%；它不是交付网站实现。业务页面自身运行完整原组件，没有用 iframe 嵌入原站。
