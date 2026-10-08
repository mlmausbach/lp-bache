"""Mantém igual, nas páginas, os trechos que elas repetem.

Dois blocos, os dois com a fonte no index.html:
  fim-da-pagina  o WhatsApp flutuante e o formulário do Raio-X (home e /medicos)
  cookies        o aviso de cookies e o painel de preferências (home, /medicos e /privacidade)

Copia o que está entre <!-- comum:NOME:inicio ... --> e <!-- comum:NOME:fim --> do index.html
para as outras páginas.

Uso: python scripts/comum.py [--conferir]
Com --conferir não escreve nada: sai com erro se alguma página divergir (é o que
tests/test_medicos.py e tests/test_cookies.py rodam).
"""
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

RAIZ = pathlib.Path(__file__).resolve().parents[1]
FONTE = "index.html"
BLOCOS = {
    "fim-da-pagina": ["medicos.html"],
    "cookies": ["medicos.html", "privacidade.html"],
}


def ler(nome):
    bruto = (RAIZ / nome).read_bytes().decode("utf-8")
    return bruto.replace("\r\n", "\n"), "\r\n" in bruto


def padrao(nome):
    return re.compile(rf"<!-- comum:{re.escape(nome)}:inicio.*?<!-- comum:{re.escape(nome)}:fim -->", re.S)


conferir = "--conferir" in sys.argv
fonte, _ = ler(FONTE)
paginas = {}
diverge = False
for bloco, destinos in BLOCOS.items():
    rx = padrao(bloco)
    achados = rx.findall(fonte)
    if len(achados) != 1:
        sys.exit(f"{FONTE}: bloco comum '{bloco}' não encontrado, ou repetido")
    for nome in destinos:
        if nome not in paginas:
            paginas[nome] = ler(nome)
        texto, crlf = paginas[nome]
        if len(rx.findall(texto)) != 1:
            sys.exit(f"{nome}: bloco comum '{bloco}' não encontrado, ou repetido")
        novo = rx.sub(lambda m: achados[0], texto)
        if conferir:
            if novo != texto:
                print(f"{nome}: o bloco '{bloco}' difere do {FONTE}; rode python scripts/comum.py")
                diverge = True
            else:
                print(f"{nome}: bloco '{bloco}' igual ao do {FONTE}")
        else:
            paginas[nome] = (novo, crlf)
            print(f"{nome}: bloco '{bloco}' copiado do {FONTE}")

if not conferir:
    for nome, (texto, crlf) in paginas.items():
        (RAIZ / nome).write_bytes((texto.replace("\n", "\r\n") if crlf else texto).encode("utf-8"))

sys.exit(1 if diverge else 0)
