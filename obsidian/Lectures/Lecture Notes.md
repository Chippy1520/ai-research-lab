---
generated_by: "build_obsidian_vault.py"
type: "map-of-content"
aliases: ["Lecture Notes"]
tags: ["moc", "lectures"]
cssclasses: ["research-note", "hub-note", "lecture-hub"]
---

[[Home|Research Lab]]  /  [[Lectures/Lecture Notes|Lectures]]

# Lecture Notes

> [!lecture] Capture → transcribe → distill → connect
> Record the lecture locally, preserve the raw transcript, then turn only durable ideas into linked concept notes.
>
> The graph is built from deliberate links—not from auto-linking every word in a transcript.

> [!map] Lecture workspace
> - [[Lectures/Courses|Courses]]
> - [[Lectures/Concepts|Lecture concepts]]
> - [[_Templates/Lecture Note|Lecture-note template]]
> - [[_Templates/Lecture Concept|Concept template]]

## Capture workflow

1. Run **Templater: Create new note from template** and choose **Lecture Note**.
2. Fill the course, module, lecturer, and status properties.
3. Start **Voice Scribe: Record voice note**. Keep the audio embed and transcript in the lecture note.
4. During class, write only cues, equations, diagrams, and questions under **Live notes**.
5. After class, distill the mechanism and worked examples; create atomic concept notes only for reusable ideas.
6. Link each concept back to its source lecture, related concepts, papers, and curriculum notes.

> [!privacy] Local transcription boundary
> Voice Scribe runs Whisper on-device after a one-time model download. No API key is required.
> Do not record a lecture unless the instructor and institutional rules permit it.

## All lecture notes

```dataview
TABLE WITHOUT ID file.link AS "Lecture", course AS "Course", module AS "Module", date AS "Date", status AS "Status"
FROM "Lectures/Notes"
WHERE type = "lecture-note"
SORT date DESC
```

## Review queue

```dataview
TABLE WITHOUT ID file.link AS "Lecture", course AS "Course", status AS "Status"
FROM "Lectures/Notes"
WHERE type = "lecture-note" AND status != "distilled"
SORT date ASC
```
