"""
Tests for LaTeX report generation functionality.
"""

import os
import sys
import unittest

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.three_ps_lcca_core.core.main import run_full_lcc_analysis
from src.examples.from_dict.Input_global import Input_global


class TestLaTeXReportGeneration(unittest.TestCase):
    """Test cases for LaTeX report generation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.input_data = Input_global
        self.construction_costs = {
            "initial_construction_cost": 12843979.44,
            "initial_carbon_emissions_cost": 2065434.91,
            "superstructure_construction_cost": 9356038.92,
            "total_scrap_value": 2164095.02,
        }
        self.test_output_path = "test_report.tex"
    
    def tearDown(self):
        """Clean up test files."""
        if os.path.exists(self.test_output_path):
            os.remove(self.test_output_path)
    
    def test_latex_report_generation_default_path(self):
        """Test LaTeX report generation with default output path."""
        results = run_full_lcc_analysis(
            self.input_data,
            self.construction_costs,
            latex_report=True
        )
        
        # Check that results are returned
        self.assertIsNotNone(results)
        self.assertIn("initial_stage", results)
        self.assertIn("use_stage", results)
        self.assertIn("reconstruction", results)
        self.assertIn("end_of_life", results)
        
        # Check that default file was created
        self.assertTrue(os.path.exists("LCCA_Report.tex"))
        
        # Clean up
        if os.path.exists("LCCA_Report.tex"):
            os.remove("LCCA_Report.tex")
    
    def test_latex_report_generation_custom_path(self):
        """Test LaTeX report generation with custom output path."""
        results = run_full_lcc_analysis(
            self.input_data,
            self.construction_costs,
            latex_report=True,
            latex_output_path=self.test_output_path
        )
        
        # Check that results are returned
        self.assertIsNotNone(results)
        
        # Check that custom file was created
        self.assertTrue(os.path.exists(self.test_output_path))
        
        # Check file content
        with open(self.test_output_path, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn(r"\documentclass", content)
            self.assertIn(r"\begin{document}", content)
            self.assertIn(r"\end{document}", content)
            self.assertIn("Life Cycle Cost Analysis Report", content)
    
    def test_latex_report_disabled(self):
        """Test that LaTeX report is not generated when latex_report=False."""
        # Clean up any existing file first
        if os.path.exists("LCCA_Report.tex"):
            os.remove("LCCA_Report.tex")
        
        results = run_full_lcc_analysis(
            self.input_data,
            self.construction_costs,
            latex_report=False
        )
        
        # Check that results are returned
        self.assertIsNotNone(results)
        
        # Check that no LaTeX file was created
        self.assertFalse(os.path.exists("LCCA_Report.tex"))
    
    def test_latex_content_structure(self):
        """Test that generated LaTeX has proper structure."""
        run_full_lcc_analysis(
            self.input_data,
            self.construction_costs,
            latex_report=True,
            latex_output_path=self.test_output_path
        )
        
        with open(self.test_output_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Check for required sections
            self.assertIn(r"\section{Project Parameters}", content)
            self.assertIn(r"\section{Construction Cost Inputs}", content)
            self.assertIn(r"\section{Initial Construction Stage}", content)
            self.assertIn(r"\section{Use Stage (Maintenance)}", content)
            self.assertIn(r"\section{Reconstruction Stage}", content)
            self.assertIn(r"\section{End-of-Life Stage (Demolition)}", content)
            self.assertIn(r"\section{Summary}", content)


if __name__ == "__main__":
    unittest.main()
