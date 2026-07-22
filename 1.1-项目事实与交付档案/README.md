# 项目事实包

每个真实客户或业务项目在此建立一个目录，命名为 `1.1-项目事实与交付档案/<project_id>/`。项目事实包是业务、管理、验证与交付事实的唯一端到端入口；实际代码、配置和自动化测试仍位于相应代码仓库。

## 创建项目

复制 `_template/` 创建新目录，保留六份文件的编号和主职责。填写时只记录已知事实；未知项保留为待确认，不以模板文本替代实际结论。

```text
1.1-项目事实与交付档案/
  <project_id>/
    01_project_charter.md
    02_product_brief.md
    03_project_plan.md
    04_engineering_and_verification.md
    05_delivery_and_acceptance.md
    06_retrospective.md
```

项目结束后，项目包继续保留作为交付和复用证据；不移动到 `Temp/`。
