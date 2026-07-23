# English Shadowing App

Single-file web app (`index.html`) for practicing English shadowing with
lessons of ~100 sentences each. No build step — open `index.html` in a browser.

## Data model
Lesson data is split out of `index.html` into per-lesson files under `lessons/`:
- `lessons/NN-<id>.js` — each does `window.LESSONS.push({...})`.
- `index.html` loads them via `<script src="lessons/NN-<id>.js">` tags (in NN
  order) before its main script, which reads `const LESSONS = window.LESSONS`.
- Because loading uses `<script>` (not `fetch`), the app still works when opened
  directly as a local `file://` (no server / CORS issues).

Each lesson object: `{id, name, gl, groups, bold, choiceBy, choicePrompt?, data:[{g, tag, en, ko, v?}]}`.
- `bold`: `phrasal|goingto|supposed|cond` triggers auto-bolding; `""` = none.
- `choiceBy`: `en` (quiz shows Korean, pick the English) or `tag`.
- `data[].v` is only for phrasal-verb lessons; omit it otherwise.

To add/replace a lesson, use `scripts/inject_lesson.py` (writes the `lessons/*.js`
file and its loader tag). Do not hand-edit `index.html` for lesson data.

## Adding lessons from a YouTube video  ← important workflow
When the user gives a **YouTube link (or 11-char video id)** and wants its
sentences in the app — including when they paste **only a link with little or no
other instruction** — automatically run the **`youtube-lesson`** agent with that
URL (via the Agent tool). Do not ask for confirmation first; that is the expected
default action for a bare YouTube link in this repo.

The agent captures the **real sentences spoken in the video** from its captions
(never invents them), curates + translates them to Korean, and injects a new
lesson into `index.html`. See `.claude/agents/youtube-lesson.md` for the full
procedure and `scripts/yt_transcript.py` / `scripts/inject_lesson.py` for the
deterministic extract + inject steps. A `/add-video <url>` command is also
available.

If the `youtube-lesson` agent type is not loaded in the current session, follow
the steps in `.claude/agents/youtube-lesson.md` yourself.

After adding a lesson, remind the user to refresh the browser.
