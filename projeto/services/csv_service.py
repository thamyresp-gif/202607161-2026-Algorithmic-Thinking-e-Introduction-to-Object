import csv
import os
from datetime import datetime


def exportar_csv(orcamento, diretorio="exports"):
    parcelas = orcamento.gerar_parcelas_csv()

    os.makedirs(diretorio, exist_ok=True)
    nome_arquivo = f"orcamento_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    caminho = os.path.join(diretorio, nome_arquivo)

    with open(caminho, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Mês", "Valor Aluguel (R$)", "Parcela Contrato (R$)", "Valor Total (R$)"])
        for p in parcelas:
            writer.writerow([
                p["parcela"],
                f"{p['valor_aluguel']:.2f}",
                f"{p['valor_parcela_contrato']:.2f}",
                f"{p['valor_total']:.2f}",
            ])

    return caminho
