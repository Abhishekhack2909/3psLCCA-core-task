import json
from ...three_ps_lcca_core.core.main import run_full_lcc_analysis


# Import user-defined structured inputs
from .Input_global import Input_global


# ============================================================
# DEFINE CONSTRUCTION COST BREAKDOWN
# ============================================================

life_cycle_construction_cost_breakdown = {
    "initial_construction_cost": 12843979.44,
    "initial_carbon_emissions_cost": 2065434.91,
    "superstructure_construction_cost": 9356038.92,
    "total_scrap_value": 2164095.02,
}


# ============================================================
# RUN ANALYSIS FUNCTION WITH LATEX REPORT
# ============================================================


def execute_analysis_with_latex(input_data):
    """
    Runs the LCCA analysis using provided input dictionary and generates LaTeX report.
    """

    try:
        results = run_full_lcc_analysis(
            input_data, 
            life_cycle_construction_cost_breakdown, 
            debug=True,
            latex_report=True,
            latex_output_path="LCCA_Report.tex"
        )

        print("✔ LCC Analysis Completed Successfully.")
        print("✔ LaTeX Report Generated: LCCA_Report.tex")
        return results

    except Exception as e:
        print("✖ Error during LCC analysis:")
        print(e)
        import traceback
        traceback.print_exc()
        return None


# ============================================================
# MAIN EXECUTION
# ============================================================

# python -m src.examples.from_dict.example_with_latex
if __name__ == "__main__":
    print("--------------------------------------------------")
    print("Running 3psLCCA Analysis with LaTeX Report")
    print("--------------------------------------------------")

    results = execute_analysis_with_latex(Input_global)

    print("\n--- ANALYSIS COMPLETED ---")

    if results:
        print("Results generated successfully.")
        print("Check LCCA_Report.tex for the detailed report.")
    else:
        print("No results generated due to error.")
