"""Build the self-contained Pages artifact from the public Luma attendance label."""
from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.request import Request, urlopen

EVENT = "https://luma.com/8al1pfmi"


class GoingLabel(HTMLParser):
    def __init__(self):
        super().__init__()
        self.counts = set()

    def handle_data(self, data):
        match = re.fullmatch(r"([0-9]+(?:,[0-9]{3})*)\s+Going", data.strip())
        if match:
            self.counts.add(int(match[1].replace(",", "")))


def build():
    page = Path("index.html").read_text()
    marker = '<span class="count" data-luma-going>'
    if marker in page:
        request = Request(EVENT, headers={"User-Agent": "Mozilla/5.0 (compatible; MonospaceKiosk/1.0)", "Accept-Language": "en-US,en;q=0.9"})
        with urlopen(request, timeout=25) as response:
            if response.geturl().rstrip("/") != EVENT:
                raise ValueError("Unexpected Luma redirect")
            labels = GoingLabel()
            labels.feed(response.read().decode("utf-8"))
            labels.close()
        if len(labels.counts) != 1:
            raise ValueError("Missing or inconsistent public Going label")
        count = labels.counts.pop()
        page, matches = re.subn(re.escape(marker) + r"[0-9]+</span>",
                                f"{marker}{count}</span>", page)
        if matches != 1:
            raise ValueError("Expected one attendance counter")
        print(f"Public Luma attendance: {count} Going")
    output = Path("_site")
    output.mkdir(exist_ok=True)
    (output / "index.html").write_text(page)


if __name__ == "__main__":
    build()
