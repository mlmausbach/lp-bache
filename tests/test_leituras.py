"""Doc 11, §04, seções 03 e 04: a tensão numa seção só, e as duas leituras."""
import unittest

from pagina import ler, por_classe, por_id, texto, todos


class Leituras(unittest.TestCase):
    def setUp(self):
        self.doc = ler("index.html")

    def secoes(self):
        main = next(todos(self.doc, lambda n: n.tag == "main"))
        return [s.attrs.get("id") for s in main.filhos if not isinstance(s, str) and s.tag == "section"]

    def test_a_ordem_depois_da_capa(self):
        self.assertEqual(self.secoes()[1:4], ["para-quem", "tensao", "leituras"])
        self.assertNotIn("improviso", self.secoes())

    def test_a_tensao_junta_a_cena_e_o_improviso(self):
        t = texto(por_id(self.doc, "tensao"))
        self.assertIn("A clínica pede post porque é a parte do marketing que dá para ver.", t)
        self.assertIn("Ela atende bem, e mesmo assim o caixa oscila", t)
        self.assertIn("O marketing roda no improviso.", t)
        self.assertIn("Toda clínica tem um responsável pelo prontuário", t)
        self.assertNotIn("Só que o marketing tem três funções", t)

    def test_o_titulo_e_o_corpo_das_duas_leituras(self):
        t = texto(por_id(self.doc, "leituras"))
        self.assertIn("Rede social, site e anúncio são uma parte do diagnóstico.", t)
        self.assertIn("Só que o marketing tem três funções", t)
        self.assertNotIn("agência", t.lower())

    def test_a_leitura_de_canal_mora_dentro_de_comunicar_valor(self):
        canal = por_classe(por_id(self.doc, "leituras"), "o-leituras__canal")
        self.assertEqual(len(canal), 1)
        li = canal[0].pai
        self.assertEqual(li.tag, "li")
        self.assertIn("Comunicar valor", texto(li))
        self.assertIn("rede social · site · anúncio", texto(canal[0]))
        self.assertIn("o-leituras", li.pai.pai.classes())

    def test_as_duas_saidas(self):
        t = texto(por_classe(por_id(self.doc, "leituras"), "o-saidas")[0])
        self.assertIn("ajustar post e anúncio.", t)
        self.assertIn("posicionamento diferente dos concorrentes, Brand Book com território, CRM com indicadores, "
                      "e aí conteúdo e anúncio, com narrativa clara.", t)


if __name__ == "__main__":
    unittest.main()
