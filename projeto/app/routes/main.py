from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.imovel import Apartamento, Casa, Estudio
from app.models.locatario import Locatario
from app.models.orcamento import Orcamento
from app.routes.csv_exporter import exportar_csv

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/gerar_orcamento", methods=["POST"])
def gerar_orcamento():
    tipo = request.form.get("tipo_imovel")
    endereco = request.form.get("endereco", "")
    quartos = int(request.form.get("quartos", 1))
    vagas = int(request.form.get("vagas_garagem", 0))
    nome_locatario = request.form.get("nome_locatario", "")
    tem_filhos = request.form.get("tem_filhos") == "on"
    parcelar = request.form.get("parcelar") == "on"
    num_parcelas = int(request.form.get("num_parcelas", 1))

    if tipo == "APARTAMENTO":
        imovel = Apartamento(endereco, quartos, vagas)
    elif tipo == "CASA":
        imovel = Casa(endereco, quartos, vagas)
    elif tipo == "ESTUDIO":
        imovel = Estudio(endereco, vagas)
    else:
        flash("Tipo de imóvel inválido", "error")
        return redirect(url_for("main.index"))

    locatario = Locatario(nome_locatario, tem_filhos)
    orcamento = Orcamento(imovel, locatario, parcelar, num_parcelas)
    resultado = orcamento.calcular_total()
    parcelas = orcamento.gerar_parcelas_csv()

    return render_template(
        "resultado.html",
        imovel=imovel,
        locatario=locatario,
        resultado=resultado,
        parcelas=parcelas,
    )


@main.route("/exportar_csv")
def exportar():
    return redirect(url_for("main.index"))