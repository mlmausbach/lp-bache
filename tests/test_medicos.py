"""Doc 11 §06: a /medicos conta o processo do especialista, sem orçamento. O Marco 1 só aparece na
pergunta de garantia (doc 12 §7): 16-OFERTAS:67 o dá à Marca Pessoal."""
import subprocess
import sys
import unittest

from pagina import RAIZ, ler, por_classe, por_id, texto, todos


def limpo(t):
    return t.replace("\xa0", " ")


class Medicos(unittest.TestCase):
    def setUp(self):
        self.doc = ler("medicos.html")
        self.corpo = next(todos(self.doc, lambda n: n.tag == "body"))

    def secoes(self):
        main = next(todos(self.doc, lambda n: n.tag == "main"))
        return [s.attrs.get("id") for s in main.filhos if not isinstance(s, str) and s.tag == "section"]

    def test_o_formulario_abre_no_caminho_do_medico(self):
        self.assertEqual(self.corpo.attrs.get("data-caminho"), "med")

    def test_a_capa(self):
        capa = por_classe(self.doc, "l-capa")[0]
        t = texto(capa)
        self.assertIn("Para médicos especialistas de alto ticket", t)
        self.assertIn("Pare de ser comparado por preço e perder pacientes pra médicos menos competentes.", t)
        self.assertIn("A Bäche lê o negócio antes de qualquer peça, dos concorrentes aos indicadores, "
                      "e responde pelo marketing inteiro, do preço ao anúncio.", t)
        portas = [a for a in todos(capa, lambda n: n.tag == "a") if a.attrs.get("href") == "/"]
        self.assertEqual(len(portas), 1)
        self.assertIn("Tenho uma clínica", texto(portas[0]))

    def test_a_ordem_sem_o_marco_1(self):
        self.assertEqual(self.secoes(), [None, "para-quem", "tensao", "leituras", "como-funciona", "instalado",
                                         "quem-somos", "perguntas", "raio-x"])

    def test_nenhum_orcamento_no_que_o_medico_le(self):
        self.assertNotIn("orçament", texto(self.corpo, "med").lower())

    def test_o_marco_1_so_na_pergunta_de_garantia_e_sem_dia_30(self):
        # A decisão 7 do doc 11 deixou o Marco 1 de fora "enquanto o 16-OFERTAS só o escreve para a clínica".
        # A linha 67 do 16-OFERTAS o escreve também para a Marca Pessoal (paga só o E1), então a página o define.
        faq = por_classe(self.doc, "o-faq")[0]
        resposta = next(texto(d) for d in todos(faq, lambda n: n.tag == "details") if "garantem" in texto(d))
        self.assertIn("O Marco 1 é a sua decisão na entrega do Diagnóstico", resposta)
        self.assertIn("paga só o Diagnóstico", resposta)
        t = texto(self.corpo, "med")
        self.assertEqual(t.count("Marco 1"), resposta.count("Marco 1"))
        self.assertNotIn("dia 30", t.lower())

    def test_a_linha_do_tempo_do_medico(self):
        como = por_id(self.doc, "como-funciona")
        faixas = [texto(n) for n in por_classe(como, "o-linha__faixa")]
        self.assertEqual(faixas, ["Instalação 4E · Marca Pessoal · 7 semanas · valor na proposta"])
        t = texto(como)
        for parte in ("E1 Diagnóstico", "E2 Estratégia", "E3 Estrutura", "Google Ads no ar", "14 dias de ajuste"):
            self.assertIn(parte, t)
        self.assertNotIn("R$", limpo(t))
        self.assertEqual(len(por_classe(como, "o-exemplo")), 2)
        self.assertEqual(por_classe(como, "o-mes"), [])

    def test_o_que_fica_instalado(self):
        inst = por_id(self.doc, "instalado")
        itens = [texto(li) for li in todos(por_classe(inst, "o-instalado")[0], lambda n: n.tag == "li")]
        self.assertEqual(itens, ["Posicionamento", "Brand Book", "Landing page", "Google Ads no ar"])
        self.assertIn("Bônus: treino de gravação (1 mês) e roteirista de IA.", texto(inst))

    def test_as_sete_perguntas(self):
        perguntas = [texto(s) for s in todos(por_id(self.doc, "perguntas"), lambda n: n.tag == "summary")]
        self.assertEqual(len(perguntas), 7)
        self.assertNotIn("Vou precisar gravar vídeo e aparecer?", perguntas)

    def test_o_bloco_comum_igual_ao_da_home(self):
        r = subprocess.run([sys.executable, str(RAIZ / "scripts" / "comum.py"), "--conferir"],
                           capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_o_servico_do_json_ld_usa_a_categoria(self):
        # §01.2 e §09: a categoria é uma só, e o serviceType do schema não a parafraseia
        for pagina in ("index.html", "medicos.html"):
            html = (RAIZ / pagina).read_text(encoding="utf-8")
            self.assertIn('"serviceType": "Assessoria de Engenharia de Marketing para Saúde"', html, pagina)

    def test_a_pagina_esta_no_sitemap(self):
        self.assertIn("<loc>https://bache.com.br/medicos</loc>", (RAIZ / "sitemap.xml").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
