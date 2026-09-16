"""Leitura das páginas para os testes, sem dependência: uma árvore simples com html.parser."""
import html.parser
import pathlib
import re

RAIZ = pathlib.Path(__file__).resolve().parents[1]
VAZIOS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}


class No:
    def __init__(self, tag, attrs, pai):
        self.tag, self.attrs, self.pai, self.filhos = tag, dict(attrs), pai, []

    def classes(self):
        return (self.attrs.get("class") or "").split()


class _Montador(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.raiz = No("#doc", {}, None)
        self.atual = self.raiz

    def handle_starttag(self, tag, attrs):
        no = No(tag, attrs, self.atual)
        self.atual.filhos.append(no)
        if tag not in VAZIOS:
            self.atual = no

    def handle_startendtag(self, tag, attrs):
        self.atual.filhos.append(No(tag, attrs, self.atual))

    def handle_endtag(self, tag):
        n = self.atual
        while n is not None and n.tag != tag:
            n = n.pai
        if n is not None and n.pai is not None:
            self.atual = n.pai

    def handle_data(self, data):
        self.atual.filhos.append(data)


def ler(nome):
    m = _Montador()
    m.feed((RAIZ / nome).read_text(encoding="utf-8"))
    return m.raiz


def todos(no, pred):
    for f in no.filhos:
        if isinstance(f, No):
            if pred(f):
                yield f
            yield from todos(f, pred)


def por_id(no, id_):
    return next(todos(no, lambda n: n.attrs.get("id") == id_), None)


def por_classe(no, classe):
    return list(todos(no, lambda n: classe in n.classes()))


def texto(no, caminho=None):
    """Texto visível. Sem script, style e template. Com caminho ('cli' ou 'med'),
    pula o que tem data-so do outro caminho, como o formulário faz na tela."""
    partes = []

    def anda(n):
        for f in n.filhos:
            if isinstance(f, str):
                partes.append(f)
            elif f.tag in ("script", "style", "template", "noscript"):
                continue
            elif caminho and f.attrs.get("data-so") not in (None, caminho):
                continue
            else:
                partes.append(" ")
                anda(f)
                partes.append(" ")

    anda(no)
    return re.sub(r"\s+", " ", "".join(partes)).strip()
