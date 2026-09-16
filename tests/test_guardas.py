"""As réguas que valem para toda página do site (doc 10 §01 e doc 11 §01).

1. Guardas da voz no texto visível (Brand Book §06.3).
2. Nenhuma cor solta no CSS da página: só tokens do DS v2.
3. Toda âncora interna leva a algum lugar.
4. O JSON-LD é JSON válido, e o FAQPage bate com as perguntas visíveis.
"""
import json
import pathlib
import re
import subprocess
import sys
import unittest

from pagina import RAIZ, ler, texto, todos

PAGINAS = ["index.html"]

GUARDAS = [r"—", r"\bnós\b", r"\bpremium\b", r"excelência", r"inovação", r"sob medida", r"solução completa",
           r"\bportanto\b", r"\bcontudo\b", r"\btodavia\b", r"\bademais\b", r"\bentretanto\b", r"dessa forma"]


class Guardas(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
