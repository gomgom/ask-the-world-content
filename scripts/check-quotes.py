r"""외부 AI 사실 검토 결과의 증빙 구절이 실제 페이지에 있는지 기계로 확인한다.

판단은 하지 않는다 — "이 구절이 이 주소의 본문에 글자 그대로 있나"만 본다.
요청문은 docs/외부-사실검토-요청문.md, 결과 JSON 은 그 요청문이 정한 형식(url·quote 필드)을 따른다.

    python -I scripts/check-quotes.py <결과.json 또는 D:\dev\eval-review 폴더>

- OK      글자 그대로 있음 (공백·따옴표 모양 차이는 무시)
- 근사    괄호 속 한자·각주 표시(주2 등)·문장부호를 빼면 있음 — 대개 맞지만 한 번 눈으로 본다
- MISS    없음 — 지적을 받아들이지 말고 사람이 본다
- 브라우저 페이지를 못 받음(브리태니커는 자동 요청을 403 으로 막는다) — 브라우저로 열어 확인한다
"""

import glob
import html
import json
import os
import re
import sys
import urllib.request


def text_of(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    raw = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")
    raw = re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.S)
    return html.unescape(re.sub(r"<[^>]+>", " ", raw))


def tight(s):
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", "", s).lower()


def loose(s):
    s = re.sub(r"\([^)]*\)|（[^）]*）|주\d+", "", s)
    return re.sub(r"[\W_]+", "", s).lower()


def load(path):
    """결과 파일 하나 또는 폴더(*-factcheck.json 전부). 배열이든 {figure, findings} 객체든 받는다."""
    files = sorted(glob.glob(os.path.join(path, "*-factcheck.json"))) if os.path.isdir(path) else [path]
    items = []
    for f in files:
        data = json.load(open(f, encoding="utf-8-sig"))
        fig = data.get("figure", "") if isinstance(data, dict) else ""
        fig = fig or os.path.basename(f).replace("-factcheck.json", "")
        for it in data.get("findings", []) if isinstance(data, dict) else data:
            items.append(dict(it, file=f"{fig}/{it.get('file', '')}"))
    return items


FIGURES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "figures")


def local_problem(it):
    """지적한 파일·문장이 우리 저장소에 실제로 있는가 — 외부 AI 가 이름을 지어내는지 본다."""
    path = os.path.join(FIGURES, *it["file"].split("/"))
    if not os.path.isfile(path):
        return "파일없음"
    sentence = (it.get("sentence") or "").strip()
    body = tight(open(path, encoding="utf-8").read())
    if sentence and tight(sentence) not in body and loose(sentence) not in loose(body):
        return "문장없음"
    return ""


def main(path):
    sys.stdout.reconfigure(encoding="utf-8")
    items = load(path)
    pages, counts = {}, {}
    for i, it in enumerate(items, 1):
        bad = local_problem(it)
        if bad:
            counts[bad] = counts.get(bad, 0) + 1
            print(f"{bad:6} #{i} {it['file']} | {(it.get('sentence') or '')[:60]}")
        url, quote = (it.get("url") or "").strip(), (it.get("quote") or "").strip()
        if not url or not quote:
            mark = "증빙없음"
        else:
            if url not in pages:
                try:
                    pages[url] = text_of(url)
                except Exception as e:  # 403·522 등
                    pages[url] = None
                    print(f"  (못 받음 {url}: {e})")
            page = pages[url]
            if page is None:
                mark = "브라우저"
            elif tight(quote) in tight(page):
                mark = "OK"
            elif loose(quote) and loose(quote) in loose(page):
                mark = "근사"
            else:
                mark = "MISS"
        counts[mark] = counts.get(mark, 0) + 1
        print(f"{mark:6} #{i} {it.get('file', '')} | {quote[:60]}")
    print("합계:", ", ".join(f"{k} {v}" for k, v in sorted(counts.items())))


if __name__ == "__main__":
    main(sys.argv[1])
