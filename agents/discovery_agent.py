import json
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup


OUTPUT_FILE = (
    "reports/discovered_attack_surface.json"
)

MAX_PAGES = 50


def crawl(start_url):

    visited = set()

    queue = [start_url]

    endpoints = []

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

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            endpoints.append({
                "url": current,
                "status": response.status_code
            })

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