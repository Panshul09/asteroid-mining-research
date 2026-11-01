# Asteroid Mining Research

An independent literature review and Python scenario analysis exploring how selected technical and economic assumptions affect the break-even resource price in a simplified asteroid-mining scenario.

## Main research question

In a simplified asteroid-mining scenario, how do selected technical and economic assumptions affect the required break-even resource price, and what does this imply about potential commercial viability?

## Files

- `paper.pdf` — formatted reviewed manuscript, exported from `paper_final.docx`.
- `paper_final.docx` — editable Word manuscript. Edit this file, then export a new PDF when ready.
- `paper/paper.md` — Markdown source version of the manuscript for GitHub.
- `paper/references.md` — bibliography and source links.
- `paper/figure_notes.md` — descriptions and caveats for the four figures.
- `src/model.py` — model inputs, validation, and equations.
- `src/run_analysis.py` — creates the baseline results and assumptions file.
- `src/make_figures.py` — generates the four analysis figures.
- `src/run_all.py` — runs the results and figure-generation steps.
- `data/assumptions.csv` — baseline values and labels indicating which values are assumptions.
- `results/` — generated baseline and sensitivity-analysis outputs.
- `figures/` — generated graphs embedded in the manuscript.
- `tests/` — basic automated tests for the baseline calculation.
- `GUIDE.md` — setup, GitHub upload, and research-archive instructions.

## Important interpretation note

This is an educational scenario model, not a forecast of the real-world profitability of asteroid mining. Several numerical inputs are illustrative assumptions rather than measured costs or properties of a specific asteroid. The $3,600/kg figure is a contextual estimate from a published study of asteroid-derived propellant delivery to lunar orbit; it is not a market price and is not directly equivalent to the model's break-even price.

## Run the analysis on Windows

Open this folder in VS Code, choose **Terminal → New Terminal**, and run:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe src\run_all.py
.venv\Scripts\python.exe -m pytest
```

After `run_all.py` completes, open the `figures` folder in VS Code and double-click a `.png` file to view it. The same run also refreshes the files in `results/` and `data/assumptions.csv`.

## Editing and exporting the manuscript

Word and Markdown are separate files: editing `paper_final.docx` does not automatically update `paper/paper.md`, or vice versa. Keep both versions synchronized before public release. After updating the DOCX, export it to PDF using Word for the web or LibreOffice, inspect every page, and replace `paper.pdf` with that final exported PDF.

Before publication, replace the `[ADD GITHUB REPOSITORY URL BEFORE PUBLIC RELEASE]` placeholder in the DOCX and Markdown manuscript with the actual public repository URL, then export and verify the PDF again.

## Research integrity

- Cite factual claims and check each reference against the source.
- Keep the model assumptions clearly labeled as assumptions.
- Describe outputs as scenario results, not forecasts.
- Be transparent about AI assistance; an AI-assisted scenario model is not the same as a peer-reviewed study.
- GitHub and Zenodo are useful for sharing and archiving work, but neither means a paper has been peer-reviewed by a scientific journal.
