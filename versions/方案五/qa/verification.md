# 方案五实际验证记录

日期：2026-10-27。范围为中文桌面端三页，业务项目强参考 Shinta。最终入口为 `http://127.0.0.1:3005/`。

## 文件与运行

| 项目 | 实际结果 | 证据 |
| --- | --- | --- |
| 三页入口 | 首页、工具价格、计算器均 HTTP 200 | `runtime-checks.json` |
| 静态资源 | 审计缺失 0、哈希不一致 0、外部静态资源 0 | `static-audit.json`、`asset-manifest.json` |
| ESM 依赖 | 相对模块依赖无缺失 | `runtime-checks.json` |
| MP4 | HTTP Range 返回 206，64 字节与文件一致；实际视频 readyState 为 4 | `runtime-checks.json`、浏览器观察 |
| CMS 分段 | 两段范围响应与源文件拼接字节相同 | `runtime-checks.json` |
| 模板未改动 | 原 Shinta 481 个文件与开始前哈希完全相同 | `template-integrity.json` |
| 项目归属 | 输出为实体目录，无软链接，无业务模板登记文件 | `template-integrity.json`、`scope.json` |
| 最终浏览器状态 | 新计算器页面和修复后的首页未记录脚本错误 | 本次浏览器日志检查 |

初次实现时发现 Framer badge 对空节点执行水合产生 React 418/423，已移除业务页面不需要的 badge 水合。原模板编辑器入口也已从业务外层移除。早期日志仍可能保存在旧标签页历史中，最终检查按修复后状态记录。

## 视觉与动效

首轮原模板及业务首页使用实际 1280 × 720 视口检查。过程中用户预览面板宽度发生变化，后续使用固定 1280 × 900 的本地 iframe 检查桌面构图，截图缩放为 58%；这不是触屏或移动端验收。

| 状态 | 观察结果 | 截图 |
| --- | --- | --- |
| 首屏对照 | 保留原三列、中心堆叠视频、波浪路径、配色和留白；替换 Logo、中文标题、业务说明和资源数字 | `reference-hero.png`、`local-hero.png`、`local-hero-desktop.png` |
| 首屏播放 | 点击后 paused=false，时间从 0.2176 增长到 2.7942；再次点击 paused=true | `local-video-playing.png` |
| 滚动转场 | 实际向下滚动观察背景变化、问题卡移动与标题逐词显现 | `local-scroll-transition.png` |
| 全球资源 | 原视频和影像已加载，当前视口无缺失图片；数字与授权口径保留 | `local-resources.png` |
| 服务叠卡 | 从首卡向下滚动可见第 3/4 卡叠放，反向滚动回到第 2 卡；无卡死 | `local-services-desktop.png`、`local-services-forward.png`、`local-services-reverse.png` |
| 产品截图 | 实际打开 AI 搜索完整截图弹窗，图片 naturalWidth=2880，可关闭 | `local-product-lightbox.png` |
| 合作流程 | 四张原色卡、原图标和品牌/团队分工已显示 | `local-process-desktop.png` |
| 联系与页脚 | 统一四字段表单、原模板配色、页脚图形和品牌链接均显示 | `local-contact-desktop.png`、`local-footer-desktop.png` |
| 工具价格 | 实际查看三张原定价组件卡、开放状态、功能与订阅边界 | `local-pricing-desktop.png` |

文字与业务内容已改变，没有声称整页几何或所有像素与原站相同。视频随机帧、循环文字相位及截图时的进场状态不同。未逐帧验证每个滚动位置、拖拽视频换序或所有悬停帧。

## 完整业务操作

| 操作 | 结果 |
| --- | --- |
| Plus 咨询 | 跳到首页 `?plan=Plus#contact`，来源为 Plus，空正文预填“我想了解 Plus 方案。” |
| Free 意向 | 跳到首页 `?plan=Free#contact`，来源为 Free，空正文预填“我想了解 Free 体验。” |
| 表单规则 | 实际读取姓名、邮箱、咨询内容 required=true，公司 required=false |
| 本地提交 | 使用虚构姓名与 `scheme-five@example.com` 提交，显示“已保存在这个浏览器中，还没有发送给 Influx。”；未调用业务后台。测试草稿字段随后清空 |
| 正常计算 | 粉丝 10000、点赞 500、评论 50 → 5.50%，显示计算完成 |
| 非法输入 | 粉丝改为 0，rangeUnderflow=true，旧计算结果清除为“—%”；HTML 校验阻止继续计算 |
| 法律预览 | 实际打开隐私政策并读取预览说明，可用关闭按钮退出 |
| 导航 | 服务锚点、工具页、计算器、Free / Plus 返回首页均实际操作 |

提交证据为 `local-enquiry-saved.png`，计算证据为 `local-calculator-result.png`。表单代码使用当前浏览器存储，没有发送至 Influx、原模板或第三方业务服务的请求。

本轮未交付或验证英文、手机布局、真实账号、支付、业务消息接收或线上发布。参考模板的公开编译输出已本地保存，未提供 Framer 编辑器工程。
