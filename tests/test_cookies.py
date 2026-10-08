"""Doc 12 §8: banner de cookies no padrão da LGPD e do guia da ANPD, e a política que ele aponta.

1. Estatística nasce desligada, e recusar custa o mesmo que aceitar. Só pede consentimento para o que o site usa:
   o container do GTM tem só o GA4 (conferido em 08/10/2026), então não há categoria Marketing.
2. O Google Tag Manager não está escrito no HTML: só o consent.js o carrega, depois da escolha.
3. A política diz quem trata o dado, por quê, com quem divide, por quanto tempo e como pedir a exclusão.
"""
import re
import subprocess
import sys
import unittest

from pagina import RAIZ, ler, por_classe, por_id, texto, todos
from test_guardas import GUARDAS

PAGINAS = ["index.html", "medicos.html", "privacidade.html"]


def botoes(no):
    return {b.attrs.get("data-cookies"): b for b in todos(no, lambda n: n.tag == "button" and "data-cookies" in n.attrs)}


class Banner(unittest.TestCase):
    def test_o_banner_nasce_escondido_e_tem_tres_botoes_iguais(self):
        for nome in PAGINAS:
            with self.subTest(pagina=nome):
                doc = ler(nome)
                banner = por_id(doc, "cookies")
                self.assertIsNotNone(banner, "falta o aviso de cookies")
                self.assertIn("hidden", banner.attrs)
                self.assertEqual(banner.attrs.get("role"), "region")
                b = botoes(banner)
                self.assertEqual(sorted(b), ["aceitar", "personalizar", "recusar"])
                # Recusar custa o mesmo que aceitar: mesmo elemento, mesmo tamanho (a classe-base é a mesma)
                self.assertEqual(b["aceitar"].tag, b["recusar"].tag)
                self.assertTrue(set(b["aceitar"].classes()) & set(b["recusar"].classes()) >= {"o-ck__b"})
                self.assertEqual(texto(b["aceitar"]).strip(), "Aceitar todos")
                self.assertEqual(texto(b["recusar"]).strip(), "Recusar todos")
                self.assertEqual(texto(b["personalizar"]).strip(), "Personalizar")

    def test_o_banner_aponta_para_a_politica(self):
        for nome in PAGINAS:
            with self.subTest(pagina=nome):
                banner = por_id(ler(nome), "cookies")
                links = [a.attrs.get("href") for a in todos(banner, lambda n: n.tag == "a")]
                self.assertIn("/privacidade", links)

    def test_estatistica_nasce_desligada_e_nao_ha_categoria_sem_uso(self):
        for nome in PAGINAS:
            with self.subTest(pagina=nome):
                dlg = por_id(ler(nome), "cookies-prefs")
                self.assertIsNotNone(dlg, "falta o painel de preferências")
                self.assertEqual(dlg.tag, "dialog")
                caixas = {c.attrs.get("id"): c for c in todos(dlg, lambda n: n.tag == "input" and n.attrs.get("type") == "checkbox")}
                # Marketing volta quando entrar uma tag de anúncio: caixa, linha na política e teste novo
                self.assertEqual(sorted(caixas), ["ck-estatisticas", "ck-necessarios"])
                self.assertNotIn("checked", caixas["ck-estatisticas"].attrs)
                self.assertIn("checked", caixas["ck-necessarios"].attrs)
                self.assertIn("disabled", caixas["ck-necessarios"].attrs)
                self.assertEqual(sorted(botoes(dlg)), ["aceitar", "fechar", "recusar", "salvar"])

    def test_o_rodape_reabre_as_preferencias(self):
        for nome in PAGINAS:
            with self.subTest(pagina=nome):
                rodape = next(todos(ler(nome), lambda n: n.tag == "footer"))
                hrefs = [a.attrs.get("href") for a in todos(rodape, lambda n: n.tag == "a")]
                self.assertIn("/privacidade", hrefs)
                abre = list(todos(rodape, lambda n: n.tag == "button" and "data-cookies-abrir" in n.attrs))
                self.assertEqual(len(abre), 1)
                self.assertEqual(texto(abre[0]).strip(), "Preferências de cookies")

    def test_o_gtm_nao_esta_escrito_no_html(self):
        for nome in PAGINAS:
            with self.subTest(pagina=nome):
                html = (RAIZ / nome).read_text(encoding="utf-8")
                self.assertNotIn("googletagmanager.com", html)
                self.assertNotIn("GTM-P7VS3KVG", html)

    def test_so_o_consent_js_carrega_o_gtm(self):
        js = (RAIZ / "assets" / "js" / "consent.js").read_text(encoding="utf-8")
        self.assertIn("https://www.googletagmanager.com/gtm.js?id=", js)
        self.assertIn("GTM-P7VS3KVG", js)
        self.assertNotRegex(js, r"connect\.facebook\.net|fbq\(|hotjar|clarity\.ms")
        for nome in ("site.js", "fit.js"):
            outro = (RAIZ / "assets" / "js" / nome).read_text(encoding="utf-8")
            self.assertNotIn("googletagmanager", outro, nome)

    def test_o_consent_js_vem_antes_do_site_js(self):
        for nome in ("index.html", "medicos.html"):
            with self.subTest(pagina=nome):
                html = (RAIZ / nome).read_text(encoding="utf-8")
                self.assertLess(html.index("/assets/js/consent.js"), html.index("/assets/js/site.js"))
        html = (RAIZ / "privacidade.html").read_text(encoding="utf-8")
        self.assertIn("/assets/js/consent.js", html)

    def test_o_aviso_do_formulario_aponta_para_a_politica(self):
        for nome in ("index.html", "medicos.html"):
            with self.subTest(pagina=nome):
                aviso = por_classe(ler(nome), "o-lgpd")[0]
                links = [a.attrs.get("href") for a in todos(aviso, lambda n: n.tag == "a")]
                self.assertEqual(links, ["/privacidade"])

    def test_os_blocos_comuns_batem(self):
        r = subprocess.run([sys.executable, str(RAIZ / "scripts" / "comum.py"), "--conferir"],
                           capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


class Politica(unittest.TestCase):
    def setUp(self):
        self.doc = ler("privacidade.html")
        self.t = texto(next(todos(self.doc, lambda n: n.tag == "main")))

    def test_a_politica_passa_nas_guardas_da_voz(self):
        corpo = texto(next(todos(self.doc, lambda n: n.tag == "body"))).lower()
        for g in GUARDAS:
            with self.subTest(guarda=g):
                self.assertIsNone(re.search(g, corpo))

    def test_a_pagina_esta_no_sitemap(self):
        self.assertIn("<loc>https://bache.com.br/privacidade</loc>", (RAIZ / "sitemap.xml").read_text(encoding="utf-8"))

    def test_tem_o_que_a_lgpd_manda_dizer(self):
        # LGPD art. 9º e art. 18: controlador, finalidade, compartilhamento, prazo, direitos e como exercê-los
        secoes = [por_id(self.doc, i) for i in ("controlador", "dados", "compartilhamento", "transferencia", "prazo", "direitos", "sobre-cookies")]
        self.assertNotIn(None, secoes)
        for termo in ("Cloudflare", "ClickUp", "Google", "WhatsApp", "base legal", "eliminação", "revogar"):
            self.assertIn(termo, self.t)

    def test_a_tabela_de_cookies_confere_com_o_banner(self):
        tabela = por_id(self.doc, "tabela-cookies")
        self.assertIsNotNone(tabela)
        t = texto(tabela)
        for nome in ("bache-cookies", "_ga", "_ga_ZLFQ717WHF"):
            self.assertIn(nome, t)
        self.assertNotIn("_gcl_", t)
        for cat in ("Necessários", "Estatísticas"):
            self.assertIn(cat, t)

    def test_a_politica_diz_o_que_o_google_recebe(self):
        # o container tem tag GA4 para whatsapp_click, abrir_modal_diagnostico e generate_lead (com o parametro fit)
        for trecho in ("cliques no WhatsApp", "quente, morno ou frio", "_ga_ZLFQ717WHF"):
            self.assertIn(trecho, self.t)
        painel = texto(por_id(ler("index.html"), "cookies-prefs"))
        for trecho in ("cliques no WhatsApp", "o Google recebe esses dados"):
            self.assertIn(trecho, painel)

    def test_a_politica_nao_fala_de_dinheiro(self):
        # doc 12 D24: o site não tem valor nem forma de pagamento
        self.assertIsNone(re.search(r"R\$|\bpix\b|parcela|crédito integral|pagamento por", self.t, re.I))

    def test_a_politica_nao_tem_dado_pendente(self):
        # Razão social, CNPJ, contato e prazo vêm do Murillo. Enquanto houver [PENDENTE ...] aqui, a página não vai ao ar.
        pendentes = re.findall(r"\[PENDENTE[^\]]*\]", (RAIZ / "privacidade.html").read_text(encoding="utf-8"))
        self.assertEqual(pendentes, [], "dados do controlador ainda por preencher: %s" % pendentes)


if __name__ == "__main__":
    unittest.main()
