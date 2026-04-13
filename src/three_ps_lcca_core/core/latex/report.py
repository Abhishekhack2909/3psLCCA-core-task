"""
LaTeX Report Generator for 3psLCCA Life Cycle Cost Analysis

This module generates comprehensive, human-readable LaTeX reports that document
all lifecycle cost calculations with formulas, explanations, and step-by-step derivations.
"""

from typing import Dict, Any


class LaTeXReportGenerator:
    """Generates a comprehensive LaTeX report for LCCA results."""
    
    def __init__(self, results: Dict[str, Any], input_data: Dict[str, Any], 
                 construction_costs: Dict[str, Any]):
        self.results = results
        self.input_data = input_data
        self.construction_costs = construction_costs
        self.general_params = input_data.get("general_parameters", {})
        
    def escape_latex(self, text: str) -> str:
        """Escape special LaTeX characters."""
        replacements = {
            '&': r'\&',
            '%': r'\%',
            '$': r'\$',
            '#': r'\#',
            '_': r'\_',
            '{': r'\{',
            '}': r'\}',
            '~': r'\textasciitilde{}',
            '^': r'\^{}',
            '\\': r'\textbackslash{}',
        }
        for old, new in replacements.items():
            text = str(text).replace(old, new)
        return text
    
    def format_number(self, value: float, decimals: int = 2) -> str:
        """Format number with thousand separators."""
        if value is None:
            return "N/A"
        return f"{value:,.{decimals}f}"
    
    def generate_preamble(self) -> str:
        """Generate LaTeX document preamble."""
        return r"""\documentclass[12pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[margin=1in]{geometry}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{booktabs}
\usepackage{longtable}
\usepackage{graphicx}
\usepackage{float}
\usepackage{hyperref}
\usepackage{fancyhdr}

\pagestyle{fancy}
\fancyhf{}
\rhead{Life Cycle Cost Analysis Report}
\lhead{3psLCCA}
\cfoot{\thepage}

\title{Life Cycle Cost Analysis Report}
\author{3psLCCA Engine}
\date{\today}

\begin{document}

\maketitle
\tableofcontents
\newpage

"""
    
    def generate_title_page_content(self) -> str:
        """Generate title page with project parameters."""
        params = self.general_params
        
        content = r"""\section{Project Parameters}

The following table summarizes the key parameters used in this Life Cycle Cost Analysis:

\begin{table}[H]
\centering
\begin{tabular}{ll}
\toprule
\textbf{Parameter} & \textbf{Value} \\
\midrule
"""
        
        param_map = {
            "service_life_years": "Service Life (years)",
            "analysis_period_years": "Analysis Period (years)",
            "discount_rate_percent": "Discount Rate (\\%)",
            "inflation_rate_percent": "Inflation Rate (\\%)",
            "interest_rate_percent": "Interest Rate (\\%)",
            "currency_conversion": "Currency Conversion Factor"
        }
        
        for key, label in param_map.items():
            value = params.get(key, "N/A")
            # Don't escape label since it already has LaTeX commands
            content += f"{label} & {self.format_number(value)} \\\\\n"
        
        content += r"""\bottomrule
\end{tabular}
\caption{Project Parameters}
\end{table}

"""
        return content
    
    def generate_construction_costs_section(self) -> str:
        """Generate construction cost inputs section."""
        content = r"""\section{Construction Cost Inputs}

The initial construction costs and related parameters are summarized below:

\begin{table}[H]
\centering
\begin{tabular}{lr}
\toprule
\textbf{Cost Component} & \textbf{Value} \\
\midrule
"""
        
        cost_map = {
            "initial_construction_cost": "Initial Construction Cost",
            "initial_carbon_emissions_cost": "Initial Carbon Emissions Cost",
            "superstructure_construction_cost": "Superstructure Construction Cost",
            "total_scrap_value": "Total Scrap Value"
        }
        
        for key, label in cost_map.items():
            value = self.construction_costs.get(key, 0)
            content += f"{self.escape_latex(label)} & {self.format_number(value)} \\\\\n"
        
        content += r"""\bottomrule
\end{tabular}
\caption{Construction Cost Breakdown}
\end{table}

"""
        return content

    def generate_component_breakdown(self, component_name: str, breakdown: Dict[str, Any]) -> str:
        """Generate detailed breakdown for a single component calculation."""
        if not breakdown:
            return ""
        
        content = f"\\subsection{{{self.escape_latex(component_name)}}}\n\n"
        
        # Formulae section
        if "formulae" in breakdown:
            content += "\\textbf{Formulae:}\n\n"
            for formula_name, formula_text in breakdown["formulae"].items():
                content += f"\\textit{{{self.escape_latex(formula_name)}}}:\n"
                content += f"\\begin{{equation}}\n"
                content += f"\\text{{{self.escape_latex(formula_text)}}}\n"
                content += f"\\end{{equation}}\n\n"
        
        # Plain English explanation
        content += "\\textbf{Explanation:}\n\n"
        content += f"This calculation determines the {self.escape_latex(component_name.lower())} "
        content += "by applying the formulae shown above to the input parameters.\n\n"
        
        # Input values
        if "inputs" in breakdown:
            content += "\\textbf{Input Values:}\n\n"
            content += "\\begin{itemize}\n"
            for input_name, input_value in breakdown["inputs"].items():
                formatted_name = input_name.replace("_", " ").title()
                content += f"\\item {self.escape_latex(formatted_name)}: {self.format_number(input_value)}\n"
            content += "\\end{itemize}\n\n"
        
        # Computed values
        if "computed_values" in breakdown:
            content += "\\textbf{Computed Values:}\n\n"
            content += "\\begin{itemize}\n"
            for comp_name, comp_value in breakdown["computed_values"].items():
                formatted_name = comp_name.replace("_", " ").title()
                content += f"\\item {self.escape_latex(formatted_name)}: {self.format_number(comp_value)}\n"
            content += "\\end{itemize}\n\n"
        
        # Final result
        if "total" in breakdown or any(k.startswith("total_") for k in breakdown.keys()):
            total_key = "total" if "total" in breakdown else [k for k in breakdown.keys() if k.startswith("total_")][0]
            total_value = breakdown.get(total_key, 0)
            content += f"\\textbf{{Final Result:}} {self.format_number(total_value)}\n\n"
        
        return content
    
    def generate_stage_section(self, stage_name: str, stage_data: Dict[str, Any]) -> str:
        """Generate a complete section for a lifecycle stage."""
        stage_titles = {
            "initial_stage": "Initial Construction Stage",
            "use_stage": "Use Stage (Maintenance)",
            "reconstruction": "Reconstruction Stage",
            "end_of_life": "End-of-Life Stage (Demolition)"
        }
        
        title = stage_titles.get(stage_name, stage_name.replace("_", " ").title())
        content = f"\\section{{{self.escape_latex(title)}}}\n\n"
        
        # Summary table
        content += "\\subsection{Summary}\n\n"
        content += "\\begin{table}[H]\n\\centering\n"
        content += "\\begin{tabular}{lr}\n\\toprule\n"
        content += "\\textbf{Component} & \\textbf{Cost} \\\\\n\\midrule\n"
        
        # Extract all components and their totals
        # Stage data has categories: economic, environmental, social
        components = {}
        total_stage_cost = 0
        
        for category, category_data in stage_data.items():
            if isinstance(category_data, dict) and category not in ["warnings", "notes"]:
                for comp_name, comp_value in category_data.items():
                    if isinstance(comp_value, (int, float)):
                        formatted_name = comp_name.replace("_", " ").title()
                        components[formatted_name] = comp_value
                        total_stage_cost += comp_value
        
        for comp_name, comp_value in components.items():
            content += f"{self.escape_latex(comp_name)} & {self.format_number(comp_value)} \\\\\n"
        
        content += "\\midrule\n"
        content += f"\\textbf{{Total}} & \\textbf{{{self.format_number(total_stage_cost)}}} \\\\\n"
        content += "\\bottomrule\n\\end{tabular}\n"
        content += f"\\caption{{{self.escape_latex(title)} - Summary}}\n\\end{{table}}\n\n"
        
        # Note: Detailed breakdowns would require debug data which isn't in the basic output
        # The debug data is written to JSON files, not returned in the results
        content += "\\textit{Note: Detailed calculation breakdowns are available in the debug JSON files.}\n\n"
        
        return content
    
    def generate_summary_section(self) -> str:
        """Generate final summary with totals for all stages."""
        content = r"""\section{Summary}

The following table presents the total costs for each lifecycle stage and the grand total:

\begin{table}[H]
\centering
\begin{tabular}{lr}
\toprule
\textbf{Lifecycle Stage} & \textbf{Total Cost} \\
\midrule
"""
        
        stage_totals = {}
        stage_names = {
            "initial_stage": "Initial Construction",
            "use_stage": "Use Stage (Maintenance)",
            "reconstruction": "Reconstruction",
            "end_of_life": "End-of-Life (Demolition)"
        }
        
        grand_total = 0
        
        for stage_key, stage_label in stage_names.items():
            stage_data = self.results.get(stage_key, {})
            stage_total = 0
            
            # Sum all numeric values in all categories
            for category, category_data in stage_data.items():
                if isinstance(category_data, dict) and category not in ["warnings", "notes"]:
                    for comp_name, comp_value in category_data.items():
                        if isinstance(comp_value, (int, float)):
                            stage_total += comp_value
            
            stage_totals[stage_key] = stage_total
            content += f"{self.escape_latex(stage_label)} & {self.format_number(stage_total)} \\\\\n"
            grand_total += stage_total
        
        content += "\\midrule\n"
        content += f"\\textbf{{Grand Total}} & \\textbf{{{self.format_number(grand_total)}}} \\\\\n"
        content += r"""\bottomrule
\end{tabular}
\caption{Lifecycle Cost Summary}
\end{table}

"""
        return content
    
    def generate_report(self) -> str:
        """Generate the complete LaTeX report."""
        report = self.generate_preamble()
        report += self.generate_title_page_content()
        report += self.generate_construction_costs_section()
        
        # Generate sections for each stage
        for stage_name in ["initial_stage", "use_stage", "reconstruction", "end_of_life"]:
            if stage_name in self.results:
                report += self.generate_stage_section(stage_name, self.results[stage_name])
        
        report += self.generate_summary_section()
        report += r"\end{document}"
        
        return report


def generate_latex_report(results: Dict[str, Any], input_data: Dict[str, Any],
                         construction_costs: Dict[str, Any], output_path: str):
    """
    Generate a comprehensive LaTeX report for LCCA results.
    
    Args:
        results: The results dictionary from run_full_lcc_analysis
        input_data: The input data dictionary
        construction_costs: The construction costs dictionary
        output_path: Path where the .tex file should be saved
    """
    generator = LaTeXReportGenerator(results, input_data, construction_costs)
    latex_content = generator.generate_report()
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(latex_content)
