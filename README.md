# 영어 쉐도잉 연습 앱 (English Shadowing Practice)

미드 스타일 필수 표현을 듣고 따라 말하며 익히는 웹앱입니다. 총 7개 레슨, 700문장.

- Lesson 1 · 구동사 100 (talk / hang / turn / show / run / live)
- Lesson 2 · be going to 100
- Lesson 3 · 속담·격언 100
- Lesson 4 · 비즈니스 스피치 100
- Lesson 5 · 여행 영어 100
- Lesson 6 · be supposed to 100
- Lesson 7 · 나에 대해 말하기 100

## 기능
- 🔊 원어민 음성 재생(속도 조절), 한글 뜻 가리기/보기, 주제별 필터
- ✍️ 받아쓰기 · 뜻 맞히기 퀴즈 (단축키 — 3: 듣기, 1: 확인, 2: 다음)
- 브라우저 내장 TTS(Web Speech API) 사용. Chrome·Edge 권장.

## 실행 방법
`index.html` 파일 하나로 동작합니다. 파일을 브라우저로 열거나, 아래처럼 GitHub Pages로 게시하면 인터넷 주소로 어디서든 실행됩니다.

---

## GitHub Pages로 게시하기 (가장 쉬운 방법 · 웹에서 클릭만)

1. github.com 에 로그인 → 오른쪽 위 **+** → **New repository**
2. 이름 입력(예: `english-shadowing`) → **Public** 선택 → **Create repository**
3. 새 저장소 화면에서 **uploading an existing file** 링크 클릭
4. `index.html` 파일을 끌어다 놓고(README.md도 함께 올려도 됨) → **Commit changes**
5. 상단 **Settings** → 왼쪽 **Pages** 메뉴
6. **Branch** 를 `main` / `/(root)` 로 선택 → **Save**
7. 1~2분 뒤 페이지 상단에 표시되는 주소
   `https://<사용자이름>.github.io/english-shadowing/` 로 접속하면 앱이 실행됩니다.

## Git 명령으로 올리는 방법 (터미널에 익숙한 경우)
```bash
git init
git add index.html README.md
git commit -m "Add English shadowing app"
git branch -M main
git remote add origin https://github.com/<사용자이름>/english-shadowing.git
git push -u origin main
```
그런 다음 위 6~7번(Settings → Pages)만 동일하게 진행하세요.
