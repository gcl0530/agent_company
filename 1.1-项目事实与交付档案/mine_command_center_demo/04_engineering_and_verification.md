# 总体方案与验证概览

> 本文件保留跨部门需要了解的总体技术方案、关键接口、版本和验证结论，并链接详细工程事实。详细设计、源码、配置、CI、测试脚本、原始日志和完整测试报告位于独立项目代码仓库。

## 总体方案与实现索引

- 代码仓库、分支、提交/版本：`/home/nvidia/mine-command-center`，`master`，`1ef7c25`（MVP 实现与依赖锁定基线）。
- 本次变更目标：完成智慧矿山数据监控大屏的截图还原 MVP，验证 Vue + ECharts + Three.js 技术链。
- 总体架构、模块与关键接口：`App.vue` 负责 1920x1080 布局和指标条；`HudPanel.vue` 负责 HUD 面板；`DashboardChart.vue` 按图表类型生成 ECharts 配置；`ZhejiangMap.vue` 将 GeoJSON 转成 Three.js 挤出几何并处理射线悬停；`dashboard.ts` 集中演示指标。无后端接口。
- 关键配置、数据、依赖与兼容性影响：Vue 3、TypeScript、Vite 7、ECharts 6.1、Three.js 0.182；GeoJSON 为公开浙江省 11 地市边界。所有业务数据均为合成数据。
- 失效处理、降级或回退结论：没有 API 时保持静态演示；WebGL 不可用时当前无降级视图，真实项目需补齐；回退可回到 Git 提交 `ed99dce`。
- 详细设计/代码/CI/测试入口：[`README.md`](/home/nvidia/mine-command-center/README.md)、[`src/components`](/home/nvidia/mine-command-center/src/components)、[`src/assets/geo/zhejiang.json`](/home/nvidia/mine-command-center/src/assets/geo/zhejiang.json)。当前未配置 CI。

## 关键验证结论

| 层级 | 验证范围 | 结论摘要 | 代码仓库中的证据位置 | 责任人 | 结论 |
| --- | --- | --- | --- | --- | --- |
| 模块 | Vue 类型检查 | `node node_modules/vue-tsc/bin/vue-tsc.js -b` 通过 | 代码仓库根目录 | Agent | 通过 |
| 集成 | 生产构建 | Vite 7 构建通过，618 个模块；主 JS 约 1.86 MB | 代码仓库 `dist/`（生成物未提交） | Agent | 通过，存在包体风险 |
| 回归 | Chromium 桌面浏览器 | 1920x1080：7 个 canvas 非空、无 console/page error；悬停命中湖州市并更新状态 | Playwright 检查 2026-07-24 | Agent | 通过 |
| 目标环境 | 窄屏等比缩放 | 390x844：16:9 画布缩放、无页面溢出、无浏览器错误 | Playwright 检查 2026-07-24 | Agent | 通过；非最终目标环境 |

## 缺陷与边界

| 编号 | 现象 | 影响 | 复现/证据 | 处理状态 | 进入交付的决定 |
| --- | --- | --- | --- | --- | --- |
| D-01 | 真实 Figma 资产与像素对齐未验证 | 视觉验收不完整 | 原稿未提供 | 开放 | 不进入客户交付 |
| D-02 | 真实数据、接口、身份与部署未实现 | 不能投入生产运行 | 本次范围定义 | 开放 | 不进入客户交付 |
| D-03 | WebGL 失败无静态地图降级 | 低能力终端可能无核心可视化 | 当前实现 | 开放 | 真实项目必须补齐或接受风险 |
