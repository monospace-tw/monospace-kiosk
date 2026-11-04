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

    reception = page.replace(
        '<div class="stack"><span class="eyebrow">MEMBER ACCESS</span><strong>會員請刷卡</strong></div>',
        '<div class="stack reception-welcome"><span class="eyebrow">WELCOME TO MONOSPACE</span>'
        '<strong>歡迎來到 Monospace</strong><span class="reception-note">你的工作、交流與創作基地</span></div>',
    ).replace('VISITORS / LINE', 'START HERE / LINE').replace('訪客預約・諮詢', '來訪報到・空間諮詢')
    reception = reception.replace(
        '<strong>來訪報到・空間諮詢</strong>',
        '<strong>來訪報到・空間諮詢</strong>'
        '<span class="reception-contact-note">掃碼加入 LINE，開始聯繫</span>',
    )
    if reception == page or 'reception-welcome' not in reception:
        raise ValueError("Reception footer template changed")
    reception = reception.replace('</style>', """
.entry {grid-template-columns: 1.2fr 1fr}
.entry .visitor {gap:1.6vw;padding-left:2.5vw}
.entry .visitor strong {font-size:2.25vw;white-space:nowrap}
.reception-welcome strong {font-size:2.8vw}
.reception-note {font-size:1.65vw;color:#c5d6df}
.reception-contact-note {font-size:1.4vw;color:#c5d6df}
</style>""", 1)
    reception_dir = output / "boards" / "reception-1107"
    reception_dir.mkdir(parents=True, exist_ok=True)
    (reception_dir / "index.html").write_text(reception)


if __name__ == "__main__":
    build()
