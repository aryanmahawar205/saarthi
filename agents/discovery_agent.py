import json
import os
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import re

OUTPUT_FILE = "reports/discovered_attack_surface.json"
MAX_PAGES = 50

COMMON_PATHS = [
    "/sitemap.xml",
    "/robots.txt",
    "/v3/api-docs",
    "/openapi.json",
    "/swagger-ui.html",
    "/swagger.json",
    "/.env",
    "/.git/config",
    "/actuator",
    "/api-docs",
    "/v2/api-docs"
]

# Improved JS endpoint extraction pattern
JS_ENDPOINT_PATTERN = re.compile(r'["\']((?:/|https?://)[a-zA-Z0-9./_-]+(?:/api/|/v1/|/v2/)[a-zA-Z0-9./_-]+)["\']|["\'](/api/[^"\']+)["\']|["\'](/[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+)["\']')

def crawl(start_url, use_proxy=True):
    visited = set()
    queue = [start_url]
    endpoints = []

    parsed_start = urlparse(start_url)
    base_url = f"{parsed_start.scheme}://{parsed_start.netloc}"
    target_netloc = parsed_start.netloc

    proxies = {
        "http": "http://localhost:8081",
        "https": "http://localhost:8081",
    } if use_proxy else None

    # Add common paths to queue
    for path in COMMON_PATHS:
        full_url = urljoin(base_url, path)
        if full_url not in visited:
            queue.append(full_url)

    while queue and len(visited) < MAX_PAGES:
        current = queue.pop(0)

        if current in visited:
            continue

        visited.add(current)
        print(f"[DiscoveryAgent] Crawling: {current}")

        try:
            response = requests.get(
                current,
                timeout=10,
                verify=False,
                allow_redirects=True,
                proxies=proxies
            )

            endpoints.append({
                "url": current,
                "status": response.status_code,
                "method": "GET"
            })

            content_type = response.headers.get("Content-Type", "")

            # Extract from HTML
            if "text/html" in content_type:
                soup = BeautifulSoup(response.text, "html.parser")

                for tag in soup.find_all(["a", "form", "script"]):
                    href = tag.get("href") or tag.get("action") or tag.get("src")
                    if not href:
                        continue

                    absolute = urljoin(current, href)
                    parsed_absolute = urlparse(absolute)

                    if parsed_absolute.netloc == target_netloc:
                        if absolute not in visited:
                            queue.append(absolute)

            # Extract from JS
            elif "application/javascript" in content_type or "text/javascript" in content_type or current.endswith(".js"):
                matches = JS_ENDPOINT_PATTERN.findall(response.text)
                for match in matches:
                    for group in match:
                        if group:
                            if group.startswith("http"):
                                absolute = group
                            else:
                                absolute = urljoin(base_url, group)

                            parsed_absolute = urlparse(absolute)
                            if parsed_absolute.netloc == target_netloc:
                                if absolute not in visited:
                                    queue.append(absolute)

            # Extract from JSON (Swagger/OpenAPI)
            elif "application/json" in content_type:
                try:
                    data = response.json()
                    # Basic OpenAPI/Swagger path extraction
                    if "paths" in data:
                        for path in data["paths"].keys():
                            absolute = urljoin(base_url, path)
                            if absolute not in visited:
                                queue.append(absolute)
                except:
                    pass

        except Exception as e:
            print(f"[DiscoveryAgent] ERROR: {e}")
            continue

    return endpoints

def run(state):
    target = state.get("target_url")
    if not target:
        print("[DiscoveryAgent] No target_url provided in state.")
        return state

    print(f"[DiscoveryAgent] Starting discovery for {target}")

    # Determine if we should use proxy (it should be active)
    use_proxy = state.get("runtime_observer_active", False)

    endpoints = crawl(target, use_proxy=use_proxy)

    result = {
        "target": target,
        "endpoint_count": len(endpoints),
        "endpoints": endpoints
    }

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(result, f, indent=2)

    state["discovered_endpoints"] = endpoints
    print(f"[DiscoveryAgent] Discovered {len(endpoints)} endpoints")

    return state

if __name__ == "__main__":
    state = {"target_url": "http://localhost:8080/WebGoat/"}
    run(state)
