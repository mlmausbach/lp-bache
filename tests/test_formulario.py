"""O formulário do Raio-X (doc 11, decisões 11 e 12): o médico responde o
faturamento do consultório e não lê "orçamento" em nenhuma etapa."""
import unittest

from pagina import ler, por_id, texto, todos


class Formulario(unittest.TestCase):
    def setUp(self):
        self.dlg = por_id(ler("index.html"), "raio-x-form")

    def grupo(self, nome):
        return next(todos(self.dlg, lambda n: n.attrs.get("data-grupo") == nome), None)

    def test_a_faixa_de_faturamento_vale_para_os_dois_caminhos(self):
        campo = self.grupo("fat").pai
        self.assertIsNone(campo.attrs.get("data-so"))
        self.assertIn("Faturamento do consultório por mês", texto(campo, "med"))
        self.assertIn("Faturamento da clínica por mês", texto(campo, "cli"))

    def test_nao_existe_mais_o_grupo_de_orcamentos(self):
        self.assertIsNone(self.grupo("orc"))

    def test_o_caminho_do_medico_nao_tem_orcamento(self):
        self.assertNotIn("orçament", texto(self.dlg, "med").lower())

    def test_a_clinica_mantem_o_orcamento_no_gargalo(self):
        self.assertIn("O orçamento sai e não fecha", texto(self.grupo("gar"), "cli"))


if __name__ == "__main__":
    unittest.main()
