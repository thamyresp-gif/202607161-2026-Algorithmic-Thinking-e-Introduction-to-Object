#!/usr/bin/env python3
import subprocess
import json
import sys
import time
import csv
import hashlib
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
REPORT_FILE = PROJECT_DIR.parent / "nfr_report.json"

sys.path.insert(0, str(PROJECT_DIR))


def run_cmd(cmd, cwd=None):
    result = subprocess.run(
        cmd, shell=True, capture_output=True, text=True, cwd=cwd or PROJECT_DIR
    )
    return result.returncode, result.stdout, result.stderr


def measure_functional():
    print("[NFR] Measuring Functional Suitability...")
    rc, out, err = run_cmd(
        "python -m pytest tests/ --ignore=tests/test_playwright_flows.py "
        "--cov=. --cov-report=json --cov-report=term-missing -q",
        cwd=PROJECT_DIR,
    )
    coverage_data = {
        "lines": 0, "branches": 0, "functions": 0, "missing_lines": [],
    }
    if rc == 0:
        try:
            with open(PROJECT_DIR / "coverage.json") as f:
                cov = json.load(f)
                coverage_data["lines"] = cov.get("totals", {}).get("covered_lines", 0)
                coverage_data["branches"] = cov.get("totals", {}).get("covered_branches", 0)
                coverage_data["functions"] = cov.get("totals", {}).get("covered_functions", 0)
                coverage_data["missing_lines"] = cov.get("totals", {}).get("missing_lines", [])
        except Exception:
            pass
    return {"status": "PASS" if rc == 0 else "FAIL", "coverage": coverage_data}


def measure_maintainability():
    print("[NFR] Measuring Maintainability...")
    metrics = {"cyclomatic_complexity": {}, "duplication": {}, "loc": {}}

    rc, out, _ = run_cmd("radon cc models/ services/ app.py config.py -s -j", cwd=PROJECT_DIR)
    if rc == 0 and out.strip():
        try:
            cc_data = json.loads(out)
            for file, funcs in cc_data.items():
                for func in funcs:
                    metrics["cyclomatic_complexity"][f"{file}:{func['name']}"] = func["complexity"]
        except Exception:
            pass

    rc, out, _ = run_cmd("radon raw models/ services/ app.py config.py -s -j", cwd=PROJECT_DIR)
    if rc == 0 and out.strip():
        try:
            raw_data = json.loads(out)
            for file, data in raw_data.items():
                metrics["loc"][file] = {
                    "loc": data.get("loc", 0),
                    "lloc": data.get("lloc", 0),
                    "comments": data.get("comments", 0),
                    "multi": data.get("multi", 0),
                    "blank": data.get("blank", 0),
                }
        except Exception:
            pass

    max_cc = max(metrics["cyclomatic_complexity"].values(), default=0)
    total_loc = sum(d["loc"] for d in metrics["loc"].values())

    return {
        "status": "PASS" if max_cc < 10 else "WARN",
        "max_cyclomatic_complexity": max_cc,
        "total_loc": total_loc,
        "details": metrics,
    }


def measure_security():
    print("[NFR] Measuring Security...")
    rc, out, err = run_cmd(
        "bandit -r models/ services/ app.py config.py -f json -q", cwd=PROJECT_DIR
    )
    findings = {"high": 0, "medium": 0, "low": 0, "issues": []}
    if out.strip():
        try:
            data = json.loads(out)
            for issue in data.get("results", []):
                severity = issue.get("issue_severity", "LOW").upper()
                findings[severity.lower()] = findings.get(severity.lower(), 0) + 1
                findings["issues"].append({
                    "file": issue.get("filename", ""),
                    "line": issue.get("line_number", 0),
                    "severity": severity,
                    "confidence": issue.get("issue_confidence", ""),
                    "test": issue.get("test_id", ""),
                    "message": issue.get("issue_text", ""),
                })
        except Exception:
            pass
    return {"status": "PASS" if findings["high"] == 0 else "FAIL", "findings": findings}


def measure_performance():
    print("[NFR] Measuring Performance...")
    from models.imovel import Apartamento, Casa, Estudio
    from models.locatario import Locatario
    from models.orcamento import Orcamento

    results = {}
    for tipo, cls, args in [
        ("APARTAMENTO", Apartamento, ("Rua A, 100", 2, 1)),
        ("CASA", Casa, ("Rua B, 200", 3, 2)),
        ("ESTUDIO", Estudio, ("Rua C, 300", 1)),
    ]:
        imovel = cls(*args)
        locatario = Locatario("Teste", False)
        orcamento = Orcamento(imovel, locatario, parcelar=True, num_parcelas=2)

        start = time.perf_counter()
        for _ in range(1000):
            orcamento.calcular_total()
        elapsed = (time.perf_counter() - start) / 1000 * 1000

        results[tipo] = {
            "avg_time_ms": round(elapsed, 3),
            "iterations": 1000,
        }

    max_time = max(r["avg_time_ms"] for r in results.values())
    return {
        "status": "PASS" if max_time < 500 else "WARN",
        "max_avg_time_ms": round(max_time, 3),
        "details": results,
    }


def measure_portability():
    print("[NFR] Measuring Portability...")
    rc, out, err = run_cmd("pip install -r requirements.txt", cwd=PROJECT_DIR)
    return {"status": "PASS" if rc == 0 else "FAIL", "install_exit_code": rc}


def measure_csv_integrity():
    print("[NFR] Measuring CSV Integrity...")
    from models.imovel import Apartamento
    from models.locatario import Locatario
    from models.orcamento import Orcamento
    from services.csv_service import exportar_csv

    imovel = Apartamento("Rua A, 100", 2, 1)
    locatario = Locatario("Teste", False)
    orcamento = Orcamento(imovel, locatario, parcelar=False)
    orcamento.calcular_total()

    csv_path = exportar_csv(orcamento)
    if not csv_path or not Path(csv_path).exists():
        return {"status": "FAIL", "error": "CSV not generated"}

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    checksum = hashlib.sha256(Path(csv_path).read_bytes()).hexdigest()
    return {
        "status": "PASS",
        "rows": len(rows),
        "checksum": checksum,
        "path": csv_path,
    }


def main():
    print("=" * 60)
    print("  NFR Measurement Report — Orçamento de Aluguel R.M")
    print("  SWEBOK 4.0 / ISO/IEC 25010:2023")
    print("=" * 60)

    report = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "axes": {},
    }

    report["axes"]["functional"] = measure_functional()
    report["axes"]["maintainability"] = measure_maintainability()
    report["axes"]["security"] = measure_security()
    report["axes"]["performance"] = measure_performance()
    report["axes"]["portability"] = measure_portability()
    report["axes"]["compatibility"] = measure_csv_integrity()

    all_pass = all(
        a["status"] in ("PASS",) for a in report["axes"].values()
    )
    report["overall"] = "PASS" if all_pass else "FAIL"

    with open(REPORT_FILE, "w") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"\n{'=' * 60}")
    print(f"  Overall: {report['overall']}")
    for axis, data in report["axes"].items():
        print(f"  {axis}: {data['status']}")
    print(f"  Report saved to: {REPORT_FILE}")
    print(f"{'=' * 60}")

    return 0 if report["overall"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
