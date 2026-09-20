---
generated_by: "build_obsidian_vault.py"
type: "map-of-content"
aliases: ["Lecture Concepts"]
tags: ["moc", "lectures", "concepts"]
cssclasses: ["research-note", "hub-note", "lecture-concepts-hub"]
---

[[Home|Research Lab]]  /  [[Lectures/Lecture Notes|Lectures]]

# Lecture Concepts

> [!concept] Atomic, reusable understanding
> Create a concept note when an idea has its own mechanism, equation, failure mode, or reusable explanation—not merely because a term appeared in a transcript.

```dataview
TABLE WITHOUT ID file.link AS "Concept", course AS "Course", confidence AS "Confidence", source_lectures AS "Source lectures"
FROM "Lectures/Concepts"
WHERE type = "lecture-concept"
SORT file.name ASC
```

> [!graph] Build a useful local graph
> Link each concept to one source lecture, one broader concept or course hub, and—when real—one paper, curriculum lesson, or neighboring concept.
