# Code - COMP6011 Task 2

This folder holds the proof-of-concept implementation of the Scale-CoT prompting pipeline described in Section 4 of the report.

## Files

- **`COMP6011_Task2_PoC.ipynb`** - the main artefact. A Colab notebook that runs the entire pipeline on the ten paraphrased clinical dialogues end-to-end. Designed for Colab's free T4 GPU.
- **`scale_cot_poc.py`** - a CLI version of the same logic, for use on a local on-premises GPU server. Useful for the production deployment story; not used by the markers directly.
- **`requirements.txt`** - pinned dependencies for the CLI version.

## How to run the notebook

1. Open Google Colab at https://colab.research.google.com.
2. File -> Upload notebook -> select `COMP6011_Task2_PoC.ipynb`.
3. Runtime -> Change runtime type -> T4 GPU -> Save.
4. You will need a Hugging Face access token (free, takes 2 minutes to create at https://huggingface.co/settings/tokens with the "Read" role).
5. Optionally, accept the Llama-3 licence at https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct. If you skip this, the notebook automatically falls back to Qwen-2.5-7B-Instruct.
6. Run cells top to bottom. About 5-10 minutes total on a T4.

The notebook produces two CSV files at the end:
- `poc_results.csv` - per-case predictions, scale-item scores, and per-case timings.
- `poc_summary.csv` - per-class agreement (matches Table 3 in the report).

Both files are safe to share since they do not contain dialogue text.

## How to run the CLI version

```bash
pip install -r requirements.txt
python scale_cot_poc.py --cases student_assignment_10_cases.xlsx --output poc_results.csv
```

The CLI script raises `NotImplementedError` from the `call_llm()` placeholder, which is intentional - that placeholder must be wired up to your specific local serving stack (vLLM, Ollama, transformers, or text-generation-inference). The notebook version handles this end-to-end inside Colab; the CLI version is for the on-premises production deployment described in the methodology.

## Privacy

Both the notebook and the CLI script are designed to keep dialogue text entirely on the executing machine. The notebook runs inside Colab's runtime; when the runtime ends, all state is destroyed. The CLI script runs on an air-gapped on-premises GPU. No version of the pipeline calls a public AI service (no OpenAI, no Anthropic, no Gemini APIs). This is the central privacy constraint of the unit's brief.

## What the pipeline does

For each input dialogue:

1. The Scale-CoT prompter queries the LLM six times, once per Columbia Suicide Severity Rating Scale item.
2. Each query asks for a binary 0/1 answer: does the C-SSRS item apply to the user based on the transcript?
3. The six binary scores are mapped deterministically to one of five risk levels (Safe, Ideation, Indicator, Behavior, Attempt) using the conservative mapping rule in `methodology/01_design_decisions.md`.
4. The prediction, scale-item scores, and timing are written to the output CSV.

The deterministic mapping and the parsing logic are unit-tested before each notebook run; the test cells are at the end of each module and visible in the notebook.

## Reproducibility

- Greedy decoding (`do_sample=False`) gives deterministic predictions for a fixed model and prompt.
- Pinned dependencies: `transformers==4.44.2`, `accelerate==0.33.0`, `bitsandbytes==0.43.3`, `openpyxl==3.1.5`.
- 4-bit NF4 quantisation matches the methodology's deployment recommendation.

## Ethical handling of the dataset

The cases come from the Human-AI-Dialogue-Suicide-Risk corpus (Chen et al., 2026, Zenodo 18684594). Per the unit's `ethical_guidelines.pdf`:

- The cases are not redistributed in this repository (the xlsx file is excluded via `.gitignore`).
- Output CSVs do not contain dialogue text.
- All local copies will be deleted on assessment completion.
