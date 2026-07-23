#!/usr/bin/env python3
"""레슨 객체(JSON)를 lessons/ 폴더의 개별 JS 파일로 저장하고,
index.html 에 해당 파일을 읽는 <script> 로더 태그를 추가한다.

앱 구조
  - 레슨 데이터는 lessons/NN-<id>.js 파일들에 나뉘어 있고, 각 파일은
    `window.LESSONS.push({...})` 로 자신을 등록한다.
  - index.html 은 메인 <script> 앞에서 이 파일들을 순서대로 <script src> 로 읽는다.

동작
  - 같은 id 의 레슨 파일이 이미 있으면 그 파일 내용을 덮어쓴다(태그 중복 없음, 순서 유지).
  - 없으면 다음 번호(NN)로 새 파일을 만들고, 마지막 레슨 태그 뒤에 로더 태그를 추가한다.
  - 항상 유효한 JSON 왕복(json.loads/dumps)으로 안전하게 처리한다.

사용법
  python inject_lesson.py <index.html 경로> <lesson.json 경로>
"""
import os, re, sys, json, glob

PUSH_RE = re.compile(r"window\.LESSONS\.push\((.*)\);", re.S)


def slug(s):
    s = re.sub(r"[^A-Za-z0-9]+", "-", s or "lesson").strip("-").lower()
    return s or "lesson"


def lesson_file_body(lesson):
    body = json.dumps(lesson, ensure_ascii=False, separators=(",", ":"))
    return ("// 자동 생성 레슨 데이터 — index.html이 <script>로 읽어옵니다.\n"
            "window.LESSONS = window.LESSONS || [];\n"
            f"window.LESSONS.push({body});\n")


def existing_lessons(lessons_dir):
    """[(filename, id, number)] 정렬된 목록."""
    out = []
    for path in sorted(glob.glob(os.path.join(lessons_dir, "*.js"))):
        fn = os.path.basename(path)
        m = PUSH_RE.search(open(path, encoding="utf-8").read())
        lid = json.loads(m.group(1)).get("id") if m else None
        num = int(re.match(r"(\d+)", fn).group(1)) if re.match(r"(\d+)", fn) else 0
        out.append((fn, lid, num))
    return out


def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: python inject_lesson.py <index.html> <lesson.json>")
    html_path, lesson_path = sys.argv[1], sys.argv[2]
    root = os.path.dirname(os.path.abspath(html_path)) or "."
    lessons_dir = os.path.join(root, "lessons")
    os.makedirs(lessons_dir, exist_ok=True)

    new = json.load(open(lesson_path, encoding="utf-8"))
    if not new.get("id"):
        raise SystemExit("레슨에 'id' 필드가 필요합니다.")

    existing = existing_lessons(lessons_dir)
    by_id = {lid: fn for fn, lid, _ in existing if lid}

    if new["id"] in by_id:                       # 기존 레슨 덮어쓰기
        fn = by_id[new["id"]]
        with open(os.path.join(lessons_dir, fn), "w", encoding="utf-8", newline="") as f:
            f.write(lesson_file_body(new))
        action = "replaced"
    else:                                        # 새 레슨 파일 + 로더 태그
        nxt = (max([n for _, _, n in existing], default=0)) + 1
        fn = f"{nxt:02d}-{slug(new['id'])}.js"
        with open(os.path.join(lessons_dir, fn), "w", encoding="utf-8", newline="") as f:
            f.write(lesson_file_body(new))

        html = open(html_path, encoding="utf-8").read()
        tag = f'<script src="lessons/{fn}"></script>'
        if tag not in html:
            existing_tags = list(re.finditer(r'<script src="lessons/[^"]+"></script>', html))
            if existing_tags:                    # 마지막 레슨 태그 뒤에 삽입
                pos = existing_tags[-1].end()
                html = html[:pos] + "\n" + tag + html[pos:]
            else:                                # 로더 태그가 하나도 없으면 메인 <script> 앞
                idx = html.index("\n<script>\n")
                html = (html[:idx] + "\n<!-- 레슨 데이터 (레슨별 개별 파일) -->\n"
                        + tag + html[idx:])
            with open(html_path, "w", encoding="utf-8", newline="") as f:
                f.write(html)
        action = "appended"

    total = len(existing_lessons(lessons_dir))
    print(f"OK {action} id={new['id']} -> lessons/{fn} | total lessons = {total} | "
          f"sentences in this lesson = {len(new.get('data', []))}")


if __name__ == "__main__":
    main()
