# 总体方案与验证概览

> 本文件保留跨部门需要了解的总体技术方案、关键接口、版本和验证结论，并链接详细工程事实。详细设计、源码、配置、CI、测试脚本、原始日志和完整测试报告位于独立项目代码仓库。

## 总体方案与实现索引

- 代码仓库、分支、提交/版本：`/home/nvidia/mine-command-center`，`master`，`a66fe15`（MVP 实现与依赖锁定基线）。
- 可复现命令（安装/构建/测试/启动）：标准命令见代码仓库 `README.md`：`npm install`、`npm run dev -- --host 0.0.0.0`、`npm run build`；本次类型检查执行 `node node_modules/vue-tsc/bin/vue-tsc.js -b`。
- 验证环境（系统、运行时、浏览器/硬件、关键配置）：WSL2 Ubuntu 22.04、Node.js 22.22.0、Chromium headless；视口 1920x1080 与 390x844；未在座舱、工控机或客户网络验证。
- 本次变更目标：完成智慧矿山数据监控大屏的截图还原 MVP，验证 Vue + ECharts + Three.js 技术链。
- 总体架构、模块与关键接口：`App.vue` 负责 1920x1080 布局和指标条；`HudPanel.vue` 负责 HUD 面板；`DashboardChart.vue` 按图表类型生成 ECharts 配置；`ZhejiangMap.vue` 将 GeoJSON 转成 Three.js 挤出几何并处理射线悬停；`dashboard.ts` 集中演示指标。无后端接口。
- 跨模块契约、评测资产与所有权位置：本样板只有前端代码仓库，未形成前后端或算法跨仓库契约；`S-01` 的内部契约为演示数据 -> ECharts/Three.js -> 浏览器画布，评测资产为公开 GeoJSON、合成指标与 Playwright 视口检查。真实项目必须使用跨模块契约模板补齐 owner、兼容性、失败语义和受控样本。
- 关键配置、数据、依赖与兼容性影响：Vue 3、TypeScript、Vite 7、ECharts 6.1、Three.js 0.182；GeoJSON 为公开浙江省 11 地市边界。所有业务数据均为合成数据。
- 失效处理、降级或回退结论：没有 API 时保持静态演示；WebGL 不可用时当前无降级视图，真实项目需补齐；回退可回到 Git 提交 `dce4d35`。
- 详细设计/代码/CI/测试入口：[`README.md`](/home/nvidia/mine-command-center/README.md)、[`src/components`](/home/nvidia/mine-command-center/src/components)、[`src/assets/geo/zhejiang.json`](/home/nvidia/mine-command-center/src/assets/geo/zhejiang.json)。当前未配置 CI。

## 关键验证结论

| 层级 | 验证范围/命令 | 验证环境 | 预期与实际结果 | 代码仓库中的证据位置 | 责任人 | 结论 |
| --- | --- | --- | --- | --- | --- | --- |
| 模块 | `node node_modules/vue-tsc/bin/vue-tsc.js -b` | WSL2 Ubuntu、Node.js 22.22.0 | 预期无类型错误；实际通过 | 代码仓库根目录 | Agent | 通过 |
| 集成 | Vite 7 生产构建 | WSL2 Ubuntu、Node.js 22.22.0 | 预期可产出静态构建；实际 618 个模块，主 JS 约 1.86 MB | 代码仓库 `dist/`（生成物未提交） | Agent | 通过，存在包体风险 |
| 回归 | Playwright 加载、截图、画布与悬停检查 | Chromium headless，1920x1080 | 预期地图和图表可见、无浏览器错误；实际 7 个 canvas 非空，悬停命中湖州市并更新状态 | Playwright 检查 2026-07-24 | Agent | 通过 |
| 目标环境 | Playwright 窄屏等比缩放检查 | Chromium headless，390x844 | 预期无滚动溢出；实际通过 | Playwright 检查 2026-07-24 | Agent | 通过；非最终目标环境 |

## 缺陷与边界

| 编号 | 现象 | 影响 | 复现/证据 | 处理状态 | 进入交付的决定 |
| --- | --- | --- | --- | --- | --- |
| D-01 | 真实 Figma 资产与像素对齐未验证 | 视觉验收不完整 | 原稿未提供 | 开放 | 不进入客户交付 |
| D-02 | 真实数据、接口、身份与部署未实现 | 不能投入生产运行 | 本次范围定义 | 开放 | 不进入客户交付 |
| D-03 | WebGL 失败无静态地图降级 | 低能力终端可能无核心可视化 | 当前实现 | 开放 | 真实项目必须补齐或接受风险 |
