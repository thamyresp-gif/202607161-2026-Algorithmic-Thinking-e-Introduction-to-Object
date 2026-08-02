import pytest
from playwright.sync_api import sync_playwright

BASE_URL = "http://localhost:8501"


@pytest.fixture(scope="module")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    page.goto(BASE_URL)
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)
    yield page
    context.close()


def wait_for_app_ready(page):
    page.wait_for_selector("[data-testid=\"stApp\"]", timeout=15000)


def select_combobox_option(page, label, option_text):
    combobox = page.get_by_role("combobox", name=label)
    combobox.click()
    page.wait_for_timeout(500)
    option = page.get_by_text(option_text).first
    option.click()
    page.wait_for_timeout(500)


def check_checkbox(page, label_text):
    escaped = label_text.replace('"', '\\"').replace('$', '\\$')
    page.evaluate(
        f"""() => {{
        const el = document.querySelector('input[aria-label="{escaped}"]');
        if (el) {{ el.click(); el.dispatchEvent(new Event('change', {{ bubbles: true }})); }}
    }}"""
    )
    page.wait_for_timeout(300)


def set_slider(page, label_text, value):
    slider = page.get_by_role("slider", name=label_text)
    box = slider.bounding_box()
    if box:
        x = box["x"] + box["width"] * (int(value) / 5)
        y = box["y"] + box["height"] / 2
        page.mouse.click(x, y)
        page.wait_for_timeout(500)


class TestAppFlows:
    def test_page_loads(self, page):
        wait_for_app_ready(page)
        assert "Orçamento" in page.content()

    def test_form_rendering(self, page):
        wait_for_app_ready(page)
        assert page.get_by_text("Dados do Imóvel").is_visible()
        assert page.get_by_text("Dados do Locatário").is_visible()
        assert page.get_by_text("Parcelamento do Contrato").is_visible()

    def test_apartamento_flow_no_filhos_no_parcelar(self, page):
        wait_for_app_ready(page)
        select_combobox_option(page, "Tipo de Imóvel", "CASA")
        page.get_by_label("Endereço").fill("Rua B, 200")
        page.get_by_label("Vagas de Garagem").fill("1")
        page.get_by_label("Nome do Locatário").fill("Carlos")
        page.get_by_role("button", name="Gerar Orçamento").click()
        page.wait_for_selector("text=Resumo do Orçamento", timeout=15000)
        assert page.get_by_text("CASA").is_visible()
        assert page.get_by_text("Rua B, 200").is_visible()
        assert page.get_by_text("Carlos").is_visible()
        assert page.get_by_text("Total Mensal").is_visible()

    def test_apartamento_flow_com_filhos_sem_parcelar(self, page):
        page.reload()
        wait_for_app_ready(page)
        select_combobox_option(page, "Tipo de Imóvel", "APARTAMENTO")
        page.get_by_label("Endereço").fill("Rua A, 100")
        page.get_by_label("Nome do Locatário").fill("Maria")
        check_checkbox(page, "Possui filhos?")
        page.get_by_role("button", name="Gerar Orçamento").click()
        page.wait_for_selector("text=Resumo do Orçamento", timeout=15000)
        assert page.get_by_text("APARTAMENTO").is_visible()
        assert page.get_by_text("Maria").is_visible()

    def test_casa_flow_com_garagem(self, page):
        page.reload()
        wait_for_app_ready(page)
        select_combobox_option(page, "Tipo de Imóvel", "CASA")
        page.get_by_label("Endereço").fill("Rua B, 200")
        page.get_by_label("Vagas de Garagem").fill("2")
        page.get_by_label("Nome do Locatário").fill("Carlos")
        page.get_by_role("button", name="Gerar Orçamento").click()
        page.wait_for_selector("text=Resumo do Orçamento", timeout=15000)
        assert page.get_by_text("CASA").is_visible()
        assert page.get_by_text("Rua B, 200").is_visible()

    def test_estudio_flow(self, page):
        page.reload()
        wait_for_app_ready(page)
        select_combobox_option(page, "Tipo de Imóvel", "ESTUDIO")
        page.get_by_label("Endereço").fill("Rua C, 300")
        page.get_by_label("Vagas de Garagem").fill("2")
        page.get_by_label("Nome do Locatário").fill("Ana")
        page.get_by_role("button", name="Gerar Orçamento").click()
        page.wait_for_selector("text=Resumo do Orçamento", timeout=15000)
        assert page.get_by_text("ESTUDIO").is_visible()
        assert page.get_by_text("Ana").is_visible()

    def test_parcelar_flow(self, page):
        page.reload()
        wait_for_app_ready(page)
        select_combobox_option(page, "Tipo de Imóvel", "APARTAMENTO")
        page.get_by_label("Endereço").fill("Rua A, 100")
        page.get_by_label("Nome do Locatário").fill("Joao")
        check_checkbox(page, "Parcelar taxa de contrato (R$ 2.000,00)")
        set_slider(page, "Número de parcelas (máx. 5)", "2")
        page.get_by_role("button", name="Gerar Orçamento").click()
        page.wait_for_selector("text=Resumo do Orçamento", timeout=20000)
        page.wait_for_timeout(2000)
        assert page.get_by_text("Parcela do Contrato").is_visible()
        assert page.get_by_text("12 Parcelas do Orçamento").is_visible()

    def test_empty_fields_shows_error(self, page):
        page.reload()
        wait_for_app_ready(page)
        page.get_by_role("button", name="Gerar Orçamento").click()
        page.wait_for_selector("text=Preencha o endereço", timeout=15000)
        assert page.get_by_text("Preencha o endereço").is_visible()

    def test_csv_export_message(self, page):
        wait_for_app_ready(page)
        select_combobox_option(page, "Tipo de Imóvel", "APARTAMENTO")
        page.get_by_label("Endereço").fill("Rua A, 100")
        page.get_by_label("Nome do Locatário").fill("Joao")
        page.get_by_role("button", name="Gerar Orçamento").click()
        page.wait_for_selector("text=Arquivo CSV exportado", timeout=15000)
        assert page.get_by_text("Arquivo CSV exportado").is_visible()