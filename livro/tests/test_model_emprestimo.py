from django.test import TestCase
from livro.models import Usuario, Livros, Emprestimos, Categoria
from django.urls import reverse

class EmprestimosModelTest(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create(
            nome="testeuser",
            email="teste@teste.com",
            senha="teste123"
        )
        self.categoria = Categoria.objects.create(
            nome="Categoria Teste",
            descricao="Descrição Teste",
            usuario=self.usuario
        )
        self.livro = Livros.objects.create(
            nome="Livro Teste",
            autor="Autor Teste",
            categoria=self.categoria,
            usuario=self.usuario,
            localizacao="Prateleira 1",
            exemplares_disponiveis="5",
            compositor="Compositor Teste",
            arranjador="Arranjador Teste",
            obra="Obra Teste",
            classificacao="Classificação Teste",
            conteudo="Conteúdo Teste",
            edicao="Edição Teste",
            observacao="Observação Teste",
            formato="Formato Teste",
            observacoes_gerais="Observações gerais Teste"
        )

    def test_url_cadastrar_emprestimo(self):
        response = self.client.get(reverse('cadastrar_emprestimo'))
        self.assertEqual(response.status_code, 200)  # Verifica se a URL retorna 200 OK

    def test_cadastrar_emprestimo_com_usuario_identificado(self):
        response = self.client.post(reverse('cadastrar_emprestimo'), {
            'nome_emprestado': self.usuario.id,
            'livro_emprestado': self.livro.id,
            'nome_emprestado_anonimo': '',
        })
        self.assertRedirects(response, '/livro/home')
        emprestimo = Emprestimos.objects.get(livro_id=self.livro.id)
        self.assertIsNotNone(emprestimo)
        self.assertEqual(emprestimo.nome_emprestado_id, self.usuario.id)
        self.livro.refresh_from_db()
        self.assertTrue(self.livro.emprestado)

    def test_cadastrar_emprestimo_com_usuario_anônimo(self):
        response = self.client.post(reverse('cadastrar_emprestimo'), {
            'nome_emprestado': '',
            'livro_emprestado': self.livro.id,
            'nome_emprestado_anonimo': 'Usuário Anônimo',
        })
        self.assertRedirects(response, '/livro/home')
        emprestimo = Emprestimos.objects.get(livro_id=self.livro.id)
        self.assertIsNotNone(emprestimo)
        self.assertEqual(emprestimo.nome_emprestado_anonimo, 'Usuário Anônimo')
        self.livro.refresh_from_db()
        self.assertTrue(self.livro.emprestado)

    def test_cadastrar_emprestimo_livro_indisponivel(self):
        self.livro.emprestado = True
        self.livro.save()
        response = self.client.post(reverse('cadastrar_emprestimo'), {
            'nome_emprestado': self.usuario.id,
            'livro_emprestado': self.livro.id,
            'nome_emprestado_anonimo': '',
        })
        self.assertRedirects(response, '/livro/home')
        emprestimos_count = Emprestimos.objects.filter(livro_id=self.livro.id).count()
        self.assertEqual(emprestimos_count, 1)
        self.livro.refresh_from_db()
        self.assertTrue(self.livro.emprestado)
