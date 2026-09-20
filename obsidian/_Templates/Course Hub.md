<%* /* generated_by: "build_obsidian_vault.py" */ -%>
---
type: course-hub
aliases: ["<% tp.file.title %>"]
course: "<% tp.file.title %>"
semester: ""
instructor: ""
tags: [course, lectures]
cssclasses: [research-note, hub-note, course-note]
---

[[Home|Research Lab]]  /  [[Lectures/Courses|Courses]]

# <% tp.file.title %>

> [!lecture] Course map
> Scope, sequence, recurring mechanisms, and unresolved questions.

## Course objectives

## Lecture sequence

```dataview
TABLE WITHOUT ID file.link AS "Lecture", module AS "Module", date AS "Date", status AS "Status"
FROM "Lectures/Notes"
WHERE type = "lecture-note" AND course = this.course
SORT date ASC
```

## Concept network

```dataview
TABLE WITHOUT ID file.link AS "Concept", confidence AS "Confidence", source_lectures AS "Sources"
FROM "Lectures/Concepts"
WHERE type = "lecture-concept" AND course = this.course
SORT file.name ASC
```

## Recurring mechanisms

## Open questions
