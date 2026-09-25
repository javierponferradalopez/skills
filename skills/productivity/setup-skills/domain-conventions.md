## Decision or convention

Each rule of this repo is an ADR in `docs/adr/`, of one of two kinds: a **decision** or a **convention**. The frontmatter of the ADR gives its kind and its status:

```md
---
kind: decision | convention
status: accepted | superseded by ADR-NNNN
---
```

A convention is the shape of the code: names, suffixes, folders, factories, the shape of a test. Its file is `NNNN-convention-<package>-<topic>.md`. The topic is the kind of class or file that it governs, and one package and topic have one `accepted` ADR.

<!-- Monorepo only. In a single-package repo, delete this list and each `<package>-` segment. -->
The packages:

- `<package>` — `<path>/`

### Before you write code

Read the `accepted` convention of each kind of class or file that you add or change: `ls docs/adr/*-convention-<package>-*` lists them. A convention is complete in itself: to follow it, you need no other ADR.

### Code that follows a superseded convention

It stays valid, and the superseded ADR explains it. When you change such a file for another reason, move it to the `accepted` convention.
