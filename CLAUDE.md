# Data Science & AI handbook

Source in `course/source/` (Markdown lessons, `build.py`, `make_pdfs.js`, `make_catalog.py`); built site in `course/`.

## Owner's standing instruction: publish without waiting
The owner (Varun Kumar) has asked that changes go live automatically:
1. Edit lessons in `course/source/lessons/`, then run `python3 build.py <lesson-id>` (or with no argument for everything), `node make_pdfs.js <filter>` and `python3 make_catalog.py`.
2. Check the rebuilt lessons for execution errors and #N/A/#NAME? cells, and that every link resolves.
3. Merge into `main` and push (`git push origin HEAD:main`), and push the feature branch.
4. Copy the built `course/` into the website repository (varunkumar1989/Skillnavora) under `data-science/` (skip `source/`, `print/` and files over 25 MB) and publish it there the same way.
