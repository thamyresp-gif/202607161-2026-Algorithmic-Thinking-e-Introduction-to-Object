import streamlit as st
from models.imovel import Apartamento, Casa, Estudio
from models.locatario import Locatario
from models.orcamento import Orcamento
from services.csv_service import exportar_csv


def main():
    st.set_page_config(page_title="Orçamento de Aluguel — R.M", page_icon="🏠")
    st.title("🏠 Orçamento de Aluguel — R.M")

    with st.form("orcamento_form"):
        st.header("Dados do Imóvel")
        tipo = st.selectbox("Tipo de Imóvel", ["APARTAMENTO", "CASA", "ESTUDIO"])
        endereco = st.text_input("Endereço", placeholder="Rua, número, bairro")
        quartos = st.number_input("Número de Quartos", min_value=1, max_value=10, value=1, step=1)
        vagas = st.number_input("Vagas de Garagem", min_value=0, max_value=10, value=0, step=1)

        st.header("Dados do Locatário")
        nome = st.text_input("Nome do Locatário", placeholder="Nome completo")
        tem_filhos = st.checkbox("Possui filhos?")

        st.header("Parcelamento do Contrato")
        parcelar = st.checkbox("Parcelar taxa de contrato (R$ 2.000,00)")
        num_parcelas = st.slider("Número de parcelas (máx. 5)", min_value=1, max_value=5, value=1)

        submitted = st.form_submit_button("Gerar Orçamento")

    if submitted:
        if not endereco or not nome:
            st.error("Preencha o endereço e o nome do locatário.")
            return

        if tipo == "APARTAMENTO":
            imovel = Apartamento(endereco, quartos, vagas)
        elif tipo == "CASA":
            imovel = Casa(endereco, quartos, vagas)
        else:
            imovel = Estudio(endereco, vagas)

        locatario = Locatario(nome, tem_filhos)
        orcamento = Orcamento(imovel, locatario, parcelar, num_parcelas)
        resultado = orcamento.calcular_total()
        parcelas = orcamento.gerar_parcelas_csv()

        st.header("📊 Resumo do Orçamento")

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Imóvel")
            st.write(f"**Tipo:** {imovel.tipo}")
            st.write(f"**Endereço:** {imovel.endereco}")
            st.write(f"**Quartos:** {imovel.quartos}")
            st.write(f"**Vagas de Garagem:** {imovel.vagas_garagem}")

        with col2:
            st.subheader("Locatário")
            st.write(f"**Nome:** {locatario.nome}")
            st.write(f"**Possui filhos:** {'Sim' if locatario.tem_filhos else 'Não'}")

        st.subheader("Detalhes Financeiros")
        col3, col4, col5 = st.columns(3)
        with col3:
            st.metric("Valor Base", f"R$ {resultado['aluguel_mensal']['valor_base']:.2f}")
        with col4:
            st.metric("Acréscimos", f"R$ {resultado['aluguel_mensal']['valor_acrescimo_quartos']:.2f}")
        with col5:
            st.metric("Desconto", f"-R$ {resultado['aluguel_mensal']['valor_desconto']:.2f}")

        col6, col7 = st.columns(2)
        with col6:
            st.metric("Valor Garagem", f"R$ {resultado['aluguel_mensal']['valor_garagem']:.2f}")
        with col7:
            st.metric("Parcela do Contrato", f"R$ {resultado['parcela_contrato']:.2f}")

        st.success(f"💰 **Total Mensal: R$ {resultado['total_mensal']:.2f}**")

        st.subheader("📋 12 Parcelas do Orçamento")
        st.dataframe(parcelas, use_container_width=True)

        csv_path = exportar_csv(orcamento)
        st.success(f"📁 Arquivo CSV exportado: `{csv_path}`")


if __name__ == "__main__":
    main()
