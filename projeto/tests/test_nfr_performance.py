import time
import pytest
from models.imovel import Apartamento, Casa, Estudio
from models.locatario import Locatario
from models.orcamento import Orcamento


class TestPerformanceNFR:
    def test_apartamento_calculation_speed(self):
        imovel = Apartamento("Rua A, 100", 2, 1)
        locatario = Locatario("Maria", False)
        orcamento = Orcamento(imovel, locatario, parcelar=True, num_parcelas=2)

        start = time.perf_counter()
        for _ in range(1000):
            orcamento.calcular_total()
        elapsed_ms = (time.perf_counter() - start) / 1000 * 1000

        assert elapsed_ms < 500, f"Avg time {elapsed_ms:.3f}ms exceeds 500ms threshold"

    def test_casa_calculation_speed(self):
        imovel = Casa("Rua B, 200", 3, 2)
        locatario = Locatario("Carlos", True)
        orcamento = Orcamento(imovel, locatario, parcelar=False)

        start = time.perf_counter()
        for _ in range(1000):
            orcamento.calcular_total()
        elapsed_ms = (time.perf_counter() - start) / 1000 * 1000

        assert elapsed_ms < 500, f"Avg time {elapsed_ms:.3f}ms exceeds 500ms threshold"

    def test_estudio_calculation_speed(self):
        imovel = Estudio("Rua C, 300", 1)
        locatario = Locatario("Ana", False)
        orcamento = Orcamento(imovel, locatario, parcelar=True, num_parcelas=5)

        start = time.perf_counter()
        for _ in range(1000):
            orcamento.calcular_total()
        elapsed_ms = (time.perf_counter() - start) / 1000 * 1000

        assert elapsed_ms < 500, f"Avg time {elapsed_ms:.3f}ms exceeds 500ms threshold"

    def test_csv_export_speed(self):
        from services.csv_service import exportar_csv

        imovel = Apartamento("Rua A, 100", 2, 1)
        locatario = Locatario("Maria", False)
        orcamento = Orcamento(imovel, locatario, parcelar=True, num_parcelas=2)
        orcamento.calcular_total()

        start = time.perf_counter()
        for _ in range(100):
            exportar_csv(orcamento)
        elapsed_ms = (time.perf_counter() - start) / 100 * 1000

        assert elapsed_ms < 500, f"CSV export avg {elapsed_ms:.3f}ms exceeds 500ms threshold"

    def test_memory_usage_within_limits(self):
        import tracemalloc

        tracemalloc.start()

        imovel = Apartamento("Rua A, 100", 2, 1)
        locatario = Locatario("Maria", False)
        orcamento = Orcamento(imovel, locatario, parcelar=True, num_parcelas=2)
        orcamento.calcular_total()

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        peak_mb = peak / (1024 * 1024)
        assert peak_mb < 50, f"Peak memory {peak_mb:.2f}MB exceeds 50MB threshold"