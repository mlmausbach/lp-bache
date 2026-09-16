"""Doc 11, §04, seções 01 e 02: quem entra entende para quem é e o que a Bäche faz na capa."""
import unittest

from pagina import ler, por_classe, por_id, texto, todos


def limpo(t):
    return t.replace("\xa0", " ")


class Capa(unittest.TestCase):
    def setUp(self):
        self.doc = ler("index.html")
        self.capa = por_classe(self.doc, "l-capa")[0]

    def test_o_olho_diz_para_quem_com_o_piso(self):
        self.assertIn("Para clínicas acima de R$ 50 mil por mês", limpo(texto(self.capa)))

    def test_a_linha_do_que_a_bache_faz(self):
        self.assertIn("A Bäche lê o negócio antes de qualquer peça, dos concorrentes aos indicadores, "
                      "e responde pelo marketing inteiro, do preço ao anúncio.", texto(self.capa))

    def test_a_porta_do_medico(self):
        portas = [a for a in todos(self.capa, lambda n: n.tag == "a") if a.attrs.get("href") == "/medicos"]
        self.assertEqual(len(portas), 1)
        self.assertIn("Sou médico especialista", texto(portas[0]))

    def test_o_menu(self):
        nav = por_classe(self.doc, "l-nav")[0]
        itens = [(a.attrs["href"], texto(a)) for a in todos(nav, lambda n: n.tag == "a") if "btn" not in n_classes(a)]
        self.assertEqual(itens, [("#como-funciona", "Como funciona"), ("#marco-1", "Marco 1"),
                                 ("#quem-somos", "Quem somos"), ("/medicos", "Para médicos")])

    def test_para_quem_e_vem_logo_depois_da_capa(self):
        main = next(todos(self.doc, lambda n: n.tag == "main"))
        secoes = [s.attrs.get("id") for s in main.filhos if not isinstance(s, str) and s.tag == "section"]
        self.assertIsNone(secoes[0])  # a capa
        self.assertEqual(secoes[1], "para-quem")

    def test_para_quem_e_sem_o_medico_e_sem_o_corte_final(self):
        t = texto(por_id(self.doc, "para-quem"))
        self.assertNotIn("Especialistas de alto ticket", t)
        self.assertNotIn("Quem não é cliente", t)

    def test_quem_nao_e_cliente_fica_no_fecho(self):
        self.assertIn("Quem não é cliente", texto(por_id(self.doc, "raio-x")))


def n_classes(no):
    return no.classes()


if __name__ == "__main__":
    unittest.main()
