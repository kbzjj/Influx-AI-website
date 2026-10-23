# Veo 源码与动效学习指南

## 从哪里开始

从模板中心打开 Veo，再用浏览器开发者工具检查元素。`index.html` 保留 Framer 原始 DOM、设计 token、响应式样式和 appear 配置；源页面的 HTML 文本副本位于 `_source/pages/`。运行时模块在 `runtime/7cbee4ec95/`，可用编辑器格式化功能辅助阅读压缩源码。

Framer 站点的 HTML 已包含初始渲染内容；模块随后进行 React 水合、接管路由和交互。因此“看起来有页面”不等于动效和导航已运行。运行时错误、字体或 CMS 失败应先修复，再比较视觉。

## 主要入口

| 文件 / 查找词 | 用途 |
| --- | --- |
| `script_main.B48J68fL.mjs` | 启动、水合、页面注册和路由。搜索 `Ur=`、`path:`、`getPageRoot`。 |
| `Q11MGpqmJ6ugQCWRGsEAqbvDnEynq6RrRVwo1jvGeLM.6T-aMWpi.mjs` | 首页主体和前后对比组件；搜索 `aria-valuenow`、`onMouseDown` 和实际标题文本。 |
| `TjBRiTgsqHghAQO1fXA9yCRo8Rxcgvfv4IXT6wA7Ink.W_Qwu5VI.mjs` | Features 页面。 |
| `3UMK4Vco4Q_Vpum2texNOR-t-L-qpFoAM6bbXQ0yBjg.I99KRxdl.mjs` | Gallery 页面。 |
| `VZiRAPpRFQINl_LKZVzpdGCHIinyQYDFxbDyeZ6JHQw.BGRE-8uE.mjs` | Pricing 页面。 |
| `tosFWBTUw_XZ0yQ5tW9W9bh2Jmkr7r0ziKLAZ0rXe_E.DDz7J5BK.mjs` | Contact 页面。 |
| `Jgv2V_ZwlsHBRvSePq6yPV_NElkVKPUQCSDT_TCzHwI.D12l0Gt8.mjs` | Blog 列表。 |
| `wJZDME00OLumXLGw7_82-i2iAcCxL54V8UeDiJVvnjE.CD6_VpVn.mjs` | 博客详情模板，文章内容由本地 CMS 提供。 |
| `XcGtWz86PivjyPmzJ4296TVShtVUTLNhQjuatBmuXac.BT5kPfNR.mjs` | 法律页面模板。 |
| `shared-lib.gu0pD8FM.mjs` 及其他组件模块 | 共享组件、导航、按钮、动态卡片等。结合页面 DOM 的 class、`data-framer-name` 定位。 |
| `motion.DbH-dO4v.mjs`、`framer.BW3ISXE6.mjs` | 原始动画和 Framer 运行时。通常先读组件配置，不直接修改库。 |

## 视觉与交互索引

- 首屏：搜索标题 `Create Stunning AI Art & Video`，查看渐变文字、背景云图、两侧漂浮卡片的变换和视频裁切。帧会随播放时间不同，应先比较容器布局。
- 图层定位：Framer 的 `data-framer-name` 比压缩 class 更易读；原有 class、ID 和页面标识是样式/水合的一部分，不要随意重命名。
- 滚动叠放与进场：HTML 的 `script[type="framer/appear"]` 和模块中的 transition / variants / scroll 配置共同决定初始状态、缓动、持续时间和滚动区间。
- 图像/视频画廊：找 `Generated Examples Gallery`、`Videos` / `Images` 的组件变体，点击后检查内容和 active 状态。
- 定价切换：`[data-framer-name="Yearly"]` 在不同组件中会复用，应结合文本和当前可见状态定位。年付切换为 $7 / $21 / $56，月付为 $10 / $30 / $80。
- FAQ：搜索问题文本及 `data-framer-name="Question"`，观察答案高度、透明度和展开/折叠状态。
- 前后对比：`[role="slider"]`，位置由 `aria-valuenow` 反映；组件的点击、鼠标和触摸事件更新裁切比例。
- 视频：原有 muted、autoplay、loop、playsinline 等保持；页面外的视频可能尚未预加载，应滚动到相应区域再检查。
- 表单：`local-preview.js` 在 capture 阶段拦截普通 submit，只显示本地反馈。

## 为什么模板独立使用一个本地根地址

Framer 的路由表使用 `/features`、`/gallery`、`/blog` 等原始路径。模板中心为每个模板分配独立的 loopback 服务，所以它们仍从根路径工作，模板也不会互相覆盖路由。

CMS 模块读取 `.framercms` 字节索引，向地址添加 `?range=...` 请求。普通文件服务器若忽略该参数并返回整个文件，界面可能初始正常，后续数据却无法正确读取。中心的服务器实现了这种分段响应，同时支持视频的 HTTP Range。

查找图片或字体来源时使用 `asset-manifest.json` 的 URL 映射；运行资源已本地化，`_source/` 中的原始 URL 用于追溯。不要将保留的外部购买/作者链接误当作本地业务能力。
