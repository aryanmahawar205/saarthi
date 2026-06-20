import json
import requests
from bs4 import BeautifulSoup


OUTPUT_FILE = "reports/recon.json"


def extract_forms(soup):

    forms = []

    for form in soup.find_all("form"):

        forms.append({

            "action":
                form.get("action"),

            "method":
                form.get(
                    "method",
                    "GET"
                )
        })

    return forms


def extract_links(soup):

    links = []

    for link in soup.find_all("a"):

        href = link.get("href")

        if href:

            links.append(href)

    return links


def run(state):

    target_url = state.get(
        "target_url"
    )

    if not target_url:

        raise ValueError(
            "target_url missing"
        )

    print(
        f"[ReconAgent] {target_url}"
    )

    result = {

        "target":
            target_url,

        "headers": {},

        "cookies": [],

        "forms": [],

        "links": [],

        "technologies": []
    }

    try:

        response = requests.get(
            target_url,
            timeout=10,
            verify=False
        )

        result["headers"] = dict(
            response.headers
        )

        result["cookies"] = list(
            response.cookies.keys()
        )

        server = response.headers.get(
            "Server"
        )

        if server:

            result[
                "technologies"
            ].append(server)

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        result["forms"] = \
            extract_forms(soup)

        result["links"] = \
            extract_links(soup)

    except Exception as e:

        print(
            f"[ReconAgent] Error: {e}"
        )

    with open(
        OUTPUT_FILE,
        "w"
    ) as f:

        json.dump(
            result,
            f,
            indent=2
        )

    state["recon"] = result

    print(
        "[ReconAgent] Complete"
    )

    return state