# 会话笔记: 2026-03-09

## 会话概览
- **日期**: 2026-03-09
- **主题**: AI Fluency - Agentic Workflow 与智能体
- **形式**: 概念对谈 + 平台实操体验（扣子/Coze）
- **知识域**: 4. 进阶实战：Agentic Workflow 与智能体 (15%)

## 问答记录与知识点掌握情况

### 探讨 1: 传统自动化 vs AI Agent
- **学生初始理解**: 有丰富的 Jenkins Pipeline、Ansible Playbook、cron 使用经验。
- **教学内容**:
  - 传统自动化 = 确定性控制流，所有分支都由人预先写死
  - AI Agent = LLM 实时决策，动态规划执行路径
  - 传统自动化遇到意外只能走 when/catch 预设逻辑，Agent 能分析原因自主调整策略
- **理解检查**: 学生正确回答了传统自动化"只能按预先写好的 when/catch 逻辑处理"，从自身经验出发准确把握了核心区别。
- **掌握的课题**: 传统自动化与 AI Agent 的本质区别。

---

### 探讨 2: Agent 核心工作循环与三大组件
- **学生初始理解**: 通过对比 Jenkins 场景建立理解。
- **教学内容**:
  - Agent 的"观察-思考-行动"循环（ReAct 模式）
  - 用 Nginx 502 排查场景演示了 Agent 的自主决策过程
  - Agent 三大组件：LLM（大脑）、Tools（工具/手脚）、Memory（记忆）
  - 用微服务架构类比：LLM = Orchestrator, Tools = Services, Memory = Database
- **理解检查**: 学生认同了 IDE AI 助手就是 Agent 的实例，理解了观察-思考-行动循环。
- **掌握的课题**: Agent 工作循环、三大核心组件及其作用。

---

### 探讨 3: Function Calling 与 Agent 风险
- **学生初始理解**: 理解 LLM 是"大脑"的角色。
- **教学内容**:
  - Function Calling：LLM 输出结构化 JSON → 编排框架执行 → 结果喂回 LLM
  - LLM 在 Function Calling 中仍然只是在"预测下一个 Token"
  - 两大风险：幻觉工具调用、危险操作
  - 铁律：高危操作必须 Human-in-the-Loop
- **引导深入理解**: 引导学生回忆底层认知中学到的"Token 预测"本质，将其与 Function Calling 联系。学生回答"做大脑"，经引导后理解本质仍是 Token 预测。
- **掌握的课题**: Function Calling 机制、Agent 风险与 Human-in-the-Loop 原则。

---

### 探讨 4: 实操体验 — 扣子(Coze)平台
- **实操内容**: 学生在 coze.cn 上体验了对话式 AI 交互。
  - 输入了 K8s CrashLoopBackOff 排查问题
  - 扣子返回了结构化的表格对比（原因、典型表现、排查命令）
- **教学重点 — 复盘分析**:
  - 引导学生分析扣子的回答是否展现了 Agent 特征
  - 对比"聊天机器人"（告诉你怎么查）vs "真正的 Agent"（替你去查）
  - 用 IDE AI 助手（自己读取文件、执行命令）作为"真正 Agent"的实例
- **理解检查**: 问学生"把 Bot 变成真正 Agent 还需要什么"，学生回答"记忆、工具"，准确命中核心。
- **掌握的课题**: 聊天机器人与 Agent 的本质区别、Agent 落地的关键要素。

---

## 今日学习总结
| 主题 | 核心收获 |
|------|----------|
| 传统自动化 vs Agent | 确定性控制流 vs LLM 实时决策 |
| Agent 工作循环 | 观察 → 思考 → 行动 → 反馈 → 循环 |
| Agent 三大组件 | LLM（大脑）+ Tools（手脚）+ Memory（记忆） |
| Function Calling | LLM 输出 JSON 调用指令，本质仍是 Token 预测 |
| Agent 风险 | 幻觉调用 + 危险操作 → Human-in-the-Loop |
| 实操复盘 | 聊天机器人 ≠ Agent，Agent 需要真正连接外部工具 |

## 已识别的知识盲区
- 暂无

## 已掌握的课题（附置信度）
- 传统自动化与 AI Agent 的核心区别（高）
- Agent 观察-思考-行动循环（高）
- Agent 三大组件及其作用（高）
- Function Calling 机制原理（高）
- Agent 风险与 Human-in-the-Loop（高）
- 聊天机器人与真正 Agent 的区别（高）

## 用户的实际工作痛点
- 有丰富的 K8s / Nginx 运维经验，Agent 能直接服务于运维排障场景
- 日常使用 Jenkins/Ansible 自动化，可与 Agent 对比理解

## 接下来的学习建议
- 可以深入学习：多 Agent 协作、ReAct 框架
- 或进入下一个知识域：日常交互与生产力提效、AI 治理与安全性
