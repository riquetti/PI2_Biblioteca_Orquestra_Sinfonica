from django.urls import reverse
from django.test import TestCase
from usuarios.models import Usuario
from ..models import Categoria

class CategoriaModelTest(TestCase):

    def setUp(self):
        # Cria um usuário para testar
        self.usuario = Usuario(username='testuser')
        self.usuario.set_password('testpass')  # Definindo a senha corretamente
        self.usuario.save()  # Salva o usuário no banco de dados

    def test_cadastrar_categoria_com_dados_validos(self):
        self.client.session['usuario'] = self.usuario.id  # Simula o usuário logado
        response = self.client.post(reverse('cadastrar_categoria'), {
            'nome': 'Categoria Teste',
            'descricao': 'Descrição da categoria de teste',
            'usuario': self.usuario.id,
        })
        
        # Verifica se o redirecionamento ocorreu corretamente
        self.assertRedirects(response, '/livro/home?cadastro_categoria=1')

        # Verifica se a categoria foi criada
        categoria = Categoria.objects.get(nome='Categoria Teste')
        self.assertEqual(categoria.descricao, 'Descrição da categoria de teste')
        self.assertEqual(categoria.usuario, self.usuario)

    def test_cadastrar_categoria_usuario_incorreto(self):
        self.client.session['usuario'] = self.usuario.id  # Simula o usuário logado
        response = self.client.post(reverse('cadastrar_categoria'), {
            'nome': 'Categoria Teste',
            'descricao': 'Descrição da categoria de teste',
            'usuario': 999,  # ID de usuário inválido
        })

        # Verifica se a resposta é 200 OK e se a categoria não foi criada
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Não foi desta vez.')  # Verifica a mensagem de erro
        self.assertFalse(Categoria.objects.filter(nome='Categoria Teste').exists())

    def test_cadastrar_categoria_sem_usuario_logado(self):
        response = self.client.post(reverse('cadastrar_categoria'), {
            'nome': 'Categoria Teste',
            'descricao': 'Descrição da categoria de teste',
            'usuario': self.usuario.id,
        })

        # Verifica se a resposta é redirecionada para login
        self.assertRedirects(response, '/auth/login/?status=2')
        self.assertFalse(Categoria.objects.filter(nome='Categoria Teste').exists())

    def test_cadastrar_categoria_usuario_sem_sessao(self):
        # Simula a tentativa de cadastro sem usuário na sessão
        response = self.client.post(reverse('cadastrar_categoria'), {
            'nome': 'Categoria Teste',
            'descricao': 'Descrição da categoria de teste',
            'usuario': self.usuario.id,
        })

        # Verifica se a resposta é redirecionada para a página de login
        self.assertRedirects(response, '/auth/login/?status=2')
        self.assertFalse(Categoria.objects.filter(nome='Categoria Teste').exists())
