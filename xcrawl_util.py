# xcrawl 封装 - 备用方案
# 免费额度：1000次/月
# 触发条件：其他方案（web_fetch / CDP）都无法使用时的最后手段

import xcrawl, ssl, time
from secrets import XCRAL_API_KEY  # 敏感信息隔离

# ============ 配置 =============
API_KEY = XCRAL_API_KEY
TIMEOUT = 60


def get_client():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return xcrawl.XcrawlClient(api_key=API_KEY, timeout=TIMEOUT)


# ============ 单页面抓取（主力方法） ============
def scrape_pages(urls, render=True, formats=None):
    """
    抓取页面内容

    :param urls: URL列表
    :param render: 是否JS渲染（默认True）
    :param formats: 输出格式列表，默认 ['markdown']
                      可选: html, raw_html, markdown, links, summary, screenshot, json
    :return: [{'url': str, 'content': str, 'metadata': dict}, ...]
    """
    if formats is None:
        formats = ["markdown"]

    client = get_client()
    results = []
    try:
        for url in urls:
            options = {
                "js_render": {"enabled": render},
                "output": {"formats": formats},
                "request": {"only_main_content": True}
            }
            resp = client.scrape(url, options)
            data = resp.get("data", {})
            results.append({
                "url": url,
                "content": data.get("markdown", "") or data.get("html", "") or data.get("raw_html", ""),
                "metadata": data.get("metadata", {}),
                "credits_used": data.get("credits_used", 0)
            })
    finally:
        client.close()
    return results


# ============ 整站爬取 ============
def crawl_site(entry_url, max_depth=2, max_pages=50):
    """
    整站爬取
    """
    client = get_client()
    try:
        options = {
            "max_depth": max_depth,
            "max_pages": max_pages
        }
        job = client.crawl(entry_url, options)
        for _ in range(60):
            status = client.get_crawl_status(job.job_id)
            if status.status == "completed":
                return client.get_job_result(job.job_id)
            elif status.status == "failed":
                return {"error": f"Crawl failed: {status.error}"}
            time.sleep(5)
        return {"error": "Crawl timeout"}
    finally:
        client.close()


# ============ 搜索 ============
def search_google(queries):
    """
    搜索 Google SERP
    :param queries: 关键词列表
    """
    client = get_client()
    try:
        options = {
            "queries": queries,
            "search_engine": "google"
        }
        resp = client.search(options)
        return resp.data if hasattr(resp, "data") else resp
    finally:
        client.close()


# ============ 快速测试 ============
if __name__ == "__main__":
    print("[xcrawl] 备用爬虫测试")
    test_url = "https://example.com"
    print(f"抓取: {test_url}")
    result = scrape_pages([test_url])
    for item in result:
        print(f"URL: {item['url']}")
        print(f"内容长度: {len(item['content'])} 字符")
        print(f"消耗配额: {item['credits_used']}")
        print(f"内容预览: {item['content'][:150]}")
    print("测试完成")
