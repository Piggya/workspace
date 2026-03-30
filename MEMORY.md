# MEMORY.md - 长期记忆

## 小杨的基本信息

- **名字**：小杨
- **工作**：阜阳土著网络科技有限公司
- **部门**：新媒体部（副主管）+ 产品部兼职
- **见客身份**：产品经理（市场部谈价格，小杨聊需求和产品）

## 工作内容

1. **公众号排版审核**
   - 政务公众号
   - 来稿排版（不需要产出内容，只负责排版）

2. **写产品方案**
   - 根据公司已售过授权的低代码/SaaS平台进行功能组合
   - 面向客户撰写定制化方案

3. **见客户讲解方案**
   - 以产品经理身份参与需求对接
   - 聊完客户需求后回来出具方案

4. **部门管理**（新媒体部副手）
   - 安排部门同事工作

5. **方案采纳后的协调**
   - 协调设计部：产品平台搭建和设计
   - 协调本部门：内容填充
   - 协调客服部：小程序认证备案等客户沟通

6. **AI产品相关**
   - AI相关产品的测试和开拓
   - OpenClaw 测试一个多月，尚未投入生产环境

## 小杨的工作痛点（待挖掘）

- 写方案需要从零搭框架、想功能组合
- 见客户后整理需求出方案费时间
- 各部门协调沟通链条长
- 还没有找到AI真正嵌入工作的切入点

## 小红书运营策略（重要！）

- 小红书严查AI托管，直接公开发布有7天封号风险
- 发布策略：
  - AI生成内容 → 好友可见 或 自分可见
  - 公开发布 → 必须由小杨人工操作
  - 我只负责：生成内容 + 存草稿 + 标注建议
- 小红书操作：通过 Chrome CDP 控制浏览器（复用登录状态）

## 浏览器控制（重要！）

- Chrome 调试端口已开启：localhost:9222
- 通过 Playwright CDP 连接，复用已登录的 Chrome 会话
- 无需 xiaohongshu-mcp MCP 服务器
- 连接方式：ws://localhost:9222/devtools/browser/{id}（id 每次重启 Chrome 会变）
- 可控制 Chrome 操作任何已登录网站（微信、小红书等）

## X(Twitter) 内容读取技巧

- x.com 链接直接 web_fetch 会失败（JS 渲染，无内容）
- **解法：用 fxtwitter.com 代理**
  - 格式：https://fxtwitter.com/i/status/{推文ID}
  - 或 https://fxtwitter.com/原始链接
- 同类工具：vxtwitter.com（但 fxtwitter 更稳定）
- 推文ID：从 URL 中提取，如 https://x.com/user/status/123456 → ID是 123456

## 虾兵蟹将体系

- **蟹将（我）**：话事人，小杨的直接对接人
- **虾兵**：子智能体，未来会配备多个，共同辅助工作
- **入口**：webui、Telegram bot（MEMORY.md 和 TOOLS.md 两个 session 都能读，信息共享）

## InStreet AI 社区

- 网址：https://instreet.coze.site
- 账号：xiejiang
- API Key：sk_inst_b931fc80ef0757be6689c8246f665e78
- Agent ID：e72090e5-c352-4ed9-8352-3d2e0e49730c
- 状态：已注册并激活

## 已配置的模型

| 模型 | 用途 | 备注 |
|------|------|------|
| MiniMax-M2.7 | 主力模型 | 默认使用 |
| nvidia/nemotron-nano-12b-v2-vl:free | 视觉理解 | 分析图片（OpenRouter免费） |
| BAAI/bge-m3 (硅基流动) | 向量记忆 | 语义搜索 |

## 图片模型配置

| 功能 | 优先级 | 模型/工具 | 费用 |
|------|--------|-----------|------|
| **图片理解** | 1st | OpenRouter Nemotron 免费模型 | 免费 |
| **图片生成** | 1st | doubao-web-image skill | 免费（带水印） |
| **图片生成** | 2nd | 硅基流动 Qwen 模型 | 付费（有余额） |

## 🌐 代理配置（重要！）

**Clash Verge 代理端口：127.0.0.1:7897**

遇到地区封锁（403/402）的外部 API 调用时，设置环境变量走代理：
```python
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7897'
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7897'
```

**适用场景：** OpenRouter、Google API 等被地区封锁的服务

## OpenRouter API Keys

| 账号 | Key | 备注 |
|------|-----|------|
| 旧账号 | sk-or-v1-3df85... | 已弃用，余额耗尽 |
| 新账号 | sk-or-v1-895baf... | 当前使用，Nemotron可用 |

## 已安装 Skills

- xhs-note-writer（小红书写作流量黑客）
- self-improving-agent、summarize、skill-vetter
- agent-browser、gog、multi-search-engine、tavily
- ~~xiaohongshu-mcp~~（已删除，改用 Chrome CDP 控制浏览器）
- **tieba-claw**（百度贴吧抓虾吧，已配置 Token）
- **doubao-web-image**（豆包免费生图，已安装）
- wechat-mp-writer-skill-mxx、social-media-publish

---

## 🔬 跨 Session 测试

- **测试时间**：2026-03-25 19:47
- **测试内容**：蟹将 WebUI 在 MEMORY.md 里写了这条记录，如果 Telegram bot 能看到，说明 MEMORY.md 在两个 session 间是共享的
- **验证方式**：去 TG bot 问它"MEMORY.md 里有几条记录"

*记录于 2026-03-25 19:47*
