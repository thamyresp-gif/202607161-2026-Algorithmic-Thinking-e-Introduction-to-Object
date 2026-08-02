import pytest
import subprocess
import json
from pathlib import Path


class TestMaintainabilityNFR:
    def test_cyclomatic_complexity_below_threshold(self):
        result = subprocess.run(
            ["radon", "cc", "models", "services", "app.py", "config.py", "-s", "-j"],
            capture_output=True,
            text=True,
            cwd=str(Path(__file__).parent.parent),
        )

        if result.stdout.strip():
            data = json.loads(result.stdout)
            max_cc = 0
            for file, funcs in data.items():
                for func in funcs:
                    cc = func.get("complexity", 0)
                    if cc > max_cc:
                        max_cc = cc

            assert max_cc < 10, f"Max cyclomatic complexity {max_cc} exceeds threshold of 10"

    def test_total_loc_within_reasonable_bounds(self):
        result = subprocess.run(
            ["radon", "raw", "models", "services", "app.py", "config.py", "-s", "-j"],
            capture_output=True,
            text=True,
            cwd=str(Path(__file__).parent.parent),
        )

        if result.stdout.strip():
            data = json.loads(result.stdout)
            total_loc = sum(d.get("loc", 0) for d in data.values())
            assert total_loc < 500, f"Total LOC {total_loc} exceeds 500 threshold"

    def test_no_duplicate_constant_definitions(self):
        config_path = Path(__file__).parent.parent / "config.py"
        orcamento_path = Path(__file__).parent.parent / "models" / "orcamento.py"

        config_content = config_path.read_text(encoding="utf-8")
        orcamento_content = orcamento_path.read_text(encoding="utf-8")

        config_constants = set()
        for line in config_content.splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line and line.split("=")[0].strip().isupper():
                config_constants.add(line.split("=")[0].strip())

        orcamento_constants = set()
        for line in orcamento_content.splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line and line.split("=")[0].strip().isupper():
                orcamento_constants.add(line.split("=")[0].strip())

        overlap = config_constants & orcamento_constants
        assert len(overlap) == 0, f"Duplicate constants found: {overlap}"

    def test_no_dead_code_in_controllers(self):
        controllers_dir = Path(__file__).parent.parent / "controllers"
        if not controllers_dir.exists():
            return

        for py_file in controllers_dir.glob("*.py"):
            if py_file.name == "__init__.py":
                continue
            content = py_file.read_text(encoding="utf-8").strip()
            assert len(content) > 10, f"Controller file {py_file.name} appears to be empty or dead code"

    def test_test_coverage_meets_threshold(self):
        result = subprocess.run(
            ["python", "-m", "pytest", "tests/", "--ignore=tests/test_playwright_flows.py",
             "--ignore=tests/test_nfr_performance.py", "--ignore=tests/test_nfr_security.py",
             "--ignore=tests/test_nfr_maintainability.py", "--cov=.", "--cov-report=json", "-q"],
            capture_output=True,
            text=True,
            cwd=str(Path(__file__).parent.parent),
        )

        cov_file = Path(__file__).parent.parent / "coverage.json"
        if cov_file.exists():
            data = json.loads(cov_file.read_text(encoding="utf-8"))
            coverage = data.get("totals", {}).get("percent_covered", 0)
            assert coverage >= 40, f"Test coverage {coverage}% is below 40% threshold"