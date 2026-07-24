# 工具链与 Agent 平台

## 作用

本系统让 Agent 和自动化工具可被授权、复用和审查。它只提供执行能力，不拥有客户承诺、发布、验收或风险接受权。

## MVP 范围

本系统不把工具链当作独立产品，而是作为各部门的内部服务团队。产品、项目、研发、交付或组织系统提出重复性摩擦和结果目标；工具链把它实现为可审查的脚本、检查器、集成或 Agent 工作单元，并用实际结果决定保留、修改或下线。

每个被复用的 Agent 工作单元应有名称、适用场景、输入、输出、工具权限、质量门、人工升级人和知识回写位置。先登记真实项目中验证有效的工作单元，再扩展平台能力。

## 质量门

- 工具和 Agent 的输入范围、可写位置及可执行动作明确。
- 输出可关联到项目事实、代码或验证证据。
- 成本、失败模式、敏感数据和人工审批要求可见。
- 没有实际收益证据的调研或工具不升级为公司标准。

## 当前服务入口

- [服务目录](service_catalog.md)：部门可以请求什么、服务的输入输出和边界。
- [工具服务请求模板](tool_service_request_template.md)：提出自动化需求时的最小合同。
- [Agent 工作单元模板](agent_work_unit_template.md)：注册可复用 Agent 的职责与权限。
- [Agent 成熟度与权限晋级](agent_maturity_and_promotion.md)：用证据决定 Agent 可承担的动作级别。
- `scripts/create_project_package.sh <project_id>`：创建项目事实包。
- `scripts/check_project_package.sh <project_id-or-path>`：检查项目事实包的必需文件。
- `scripts/check_project_evidence.sh <project_id-or-path>`：检查具体项目是否已登记代码基线、版本、需求/里程碑和工作单元证据；不判断结论是否真实或批准项目。
- `scripts/check_markdown_links.js [path]`：检查 Markdown 本地链接。

所有脚本只处理本地仓库文件；部署、客户外部沟通和生产动作仍由项目负责人按权限执行。
