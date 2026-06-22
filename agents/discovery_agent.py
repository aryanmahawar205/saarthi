import json
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import re


OUTPUT_FILE = (
    "reports/discovered_attack_surface.json"
)

MAX_PAGES = 50

COMMON_PATHS = [
    "/sitemap.xml",
    "/robots.txt",
    "/v3/api-docs",
    "/openapi.json",
    "/swagger-ui.html",
    "/swagger.json"
]

JS_ENDPOINT_PATTERN = re.compile(r'["\'](/api/[^"\']+)["\']|["\'](/[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+)["\']')


def crawl(start_url):

    visited = set()

    queue = [start_url]

    endpoints = []

    parsed_start = urlparse(start_url)
    base_url = f"{parsed_start.scheme}://{parsed_start.netloc}"

    for path in COMMON_PATHS:
        full_url = urljoin(base_url, path)
        if full_url not in visited:
            queue.append(full_url)

    while queue and len(visited) < MAX_PAGES:

        current = queue.pop(0)

        if current in visited:
            continue

        visited.add(current)

        try:

            response = requests.get(
                current,
                timeout=10,
                verify=False,
                allow_redirects=True
            )

            endpoints.append({
                "url": current,
                "status": response.status_code
            })

            content_type = response.headers.get("Content-Type", "")

            if "text/html" in content_type:
                soup = BeautifulSoup(
                    response.text,
                    "html.parser"
                )

                for link in soup.find_all("a"):

                    href = link.get(
                        "href"
                    )

                    if not href:
                        continue

                    absolute = urljoin(
                        current,
                        href
                    )

                    if "localhost:8080" in absolute:

                        if absolute not in visited:

                            queue.append(
                                absolute
                            )
                for script in soup.find_all("script"):
                    src = script.get("src")
                    if src:
                        absolute = urljoin(current, src)
                        if "localhost:8080" in absolute and absolute not in visited:
                            queue.append(absolute)

            elif "application/javascript" in content_type or "text/javascript" in content_type or current.endswith(".js"):
                # Extract endpoints from JS
                matches = JS_ENDPOINT_PATTERN.findall(response.text)
                for match in matches:
                    for group in match:
                        if group:
                            absolute = urljoin(base_url, group)
                            if "localhost:8080" in absolute and absolute not in visited:
                                queue.append(absolute)

        except Exception as e:

            print(
                f"[DiscoveryAgent] ERROR: {e}"
            )

            continue

    return endpoints


def run(state):

    target = state.get(
        "target_url"
    )

    print(
        f"[DiscoveryAgent] {target}"
    )

    endpoints = crawl(
        target
    )

    result = {

        "target":
            target,

        "endpoint_count":
            len(endpoints),

        "endpoints":
            endpoints
    }

    with open(
        OUTPUT_FILE,
        "w"
    ) as f:

        json.dump(
            result,
            f,
            indent=2
        )

    # IMPORTANT

    state[
        "discovered_endpoints"
    ] = endpoints

    print(
        f"[DiscoveryAgent] "
        f"{len(endpoints)} endpoints"
    )

    return state


if __name__ == "__main__":

    state = {

        "target_url":
            "http://localhost:8080/WebGoat/"
    }

    run(state)
