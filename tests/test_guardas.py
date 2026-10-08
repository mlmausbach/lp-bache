"""As réguas que valem para toda página do site (doc 10 §01 e doc 11 §01).

1. Guardas da voz no texto visível (Brand Book §06.3).
2. Nenhuma cor solta no CSS da página: só tokens do DS v2.
3. Toda âncora interna leva a algum lugar.
4. O JSON-LD é JSON válido, e o FAQPage bate com as perguntas visíveis.
"""
import html
import json
import pathlib
import re
import subprocess
import sys
import unittest

from pagina import RAIZ, ler, texto, todos

PAGINAS = ["index.html", "medicos.html"]

GUARDAS = [r"—", r"–", r"\bnós\b", r"\bpremium\b", r"excelência", r"inovação", r"sob medida", r"solução completa",
           r"\bportanto\b", r"\bcontudo\b", r"\btodavia\b", r"\bademais\b", r"\bentretanto\b", r"dessa forma"]


# Murillo, 08/10/2026: nenhuma informação de pagamento no site, nem forma de pagamento nem valor.
# Fica de fora a faixa de faturamento da clínica (R$ 50 mil, 50 a 80 mil...), que é critério de quem se atende.
PAGAMENTO = [r"7\.900", r"crédito integral", r"pagament", r"\bpago por\b", r"\bpaga só\b", r"\bpagar\b",
             r"recebe de volta", r"parcela", r"\bpix\b", r"cart[ãa]o", r"\bentrada\b", r"valor na proposta",
             r"investimento", r"reembols", r"devolu", r"verba de mídia", r"mensalidade", r"\bfee\b", r"desconto"]


def texto_publico(nome):
    """O que o leitor e o buscador veem: texto da página, JSON-LD incluso, ou o llms.txt inteiro."""
    t = (RAIZ / nome).read_text(encoding="utf-8")
    if nome.endswith(".html"):
        t = re.sub(r"<style.*?</style>|<script(?![^>]*ld\+json).*?</script>", " ", t, flags=re.S)
        t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", html.unescape(t).replace("\xa0", " "))


class Guardas(unittest.TestCase):
    def test_o_site_nao_fala_de_pagamento(self):
        for nome in PAGINAS + ["llms.txt"]:
            t = texto_publico(nome)
            for g in PAGAMENTO:
                with self.subTest(pagina=nome, termo=g):
                    self.assertIsNone(re.search(g, t, re.I), re.search(g, t, re.I) and t[re.search(g, t, re.I).start() - 40:][:120])
            with self.subTest(pagina=nome, termo="R$ fora da faixa de faturamento"):
                faixas = re.findall(r"R\$\s?\d+(?:\s?a\s?\d+)?\s?mil", t)
                self.assertEqual(t.count("R$"), len(faixas))

    def test_guardas_da_voz(self):
        for nome in PAGINAS:
            corpo = next(todos(ler(nome), lambda n: n.tag == "body"))
            t = texto(corpo).lower()
            for g in GUARDAS:
                with self.subTest(pagina=nome, guarda=g):
                    self.assertIsNone(re.search(g, t))

    def test_toda_ancora_tem_destino(self):
        for nome in PAGINAS:
            doc = ler(nome)
            ids = {n.attrs["id"] for n in todos(doc, lambda n: "id" in n.attrs)}
            for a in todos(doc, lambda n: n.tag == "a" and n.attrs.get("href", "").startswith("#")):
                alvo = a.attrs["href"][1:]
                if alvo:
                    with self.subTest(pagina=nome, ancora=alvo):
                        self.assertIn(alvo, ids)

    def test_json_ld_valido(self):
        for nome in PAGINAS:
            for s in todos(ler(nome), lambda n: n.tag == "script" and n.attrs.get("type") == "application/ld+json"):
                with self.subTest(pagina=nome):
                    json.loads("".join(f for f in s.filhos if isinstance(f, str)))

    def test_faq_schema_em_dia(self):
        for nome in PAGINAS:
            r = subprocess.run([sys.executable, str(RAIZ / "scripts" / "faq_schema.py"), nome, "--conferir"],
                               capture_output=True, text=True, encoding="utf-8")
            with self.subTest(pagina=nome):
                self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_css_da_pagina_sem_cor_solta(self):
        css = (RAIZ / "assets" / "css" / "site.css").read_text(encoding="utf-8")
        self.assertEqual(re.findall(r"#[0-9a-fA-F]{3,8}\b", css), [])
        self.assertNotIn("rgb(", css)

    def test_guardas_da_voz_no_description(self):
        for nome in PAGINAS:
            doc = ler(nome)
            metas = list(todos(doc, lambda n: n.tag == "meta" and (
                n.attrs.get("name") == "description" or n.attrs.get("property") == "og:description")))
            self.assertTrue(metas)
            for m in metas:
                t = (m.attrs.get("content") or "").lower()
                for g in GUARDAS:
                    with self.subTest(pagina=nome, meta=m.attrs.get("name") or m.attrs.get("property"), guarda=g):
                        self.assertIsNone(re.search(g, t))


if __name__ == "__main__":
    unittest.main()
