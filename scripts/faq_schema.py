"""Gera o FAQPage do JSON-LD a partir das <details> do index.html.

O Google exige que o texto do schema seja o texto visível da página. Escrito à
mão, os dois divergem na primeira edição; gerado daqui, não divergem nunca.

Uso: python scripts/faq_schema.py
Reescreve o bloco entre <!-- faq-schema:inicio --> e <!-- faq-schema:fim -->.
"""
import html
import json
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

PAGINA = pathlib.Path(__file__).resolve().parents[1] / "index.html"
bruto = PAGINA.read_bytes().decode("utf-8")

inicio = bruto.index('<div class="o-faq')
itens = re.findall(r"<summary>(.*?)</summary>\s*<div class=\"o-faq__r\">(.*?)</div>", bruto[inicio:], re.S)
if not itens:
    sys.exit("nenhuma <details> encontrada no .o-faq")


def limpa(t):
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", t))).strip()


dados = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
        {"@type": "Question", "name": limpa(q),
         "acceptedAnswer": {"@type": "Answer", "text": limpa(a)}}
        for q, a in itens
    ],
}
bloco = ('<script type="application/ld+json">\n'
         + json.dumps(dados, ensure_ascii=False, indent=2)
         + "\n</script>")

novo, n = re.subn(r"(<!-- faq-schema:inicio -->).*?(<!-- faq-schema:fim -->)",
                  lambda m: m.group(1) + "\n" + bloco + "\n" + m.group(2), bruto, flags=re.S)
if n != 1:
    sys.exit("marcadores do faq-schema não encontrados (ou repetidos)")

PAGINA.write_bytes(novo.encode("utf-8"))
print(f"{len(itens)} perguntas no FAQPage")
