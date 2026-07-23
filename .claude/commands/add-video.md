---
description: Add a YouTube video's real English sentences to the app as a new lesson
argument-hint: <youtube-url-or-id>
---

Add the English sentences actually spoken in this YouTube video to the shadowing
app as a new lesson: $ARGUMENTS

Use the `youtube-lesson` agent to do it (extract captions → curate → translate →
inject into `index.html`). If that agent isn't available, follow the workflow in
`.claude/agents/youtube-lesson.md` directly.
