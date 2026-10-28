# Influx AI · 方案四

2026-10-26。使用 Reels 原始 Webflow 页面结构、CSS、GSAP 时间线和 Lenis，适配已定稿的 Influx Agency 官网内容。保留方案三 Logo、字体、紫蓝主色与顶部导航样式。

## 打开预览

项目服务运行时打开：

- [首页](http://localhost:3000/versions/%E6%96%B9%E6%A1%88%E5%9B%9B/)
- [工具与价格](http://localhost:3000/versions/%E6%96%B9%E6%A1%88%E5%9B%9B/pricing.html)
- [免费计算器](http://localhost:3000/versions/%E6%96%B9%E6%A1%88%E5%9B%9B/free-tools.html)

也可从[模板中心](http://127.0.0.1:4176/)点击“Influx AI · 方案四”的真实截图封面。模板中心为此目录启动独立服务器，支持视频 Range 请求。

需要重启项目预览时，在项目根目录运行 `node scripts/serve.mjs`；当前环境 Node 不在 PATH 时，可使用 `/Users/gztd-03-02687/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node scripts/serve.mjs`。项目根入口仍保留原设置，方案四使用上述独立地址。

需要重启模板中心时，运行 `python3 /Users/gztd-03-02687/.agents/skills/website-replica/scripts/library.py --port 4176`。服务终端按 Control+C 停止；停止中心也会停止它启动的独立模板预览。项目 3000 服务与中心是两个独立服务。

## 页面与适配

首页：首屏 → 四项营销服务与定制报价 → 愿景及全球资源 → 四项产品能力轮播 → 四步合作流程 → 统一联系表单 → 页脚。

- 直接保留 Reels 错落视频、创作者胶囊跑马灯、服务叠卡及横移缩放、资源影像构图、Webflow Slider、四步流程、按钮文字和箭头动效。
- 四大能力改用原模板案例轮播呈现，内容全部替换为 Influx 真实产品截图及已确认说明；不带入模板客户、案例成绩或评价。
- 工具页保留 Reels 的三列定价构图：Free、Plus、Pro / Enterprise。两个尚未开放方案合并展示，名称和状态分别保留；没有增加年付或服务月费。
- 原计费周期开关不适用，已移除并释放对应留白。营销服务定制报价提示放在工具套餐之前，计算器入口放在底部及页脚。
- 联系区采用原模板 Contact 页构图。所有来源共用姓名、邮箱、选填公司、咨询内容四字段；Free / Plus 可带来源并预填可编辑说明。
- 计算器使用相同的 Contact 原生布局及字段样式，计算结果在屏外时自动滚动到结果。
- 中英文切换保留语言偏好，并刷新页面让原 Webflow 时间线只对翻译后的节点初始化一次；未提交的咨询草稿在当前浏览器会话内保留。

## 文件与目录

- `index.html`、`pricing.html`、`free-tools.html`：直接运行的三个页面，不需要构建或安装依赖。
- `assets/`：模板原始素材、字体及原始运行时；`assets/influx/` 为方案三品牌资产、产品图与字体。
- `influx.css`：品牌字体/主色/导航，以及中文长度和子页的必要适配。
- `copy.js`：中英文内容；`influx.js`：语言、菜单、统一表单、截图、法律预览、计算器。
- `runtime-bridge.js`：字体加载后的刷新、首屏锚点定位、隐藏标签页视频暂停；原始动画仍由 Webflow / GSAP 执行。
- `scope.json`、`asset-manifest.json`：本次范围及资源来源；`_source/` 保存参与适配的原始 HTML 文本。
- `scripts/`：本次抽取和内容装配工具。网站本身不依赖这些脚本运行。
- [源码学习索引](STUDY_GUIDE.md)、[实际验证记录](qa/verification.md)。

实体位于技能模板库 `assets/templates/influx-ai-v4/`，项目的 `versions/方案四/` 是指向该实体的符号链接，遵循一份实体的模板管理约定。方案三未修改。

## 预览边界

仅本地预览，未发布、未接入业务提交、支付或账号开通。表单只保存到本浏览器，测试记录使用虚构信息。暂未提供真实登录地址，因此没有虚假的登录入口。

参考人物、视频及流程插画来自 Reels，只作视觉演示；图注标明参考素材或非实际项目数据。未将模板的客户、达人身份、效果数据或评价包装成 Influx 的真实成果。素材正式发布使用范围仍需落实。

原模板作者为 Webestica，原 Webflow 运行时与素材映射保留，页脚保留模板来源署名。
