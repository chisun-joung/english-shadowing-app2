#!/usr/bin/env python3
"""유튜브 영상에서 '실제로 사용된 영어 문장'을 자막(caption)으로 인식해 추출·정제한다.

동작 방식
  - youtube-transcript-api 로 해당 영상의 영어 자막(수동 우선, 없으면 자동생성)을 가져온다.
    자막은 영상에서 실제 발화된 문장을 그대로 담고 있으므로, 별도 음성인식(STT) 없이
    "실제 사용된 영어 문장"을 그대로 확보할 수 있다.
  - [music], [laughter] 같은 대괄호 마커와 >> 화자 표시, 중복/공백을 제거한다.
  - 문장 부호(.!?) 기준으로 문장 단위로 쪼개어 후보 문장 목록을 만든다.

사용법
  python yt_transcript.py <youtube_url_or_id> [--lang en] [--out sentences.json]

출력(JSON)
  {video_id, lang, sentence_count, sentences:[{i, text}], full_text}
필요 패키지가 없으면 자동으로 설치를 시도한다.
"""
import sys, re, json, argparse, subprocess


def ensure_dep():
    try:
        import youtube_transcript_api  # noqa: F401
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "--quiet",
                        "youtube-transcript-api"], check=True)


def parse_video_id(s):
    s = s.strip()
    m = re.search(r"(?:v=|youtu\.be/|/shorts/|/embed/|/live/)([A-Za-z0-9_-]{11})", s)
    if m:
        return m.group(1)
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", s):
        return s
    raise SystemExit("영상 ID를 인식할 수 없습니다: " + s)


def clean(text):
    text = re.sub(r"\[[^\]]*\]", " ", text)   # [music], [laughter], [applause] ...
    text = re.sub(r"\([^)]*\)", " ", text)     # (inaudible) 등
    text = text.replace(">>", " ")             # 화자 전환 표시
    text = re.sub(r"\s+", " ", text).strip()
    return text


def split_sentences(text):
    parts = re.split(r"(?<=[.!?])\s+", text)
    return [p.strip() for p in parts if p.strip()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url", help="유튜브 URL 또는 11자리 영상 ID")
    ap.add_argument("--lang", default="en", help="자막 언어 코드 (기본 en)")
    ap.add_argument("--out", default="", help="결과 JSON 저장 경로 (없으면 표준출력)")
    a = ap.parse_args()

    ensure_dep()
    from youtube_transcript_api import YouTubeTranscriptApi

    vid = parse_video_id(a.url)
    api = YouTubeTranscriptApi()
    tr = api.fetch(vid, languages=[a.lang, "en", "en-US", "en-GB"])

    raw = " ".join(seg.text.replace("\n", " ") for seg in tr)
    full = clean(raw)
    sents = split_sentences(full)

    # 소문자 기준 중복 제거(순서 유지)
    seen, uniq = set(), []
    for s in sents:
        k = s.lower()
        if k in seen:
            continue
        seen.add(k)
        uniq.append(s)

    result = {
        "video_id": vid,
        "lang": a.lang,
        "sentence_count": len(uniq),
        "sentences": [{"i": i + 1, "text": s} for i, s in enumerate(uniq)],
        "full_text": full,
    }
    js = json.dumps(result, ensure_ascii=False, indent=1)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(js)
        print(f"WROTE {a.out}  ({len(uniq)} sentences, {len(full)} chars, id={vid})")
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        print(js)


if __name__ == "__main__":
    main()
