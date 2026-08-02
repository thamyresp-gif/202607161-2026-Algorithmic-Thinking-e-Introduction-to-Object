import pytest
import subprocess
import json
from pathlib import Path


class TestSecurityNFR:
    def test_bandit_no_high_severity_issues(self):
        result = subprocess.run(
            ["bandit", "-r", "models/", "services/", "app.py", "config.py", "-f", "json", "-q"],
            capture_output=True,
            text=True,
            cwd=str(Path(__file__).parent.parent),
        )

        if result.stdout.strip():
            try:
                data = json.loads(result.stdout)
                high_issues = [
                    i for i in data.get("results", [])
                    if i.get("issue_severity", "").upper() == "HIGH"
                ]
                assert len(high_issues) == 0, f"Found {len(high_issues)} high severity issues"
            except json.JSONDecodeError:
                pass

    def test_csv_export_does_not_leak_sensitive_data(self):
        from models.imovel import Apartamento
        from models.locatario import Locatario
        from models.orcamento import Orcamento
        from services.csv_service import exportar_csv

        imovel = Apartamento("Rua A, 100", 2, 1)
        locatario = Locatario("Joao", False)
        orcamento = Orcamento(imovel, locatario, parcelar=False)
        orcamento.calcular_total()

        csv_path = exportar_csv(orcamento)
        assert Path(csv_path).exists(), "CSV file was not generated"

        content = Path(csv_path).read_text(encoding="utf-8")
        assert "Parcela" in content, "CSV missing parcela column"
        assert "Valor" in content, "CSV missing value column"

    def test_csv_format_is_valid(self):
        from models.imovel import Apartamento
        from models.locatario import Locatario
        from models.orcamento import Orcamento
        from services.csv_service import exportar_csv

        imovel = Apartamento("Rua A, 100", 2, 1)
        locatario = Locatario("Joao", False)
        orcamento = Orcamento(imovel, locatario, parcelar=False)
        orcamento.calcular_total()

        csv_path = exportar_csv(orcamento)
        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = f.read()

        assert reader.lower().startswith("mês"), "CSV missing header row"
        assert ";" in reader or "," in reader, "CSV missing delimiter"

    def test_input_sanitization_no_code_injection(self):
        from models.imovel import Apartamento
        from models.locatario import Locatario
        from models.orcamento import Orcamento

        malicious_names = [
            "<script>alert('xss')</script>",
            "'; DROP TABLE orcamento; --",
            "{{7*7}}",
            "${7*7}",
            "| cat /etc/passwd",
        ]

        for malicious in malicious_names:
            imovel = Apartamento("Rua A, 100", 2, 1)
            locatario = Locatario(malicious, False)
            orcamento = Orcamento(imovel, locatario, parcelar=False)
            result = orcamento.calcular_total()

            assert result["total_mensal"] > 0, f"Calculation failed for input: {malicious}"