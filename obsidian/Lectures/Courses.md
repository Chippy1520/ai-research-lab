---
generated_by: "build_obsidian_vault.py"
type: "map-of-content"
aliases: ["Courses"]
tags: ["moc", "lectures", "courses"]
cssclasses: ["research-note", "hub-note", "course-hub"]
---

[[Home|Research Lab]]  /  [[Lectures/Lecture Notes|Lectures]]

# Courses

> [!lecture] Course-level maps
> A course hub should connect lectures in sequence and expose the concepts that recur across them.

```dataview
TABLE WITHOUT ID rows.file.link AS "Lectures"
FROM "Lectures/Notes"
WHERE type = "lecture-note" AND course
GROUP BY course
SORT key ASC
```

> [!method] Create a course hub
> Use the **Course Hub** template, then give every lecture in that course the exact same `course` property.
