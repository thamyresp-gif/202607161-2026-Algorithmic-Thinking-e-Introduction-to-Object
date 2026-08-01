import csv
import os
from datetime import datetime


def exportar_csv(orcamento, nome_arquivo=None):
    if nome_arquivo is None:
        nome_arquivo = f"orcamento_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    parcelas = orcamento.gerar_parcelas_csv()
    total = orcamento.calcular_total()

    caminho = os.path.join("exports", nome_arquivo)
    os.makedirs("exports", exist_ok=True)

    with open(caminho, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Parcela", "Valor (R$)"])
        for p in parcelas:
            writer.writerow([p["parcela"], f"{p['valor']:.2f}"])
        writer.writerow([])
        writer.writerow(["Resumo", "Valor (R$)"])
        writer.writerow(["Aluguel base", f"{total['aluguel_mensal']['valor_base']:.2f}"])
        writer.writerow(["Acréscimos", f"{total['aluguel_mensal']['valor_acrescimo_quartos']:.2f}"])
        writer.writerow(["Desconto", f"{total['aluguel_mensal']['valor_desconto']:.2f}"])
        writer.writerow(["Garagem", f"{total['aluguel_mensal']['valor_garagem']:.2f}"])
        writer.writerow(["Parcela contrato", f"{total['parcela_contrato']:.2f}"])
        writer.writerow(["Total mensal", f"{total['total_mensal']:.2f}"])

    return caminho