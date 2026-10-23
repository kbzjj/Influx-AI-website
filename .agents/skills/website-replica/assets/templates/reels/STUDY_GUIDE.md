# Reels 前端学习索引

## 建议阅读顺序

1. 运行本地预览，用浏览器开发者工具查看元素与计算样式。
2. 打开 `index.html`，按下面的 class 搜索区块。HTML 保留公开输出的紧凑格式，以避免新增空白改变内联布局。
3. 阅读 `assets/8541643a1d-reels-wbs.webflow.shared.c930502d8.css`。该文件有换行，可直接搜索 class、CSS 变量和媒体查询。
4. 阅读 `study/scroll-and-nav.js`，理解导航隐藏和 Lenis / GSAP 同步。
5. 再读首页交互入口 `assets/ebe1d0e61c-webflow.ae5bb349.bb882b5f4ad9a603.js` 中的 `register`、`triggers`、`timelineIds`、`scrub`。它是原站编译后的动画配置，适合配合 DevTools 格式化阅读。

## 布局与视觉

| 效果 / 区块 | 主要搜索入口 | 学习重点 |
| --- | --- | --- |
| 颜色、字号、间距 | CSS 中 `:root`、`--_typography` | 全站设计变量，标题与正文两套字体 |
| 顶部导航与中间凹口菜单 | `.nav-brand`、`.right-nav`、`.menu-button`、`.nav-menu` | 固定定位、装饰形状、层叠上下文 |
| 首屏标题 | `.hero-content`、`.hero-title-wrap`、`.hero-title-highlight` | 大字排版、强调色胶囊、断点换行 |
| 视频与创作者卡片 | `.hero-reels-item`、`.hero-creator-card` | 纵向视频裁切、渐变遮罩、旋转与滚动位移 |
| 平台 / 头像跑马灯 | `marquee`、`.hero-social-platform` | 超宽内容与遮罩，连续循环时间线 |
| 逐词文字区 | 第二个 `section` 内的标题节点 | ScrollTrigger 进度与文字透明度变化 |
| 服务卡片 | 搜索 `How we grow you` 及 `service` | 纵向空间、卡片叠放及随滚动变化 |
| 案例轮播 | `.w-slider`、`.w-slider-dot` | Webflow Slider 的 active 状态及切换 |
| 对比表 | `.compare-section`、`.compare-overlay` | 复杂嵌套布局、背景分层和遮罩 |
| 四步流程 | `.step-section` 及 `step` | 分步卡片、固定/滚动区间与动画时间线 |
| 数字与评价 | `counter`、`.testimonial-section` | 循环内容、纵横方向移动与视频 |
| 定价 | `.w-tabs`、`.w-tab-pane`、`data-w-tab` | Webflow Tabs；月付 / 年付两套内容 |
| CTA | `.cta-avatar-list`、`.cta-avatar-wrap`、`.footer-cta` | 头像分布、旋转与底部引导 |
| FAQ | `faqs/index.html` 中 `.faqs-item`、`.faqs-content` | 点击时间线、面板高度与图标旋转 |
| 按钮悬停 | `[button="hover"]`、`.button-arrow`、`.button-primary` | 双层文字、箭头位移和 hover 状态 |
| 响应式 | CSS 中的 `@media` | 原站平板、手机横屏及手机竖屏布局 |

## 动画运行关系

HTML 提供 DOM、class、`data-w-id`、`data-wf-page` 等标识；CSS 提供布局及基础状态。Webflow 分块脚本加载交互引擎，各页面的 `webflow.*.js` 再注册对应的事件和时间线。

GSAP 负责补间动画，ScrollTrigger 把滚动位置映射到动画进度，SplitText 用于文字拆分。Lenis 接管平滑滚动；`lenis.on('scroll', ScrollTrigger.update)` 和 `gsap.ticker` 将两者同步。

导航的滚动隐藏是额外的原站内联代码：桌面宽度大于 768px 时，下滚且超过 100px 将左右导航上移 80px 并淡出；上滚时恢复。菜单本体的开关和背景效果由 Webflow 时间线控制。

学习或修改时请同时保留页面底部脚本的加载顺序及节点标识。仅复制 CSS 会丢失菜单、文字和卡片动画；只更改 class 而不更新时间线目标，也可能让动画失效。

## 从小改动开始

建议先复制一个页面，再修改 CSS 颜色变量或单个按钮的圆角，观察它如何影响各个状态。随后尝试在 `study/scroll-and-nav.js` 的学习副本中改变 `lerp`、`duration`、`y` 的值，并把选定参数应用回页面对应的原始内联脚本。学习副本本身不参与运行。

资源文件名前的十位短哈希用于防止不同 CDN 目录的同名文件互相覆盖。可通过 `asset-manifest.json` 查到每个文件的原始地址。
