"""Gera o FAQPage do JSON-LD a partir das <details> de uma página.

O Google exige que o texto do schema seja o texto visível da página. Escrito à
mão, os dois divergem na primeira edição; gerado daqui, não divergem nunca.

Uso: python scripts/faq_schema.py [pagina.html] [--conferir]
Sem página, usa o index.html. Reescreve o bloco entre <!-- faq-schema:inicio -->
e <!-- faq-schema:fim -->. Com --conferir não escreve nada: sai com erro se o
bloco não bate com as perguntas da página (é o que tests/test_guardas.py roda).
"""
import html
import json
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

args = [a for a in sys.argv[1:] if not a.startswith("--")]
conferir = "--conferir" in sys.argv
PAGINA = pathlib.Path(__file__).resolve().parents[1] / (args[0] if args else "index.html")
bruto = PAGINA.read_bytes().decode("utf-8")
crlf = "\r\n" in bruto
pagina = bruto.replace("\r\n", "\n")

inicio = pagina.index('<div class="o-faq')
itens = re.findall(r"<summary>(.*?)</summary>\s*<div class=\"o-faq__r\">(.*?)</div>", pagina[inicio:], re.S)
if not itens:
    sys.exit(f"{PAGINA.name}: nenhuma <details> encontrada no .o-faq")


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
                  lambda m: m.group(1) + "\n" + bloco + "\n" + m.group(2), pagina, flags=re.S)
if n != 1:
    sys.exit(f"{PAGINA.name}: marcadores do faq-schema não encontrados (ou repetidos)")

if conferir:
    if novo != pagina:
        sys.exit(f"{PAGINA.name}: o FAQPage não bate com as perguntas; rode python scripts/faq_schema.py {PAGINA.name}")
    print(f"{PAGINA.name}: FAQPage em dia, {len(itens)} perguntas")
else:
    PAGINA.write_bytes((novo.replace("\n", "\r\n") if crlf else novo).encode("utf-8"))
    print(f"{PAGINA.name}: {len(itens)} perguntas no FAQPage")
