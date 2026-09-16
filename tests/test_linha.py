"""Doc 11, §04 seções 05 e 06, §05 e §07: como funciona, num desenho só."""
import unittest

from pagina import RAIZ, ler, por_classe, por_id, texto, todos


def limpo(t):
    return t.replace("\xa0", " ")


def bloco_media(css, largura):
    """Conteúdo do bloco @media (max-width: <largura>px) { ... }, por contagem de chaves."""
    marca = f"@media (max-width: {largura}px) {{"
    i = css.index(marca)
    ini = i + len(marca)
    prof = 1
    j = ini
    while prof:
        if css[j] == "{":
            prof += 1
        elif css[j] == "}":
            prof -= 1
        j += 1
    return css[ini:j - 1]


class LinhaDoTempo(unittest.TestCase):
    def setUp(self):
        self.doc = ler("index.html")
        self.como = por_id(self.doc, "como-funciona")

    def secoes(self):
        main = next(todos(self.doc, lambda n: n.tag == "main"))
        return [s.attrs.get("id") for s in main.filhos if not isinstance(s, str) and s.tag == "section"]

    def test_a_ordem(self):
        self.assertEqual(self.secoes()[1:6], ["para-quem", "tensao", "leituras", "como-funciona", "instalado"])
        self.assertNotIn("metodo", self.secoes())
        self.assertNotIn("contratar", self.secoes())

    def test_os_cinco_marcos(self):
        quando = [texto(n) for n in por_classe(self.como, "o-marco__quando")]
        self.assertEqual(quando, ["Dia 0", "Dias 1 a 30", "Dias 30 a 60", "Dias 60 a 120", "12 meses"])
        t = texto(self.como)
        for fase in ("E1 Diagnóstico", "E2 Estratégia", "E3 Estrutura", "E4 Evolução"):
            self.assertIn(fase, t)
        self.assertIn("No dia 30, você decide se segue", t)

    def test_as_faixas(self):
        faixas = [texto(n) for n in por_classe(self.como, "o-linha__faixa")]
        self.assertEqual(faixas, ["Instalação 4E · cerca de 120 dias · valor na proposta · pagamento por entrega",
                                  "Evolução · 12 meses"])

    def test_o_primeiro_mes(self):
        mes = por_classe(self.como, "o-mes")[0]
        t = texto(mes)
        self.assertIn("Até três, escolhidas com você na primeira reunião. Todas reversíveis e sem verba de anúncio.", t)
        self.assertIn("No dia 30, cada uma vem com o número de antes e o de agora.", t)
        itens = [texto(li) for li in todos(por_classe(mes, "o-mes__lista")[0], lambda n: n.tag == "li")]
        self.assertEqual(len(itens), 6)
        self.assertNotIn("dia 5", t.lower())

    def test_os_tres_exemplos_rotulados_e_com_fonte(self):
        exemplos = por_classe(self.como, "o-exemplo")
        self.assertEqual(len(exemplos), 3)
        for e in exemplos:
            self.assertIn("Exemplo · dados fictícios", texto(e))
        diag = texto(exemplos[0])
        self.assertIn("MIT e InsideSales, 2007", diag)
        self.assertIn("Catalyst Index, 2026", diag)

    def test_sem_termo_interno(self):
        t = texto(self.como).lower()
        self.assertNotIn("4cs", t)
        self.assertNotIn("sete momentos", t)

    def test_o_diagnostico_avulso_e_a_capacidade(self):
        t = limpo(texto(self.como))
        self.assertIn("R$ 7.900, com crédito integral na Instalação se você seguir em até 30 dias", t)
        self.assertIn("A Bäche abre uma Instalação nova por mês", t)

    def test_o_que_fica_instalado(self):
        inst = por_id(self.doc, "instalado")
        itens = [texto(li) for li in todos(por_classe(inst, "o-instalado")[0], lambda n: n.tag == "li")]
        self.assertEqual(itens, ["Brand Book", "Site", "CRM com automações", "Painel de indicadores",
                                 "Roteiro e treino da recepção", "Primeira campanha publicada"])
        self.assertIn("Conteúdo e anúncio (Meta e Google) entram na Evolução completa.", texto(inst))

    def test_sairam_os_blocos_antigos(self):
        self.assertEqual(por_classe(self.doc, "l-afirmacoes"), [])
        titulos = [texto(h) for h in todos(self.doc, lambda n: n.tag == "h2")]
        self.assertNotIn("O tráfego entra por último.", titulos)


class LinhaDoTempoResponsiva(unittest.TestCase):
    """F1: a linha vertical entra no tablet (até 1100 px), não só no celular (até 900 px)."""

    REGRAS = [
        ".o-linha__faixas { display: flex; flex-direction: column; gap: 6px; }",
        ".o-linha__marcos { grid-template-columns: 1fr; margin-left: 6px; border-top: 0; "
        "border-left: 2px solid var(--texto); }",
        ".o-marco, .o-marco + .o-marco { padding: 0 0 30px 24px; box-shadow: none; }",
        ".o-marco::before { top: 3px; left: -7px; }",
    ]

    def test_regras_no_bloco_de_1100_e_fora_do_900(self):
        css = (RAIZ / "assets" / "css" / "site.css").read_text(encoding="utf-8")
        b1100 = bloco_media(css, 1100)
        b900 = bloco_media(css, 900)
        for regra in self.REGRAS:
            with self.subTest(regra=regra):
                self.assertIn(regra, b1100)
                self.assertNotIn(regra, b900)


if __name__ == "__main__":
    unittest.main()
