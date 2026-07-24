# Agent 工程实践调研与采用边界

## 目的

本记录只提炼可在定制软件公司中验证的工程做法，不把任何厂商文章、框架或“多 Agent”叙事直接视为公司能力。每项采用项都要经过项目试用、指标和人类 owner 审批。

## 公开来源与可采用结论

| 来源 | 可验证的原始观点 | 公司采用方式 | 不直接推出的结论 |
| --- | --- | --- | --- |
| [Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)（2024-12-19，访问于 2026-07-24） | 先选择最简单方案；确定任务优先工作流；Agent 在执行中从工具返回获得环境事实，并在检查点回到人类。 | 将“工作流优先、环境事实、停止条件、人工检查点”写入工作单元和运行记录。 | 不因模型能调用工具就扩大到客户承诺、发布或风险接受。 |
| [GitHub Docs: About code owners](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)（访问于 2026-07-24） | 关键路径可指定代码 owner，受保护分支可要求其批准后合并。 | 每个代码仓库按风险定义模块 owner 和合并门；Agent 改动仍进入人类评审。 | 不假设所有仓库、所有路径或所有变更需要同一审批强度。 |
| [OpenAI: A practical guide to building agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-agents/)（访问于 2026-07-24） | 将 Agent 系统视作可组合的工作流，并需治理、评估与人工控制。 | 以任务合同、评测资产、运行记录和权限晋级管理 Agent。 | 不把厂商指南当作本公司客户、安全或合规事实。 |

## 当前采用的最小机制

1. **工作流优先**：可预测、可重复任务优先使用确定性脚本或预定义步骤；只有无法预先确定步骤的开放问题才试用 Agent 循环。
2. **环境事实优先**：Agent 的推进依据代码、测试、工具输出、受控数据和人工确认，而不是自我声称完成。
3. **交付切片优先**：用可验证的端到端结果组织前端、后端、算法和集成，不按职能孤立完成度放行。
4. **契约与评测资产**：跨模块变更必须有 owner、兼容性、失败语义和可版本化的正常/边界/失败样本。
5. **运行可审计**：对 M1 及以上复用工作单元记录输入、动作范围、工具事实、成本、复核和异常。
6. **人类合并与发布门**：高影响路径需要明确 owner 审查；任何 Agent 都不绕过对外承诺、合并、发布、验收与风险接受。

## 试用指标

采用新 Agent 机制前后，应至少比较：交付切片周期、接口返工次数、评测覆盖率、人工复核率、失败/回退次数、单次成本和客户/业务反馈。没有基线，不宣布提效。
