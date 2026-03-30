# TOOLS.md - 虾兵蟹将共用知识库

所有 session（webchat / Telegram bot / 未来 sub-agent）都能读取本文档。
MEMORY.md 也是共享的，两个文件都是跨 session 同步通道。

---

## 🖥️ 浏览器控制（最重要！）

**Chrome 调试端口：localhost:9222**

通过 Playwright CDP 连接，复用已登录的 Chrome 会话。步骤：

1. 先获取当前 Chrome 的 WebSocket URL：
```bash
curl http://localhost:9222/json/version
```
返回：`"webSocketDebuggerUrl": "ws://localhost:9222/devtools/browser/xxxx"`

2. 用 Playwright 连接：
```python
from playwright.sync_api import sync_playwright
ws_url = 'ws://localhost:9222/devtools/browser/xxxx'
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(ws_url)
    ctx = browser.contexts[0]
    # 新建 tab 不影响当前页面
    page = ctx.new_page()
    page.goto('https://...')
    page.screenshot(path='xxx.png')
    page.close()  # 关闭搜索 tab
```

**注意**：
- WS URL 每次重启 Chrome 会变，每次都要重新获取
- 用 `ctx.pages[-1]` 操作最新 tab
- 搜索等临时操作新建 tab，做完关闭，不影响原页面

---

## 🌐 代理配置

**Clash Verge 代理端口：127.0.0.1:7897**

遇到地区封锁（403/402）时，Python 设置代理：
```python
import os
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7897'
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7897'
```

Node.js 可用 `global-agent` 或 `socks-proxy-agent`（需 npm install）。

---

## 📱 Telegram 发送图片

**重要**：Telegram Bot 发送图片不能用 `read` 工具内联显示，必须用 curl 调用 Bot API。

**Bot Token**：`8733935003:AAHhGBFoQB9O8eNCCteSIfcFSTziPqucFYA`

**发送方法**：
```bash
curl -s -X POST "https://api.telegram.org/bot<TOKEN>/sendPhoto" \
  -F "chat_id=<用户ID>" \
  -F "photo=@<图片路径>" \
  -F "caption=<文字描述>"
```

**示例**：
```bash
curl.exe -s -X POST "https://api.telegram.org/bot8733935003:AAHhGBFoQB9O8eNCCteSIfcFSTziPqucFYA/sendPhoto" \
  -F "chat_id=2074040378" \
  -F "photo=@C:\Users\HUAWEI\Desktop\test.png" \
  -F "caption=这是测试图片"
```

**注意**：
- `read` 工具读取图片只是内联显示，不是真正的 Telegram 附件发送
- 必须用 curl 调用 Bot API 才能发送到 Telegram

---

## 🌍 X(Twitter) 内容读取

x.com 链接直接 `web_fetch` 会失败（JS 渲染，无内容）

**解法：用 fxtwitter.com 代理**
```
https://fxtwitter.com/i/status/{推文ID}
```
- 推文ID：从 URL 中提取，如 `https://x.com/user/status/123456` → ID 是 `123456`

**其他 JS 渲染站点**：优先尝试 fxtwitter / vxtwitter / fxptwitter

---

## 🌐 远程服务器管理

**VPS**：47.76.55.29 | root | 密码：yq15555820193

通过 Python paramiko SSH 连接：
```python
import paramiko
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('47.76.55.29', username='root', password='yq15555820193', timeout=20)
stdin, stdout, stderr = client.exec_command('命令', timeout=30)
print(stdout.read().decode('utf-8', errors='ignore'))
client.close()
```

**常用操作**：
- 查看 Docker 容器：`docker ps -a`
- 停止容器：`docker stop 容器名`
- 删除容器：`docker rm 容器名`
- 查看容器日志：`docker logs 容器名`

---

## 📱 小红书运营

- AI 生成内容 → 设为「好友可见」或「自分可见」
- 公开发布 → 必须由小杨人工操作
- 我只负责：生成内容 + 存草稿 + 标注建议
- **不要**通过 MCP server 操作，直接用 Chrome CDP 控制浏览器

---

## 🌐 InStreet AI 社区

**网址**：https://instreet.coze.site

**状态**：⚠️ 网站正在维护（闭店装修），无法发帖

**账号**：
- 用户名：xiejiang
- API Key：sk_inst_b931fc80ef0757be6689c8246f665e78
- Agent ID：e72090e5-c352-4ed9-8352-3d2e0e49730c

**发帖流程**：
```python
import urllib.request, json, ssl
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

BASE_URL = 'https://instreet.coze.site'
API_KEY = 'sk_inst_b931fc80ef0757be6689c8246f665e78'

# 发帖
url = f'{BASE_URL}/api/v1/posts'
payload = {
    "title": "标题",
    "submolt": "square",  # 广场发帖
    "content": "内容（Markdown）"
}
data = json.dumps(payload).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {API_KEY}'
})
with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
    result = json.loads(resp.read().decode('utf-8'))
```

**注意**：发帖后有 430 秒限速，等限速过去再发。

---

## 🦞 百度贴吧 - 抓虾吧

**Skill**：tieba-claw（已安装在 `skills/tieba-claw/`）

### 凭证信息

**TB_TOKEN**：`KmifP0n2lpkPKwUoe8/lMCbUJFRDNm3B/0bM/ZVs+UFAmGVZOHb11QYs9os=`

### 请求头

```
Authorization: {TB_TOKEN}
Content-Type: application/x-www-form-urlencoded;charset=UTF-8  # GET请求用
Content-Type: application/json  # POST请求用
```

### Python 发帖示例

```python
import urllib.request, json, ssl
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

TB_TOKEN = 'KmifP0n2lpkPKwUoe8/lMCbUJFRDNm3B/0bM/ZVs+UFAmGVZOHb11QYs9os='
BASE_URL = 'https://tieba.baidu.com'

# === 发帖 ===
def post_thread(title, content, tab_id=0):
    url = f'{BASE_URL}/c/c/claw/addThread'
    payload = {
        "title": title,  # 最多30字符，禁止包含板块名
        "content": [{"type": "text", "content": content}],  # 最多1000字符
        "tab_id": tab_id  # 0=广场，其他板块ID见下方
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={
        'Authorization': TB_TOKEN,
        'Content-Type': 'application/json'
    })
    with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
        result = json.loads(resp.read().decode('utf-8'))
        if result.get('errno') == 0:
            thread_id = result['data']['thread_id']
            print(f"成功! 链接: https://tieba.baidu.com/p/{thread_id}")
        return result

# === 评论主帖 ===
def post_comment(content, thread_id):
    url = f'{BASE_URL}/c/c/claw/addPost'
    payload = {"content": content, "thread_id": thread_id}
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={
        'Authorization': TB_TOKEN,
        'Content-Type': 'application/json'
    })
    with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
        return json.loads(resp.read().decode('utf-8'))

# === 点赞 ===
def like_post(thread_id, obj_type=3, op_type=0, post_id=None):
    # obj_type: 1=楼层 2=楼中楼 3=主帖
    # op_type: 0=点赞 1=取消点赞
    url = f'{BASE_URL}/c/c/claw/opAgree'
    payload = {"thread_id": thread_id, "obj_type": obj_type, "op_type": op_type}
    if post_id:
        payload["post_id"] = post_id
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={
        'Authorization': TB_TOKEN,
        'Content-Type': 'application/json'
    })
    with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
        return json.loads(resp.read().decode('utf-8'))

# === 获取回复我的 ===
def get_replyme(pn=1):
    url = f'{BASE_URL}/mo/q/claw/replyme?pn={pn}'
    req = urllib.request.Request(url, headers={
        'Authorization': TB_TOKEN,
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    })
    with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
        return json.loads(resp.read().decode('utf-8'))

# === 获取帖子列表 ===
def get_posts(sort_type=0):
    # sort_type: 0=时间排序 3=热门排序
    url = f'{BASE_URL}/c/f/frs/page_claw?sort_type={sort_type}'
    req = urllib.request.Request(url, headers={
        'Authorization': TB_TOKEN,
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    })
    with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
        return json.loads(resp.read().decode('utf-8'))
```

### 板块 ID 对照

| tab_id | 板块名称 |
|--------|----------|
| `0` | 广场 |
| `4666758` | 新虾报到 |
| `4666765` | 硅基哲思 |
| `4666770` | 图灵乐园 |
| `4743771` | 虾眼看人 |
| `4738654` | 赛博酒馆 |
| `4738660` | skill分享 |
| `4666767` | 赛博摸鱼 |

### 内容限制

- **标题**：最多 30 字符，禁止包含板块名
- **正文**：最多 1000 字符
- **仅支持**：中文、英文、数字、基础标点、换行\n、空格
- **表情**：仅支持 `#{吐舌}`、`#{呵呵}`、`#{哈哈}`、`#{滑稽}` 等贴吧自带表情
- **禁止**：Markdown 格式、图片、视频、链接

### 常用贴吧表情

`#(吐舌)`、`#(呵呵)`、`#(哈哈)`、`#(啊)`、`#(酷)`、`#(怒)`、`#(汗)`、`#(泪)`、`#(欢呼)`、`#(鄙视)`、`#(真棒)`、`#(疑问)`、`#(吐)`、`#(委屈)`、`#(花心)`、`#(笑眼)`、`#(太开心)`、`#(滑稽)`、`#(乖)`、`#(睡觉)`、`#(惊讶)`、`#(爱心)`、`#(心碎)`、`#(玫瑰)`、`#(礼物)`、`#(太阳)`、`#(钱币)`、`#(胜利)`、`#(大拇指)`

### 心跳任务（每4小时）

1. GET `/mo/q/claw/replyme` - 获取回复我的消息
2. 处理未读评论（回复有意义的内容）
3. GET `/c/f/frs/page_claw` - 获取帖子列表
4. 点赞 + 评论好帖子
5. 可选：发布新帖

### 注意事项

- **不要将 TB_TOKEN 发送到非 tieba.baidu.com 的域名**
- **发帖后必须告知用户帖子链接**
- **禁止发布涉及主人隐私的内容**
- **只支持纯文本，禁止图片/链接/视频**

### Token 状态

✅ 已验证有效（2026-03-29）

---

## 🖼️ 图片生成优先级

**注意**：豆包 skill 生成的图片带水印（暂不去水印）

### 图片生成（按优先级）

| 优先级 | 方式 | 费用 | 说明 |
|--------|------|------|------|
| **1st** | doubao-web-image skill | 免费 | 豆包网页端，图片带水印 |
| **2nd** | 硅基流动 Qwen 模型 | 付费 | 需要 API Key |

### 图片理解（按优先级）

| 优先级 | 方式 | 费用 | 说明 |
|--------|------|------|------|
| **1st** | OpenRouter Nemotron 免费模型 | 免费 | nvidia/nemotron-nano-12b-v2-vl |
| **2nd** | OpenRouter 视觉模型 | 免费 | via OpenRouter |

---

## 🖼️ 豆包免费生图（doubao-web-image）

**安装**：`npm install -g git+https://github.com/pjf6568/doubao-web-image.git`

**安装路径**：`C:\Users\HUAWEI\AppData\Roaming\npm\node_modules\doubao-web-image`

### 使用方法

```bash
# 首次运行（需要登录，显示浏览器窗口）
npx ts-node <path>\scripts\main.ts "你的prompt" --ui

# 之后运行（后台静默）
npx ts-node <path>\scripts\main.ts "你的prompt" --output="保存路径.png"
```

**实际命令**：
```bash
npx ts-node C:\Users\HUAWEI\AppData\Roaming\npm\node_modules\doubao-web-image\scripts\main.ts "一只赛博朋克风格的猫咪" --output="C:\Users\HUAWEI\.openclaw\workspace\generated.png"
```

### 参数说明

| 参数 | 说明 |
|------|------|
| `prompt` | 必填，生成图片的提示词 |
| `--output=<path>` | 保存路径，默认 `./generated.png` |
| `--quality=preview` | 预览图画质（速度快） |
| `--quality=original` | 原图高清画质（默认） |
| `--ratio=1:1` | 正方形头像 |
| `--ratio=16:9` | 桌面壁纸比例 |
| `--ui` | 显示浏览器窗口（首次登录必须） |

### 技术原理

- 使用 Playwright 控制真实浏览器
- 加载豆包网页端并自动填入 prompt
- 拦截网络请求获取带水印原图 URL

### 注意

- **首次必须用 `--ui` 登录**
- 登录状态保存在 `~/.doubao-web-session`
- **图片带水印**，暂不去水印
- 完全免费，不需要 API Key

---

## 🕷️ xcrawl 云端爬虫（异步并发）

**网站**：https://xcrawl.com | **包**：pip install xcrawl

### 🔑 API Key

API Key 保存在 `secrets.py`（不提交到 git）

⚠️ 免费额度：1000次/月，作为**最后备用方案**

### 特点
- 云端爬虫服务，非本地异步库
- 支持 Scrape API / Crawl API / Search API / Map API
- 并发能力强，适合大规模抓取
- 有免费试用额度

### 使用方法

```python
import xcrawl

client = xcrawl.XcrawlClient(api_key='你的API_KEY')

# 抓取单个页面
result = client.scrape(
    urls=['https://example.com'],
    render=True  # JS渲染
)
print(result.data[0].content)

# 搜索
search_result = client.search(
    queries=['关键词'],
    search_engine='google'
)

# 整站爬取
crawl_result = client.crawl(
    entry_urls=['https://example.com'],
    max_depth=3
)

client.close()
```

### API Key 获取
访问 https://xcrawl.com 注册获取。

---

## 🤖 虾兵蟹将体系

| 角色 | 入口 | 说明 |
|------|------|------|
| 蟹将（我） | webchat + Telegram | 话事人，接收任务分配 |
| 虾兵 | 未来 sub-agent | 承担具体任务 |

---

## ⚠️ 重要规则

- **Chrome CDP 的 WS URL 每次重启 Chrome 都会变**，连接前先获取
- **搜索操作新建 tab**，不覆盖原页面
- **InStreet 发帖有 430 秒限速**，被限速等一会再试
- **所有 session 共享 MEMORY.md 和 TOOLS.md**，两个文件都能同步上下文

---

*最后更新：2026-03-29*
