"""Mantém igual, nas páginas, o trecho que elas repetem: o WhatsApp flutuante e o formulário do Raio-X.

A fonte é o index.html. Copia o bloco entre <!-- comum:fim-da-pagina:inicio ... -->
e <!-- comum:fim-da-pagina:fim --> para as outras páginas.

Uso: python scripts/comum.py [--conferir]
Com --conferir não escreve nada: sai com erro se alguma página divergir (é o que
tests/test_medicos.py roda).
"""
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

RAIZ = pathlib.Path(__file__).resolve().parents[1]
FONTE = "index.html"
PAGINAS = ["medicos.html"]
BLOCO = re.compile(r"<!-- comum:fim-da-pagina:inicio.*?<!-- comum:fim-da-pagina:fim -->", re.S)


def ler(nome):
    bruto = (RAIZ / nome).read_bytes().decode("utf-8")
    return bruto.replace("\r\n", "\n"), "\r\n" in bruto


fonte, _ = ler(FONTE)
achados = BLOCO.findall(fonte)
if len(achados) != 1:
    sys.exit(f"{FONTE}: bloco comum não encontrado, ou repetido")
bloco = achados[0]

conferir = "--conferir" in sys.argv
diverge = False
for nome in PAGINAS:
    pagina, crlf = ler(nome)
    if len(BLOCO.findall(pagina)) != 1:
        sys.exit(f"{nome}: bloco comum não encontrado, ou repetido")
    novo = BLOCO.sub(lambda m: bloco, pagina)
    if conferir:
        if novo != pagina:
            print(f"{nome}: o bloco comum difere do {FONTE}; rode python scripts/comum.py")
            diverge = True
        else:
            print(f"{nome}: bloco comum igual ao do {FONTE}")
    else:
        (RAIZ / nome).write_bytes((novo.replace("\n", "\r\n") if crlf else novo).encode("utf-8"))
        print(f"{nome}: bloco comum copiado do {FONTE}")

sys.exit(1 if diverge else 0)
