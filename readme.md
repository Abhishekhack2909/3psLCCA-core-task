# Intern Screening Task - 3psLCCA LaTeX Report Generator


## Objective

The objective of this task is to extend the existing LCCA engine to generate a **comprehensive, human-readable LaTeX report** that clearly explains all lifecycle cost calculations.

The report should not only present results, but also:

* Document every formula used
* Explain the purpose of each calculation in plain English
* Show all input values
* Provide step-by-step derivations
* Present final computed values in a structured format

This ensures the output is suitable for **engineering review, auditing, and documentation purposes**.

## Background

3psLCCA is a Life Cycle Cost Analysis (LCCA) engine for bridge infrastructure. It calculates costs across four lifecycle stages: **initial construction**, **use (maintenance)**, **reconstruction**, and **end-of-life (demolition)**.

The core entry point is `run_full_lcc_analysis()` in:

```
src/three_ps_lcca_core/core/main.py
```

The function currently accepts a `debug=True` flag. When enabled, each calculation step inside `StageCostCalculator` (in `stage_cost.py`) exposes a detailed breakdown dictionary containing:

* `formulae` — the equations used
* `inputs` — the raw values fed into each formula
* `computed_values` — intermediate and final results

Your task is to make use of these debug breakdowns to generate a structured **LaTeX report**.

---

## Your Task

Add a `latex_report` parameter to `run_full_lcc_analysis()` that, when set to `True`, generates a `.tex` file containing a well-structured LCCA report.

### Function Signature (after your change)

```python
def run_full_lcc_analysis(
    input_data,
    construction_costs,
    debug=False,
    latex_report=False,        # <-- add this
    latex_output_path=None,    # <-- optional: where to save the file
):
```

### Behaviour

| Parameter           | Value                  | Effect                                                     |
| ------------------- | ---------------------- | ---------------------------------------------------------- |
| `latex_report`      | `False` (default)      | No change — existing behaviour preserved                   |
| `latex_report`      | `True`                 | Generates a `.tex` file and saves it to disk               |
| `latex_output_path` | `None`                 | Save as `LCCA_Report.tex` in the current working directory |
| `latex_output_path` | `"path/to/report.tex"` | Save to the specified path                                 |

**Important:** When `latex_report=True`, the function must internally enable `debug=True` (even if the caller did not set it) so that the breakdown data is available to build the report. The `debug` JSON dump behaviour should only trigger if the caller explicitly passed `debug=True`.

---

## Additional Requirement (Detailed Explanation of Calculations)

The generated LaTeX report must not only display formulas and results, but also **clearly explain every equation and calculation step**.

For every cost component across all stages, the report must include:

* The formula (in LaTeX format)
* A brief plain-English explanation of what the formula represents
* A list of input values used in the calculation
* Substitution of actual values into the formula
* Step-by-step breakdown of how the result is computed
* The final computed value

This applies to **all stages and all sub-components**, including:

* Initial stage calculations
* Use stage maintenance components
* Reconstruction cycles
* End-of-life costs

---

## Report Structure

The generated `.tex` file must compile with `pdflatex` without errors and contain the following sections, in order:

### 1. Title Page

* Report title: **Life Cycle Cost Analysis Report**
* Project parameters table: `service_life_years`, `analysis_period_years`, `discount_rate_percent`, `inflation_rate_percent`, `interest_rate_percent`, `currency_conversion`

### 2. Construction Cost Inputs

* Table of the `construction_costs` dict passed to the function:
  `initial_construction_cost`, `initial_carbon_emissions_cost`, `superstructure_construction_cost`, `total_scrap_value`

### 3. Initial Stage

* Summary table of `initial_stage` results
* Sub-section for each cost component (construction costs, time cost of loan, road user cost) with:

  * The formula used (from `breakdown["formulae"]`)
  * Input values (from `breakdown["inputs"]`)
  * Computed result
  * **Detailed explanation and step-by-step derivation (as described above)**

### 4. Use Stage

* Summary table of `use_stage` results
* Sub-sections for routine inspection, periodic maintenance, major inspection, major repair, and bearing/expansion joint replacement
* Each sub-section should list:

  * Formula
  * Inputs
  * Result
  * **Detailed explanation and step-by-step derivation**

### 5. Reconstruction

* Summary of reconstruction costs across cycles
* Table with present worth factors and computed costs per reconstruction cycle
* Include **explanation of discounting logic and step-by-step calculation of present worth values**

### 6. End-of-Life Stage

* Demolition, disposal, and scrap value costs
* Formula and computed values
* **Include full explanation and derivation steps**

### 7. Summary

* Final summary table with all four stage totals and a grand total

---


## How to Run the Existing Example

From the project root:

```bash
python -m src.examples.from_dict.example
```

Study the output and the `debug` JSON files dumped (e.g., `A0_Core_Inputs.json`, `Stage_Cost_Calculator_Inputs.json`) to understand the data structure your report generator will consume.

---

## Files to Read Before Starting

| File                                                   | Why                                               |
| ------------------------------------------------------ | ------------------------------------------------- |
| `src/three_ps_lcca_core/core/main.py`                  | Entry point — this is where you add the parameter |
| `src/three_ps_lcca_core/core/stage_cost/stage_cost.py` | All calculations and debug breakdowns             |
| `src/examples/from_dict/example.py`                    | Working example to test against                   |
| `src/examples/from_dict/Input_global.py`               | Sample input in global RUC mode                   |

---
## Deliverables

Submit a single pull request (or zip of your changes) containing:

* [ ] Modified `main.py` with the new `latex_report` and `latex_output_path` parameters
* [ ] New file `src/three_ps_lcca_core/core/latex/report.py` (or equivalent module) containing the report generation logic
* [ ] At least one test in `tests/`
* [ ] A sample `LCCA_Report.tex` generated from `Input_global.py` (so we can see your output without running the code)
* [ ] **Raise a Pull Request (PR)** with clear commit history and description of changes
* [ ] **Submit a short video walkthrough (5–10 minutes)** explaining:

  * Your approach
  * Code structure
  * How the LaTeX report is generated
  * Sample output and key sections

---
