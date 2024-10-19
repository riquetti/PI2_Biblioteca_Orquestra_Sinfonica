from django.test import TestCase, Client
from django.urls import reverse
from hashlib import sha256
from usuarios.models import Usuario
from livro.models import Livros, Categoria  # Ajuste na importação
import re


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()

        # Criação do usuário sem create_user, apenas usando create e criptografando a senha
        senha_criptografada = sha256('12345'.encode()).hexdigest()
        self.usuario = Usuario.objects.create(
            nome='Test User',
            email='test@example.com',
            senha=senha_criptografada,
            ativo=True
        )

        # Simulando login do usuário com a senha criptografada
        session = self.client.session
        session['usuario'] = self.usuario.id
        session.save()

        # Criar outras instâncias de teste
        self.categoria = Categoria.objects.create(nome='Test Categoria', usuario=self.usuario)
        self.livro = Livros.objects.create(
            nome='O Grande Gatsby',
            autor='F. Scott Fitzgerald',
            categoria=self.categoria,
            usuario=self.usuario,
            localizacao='Estante A',
            exemplares_disponiveis='5'
        )

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_ver_livro_view(self):
        response = self.client.get(reverse('ver_livros', args=[self.livro.id]))
        self.assertEqual(response.status_code, 200)

    # Teste de validação de email
    def test_valida_cadastro_email_invalido(self):
        """Testa se um email inválido é rejeitado durante o cadastro."""
        response = self.client.post(reverse('valida_cadastro'), {
            'nome': 'Novo Usuario',
            'email': 'emailinvalido',
            'senha': 'senha1234'
        })
        # A view redireciona para status=4 quando o email é inválido
        self.assertRedirects(response, '/auth/cadastro/?status=4')

    def test_valida_cadastro_email_invalido(self):
        response = self.client.post(reverse('valida_cadastro'), {
            'nome': 'Novo Usuario',
            'email': 'emailinvalido',
            'senha': 'senha1234'
        })
        self.assertEqual(response.status_code, 302)

    def test_valida_cadastro_email_ja_existente(self):
        """Testa se um email já existente no banco de dados é rejeitado."""
        response = self.client.post(reverse('valida_cadastro'), {
            'nome': 'Novo Usuario',
            'email': 'test@example.com',  # Email já criado no setUp
            'senha': 'senha1234'
        })
        self.assertEqual(response.status_code, 302)  # Verifica se o código de status é 302
        self.assertEqual(response['Location'], '/auth/cadastro/?status=3')  # Verifica se o redirecionamento foi para a URL correta

    def test_valida_cadastro_senha_curta(self):
        """Testa se uma senha com menos de 8 caracteres é rejeitada."""
        response = self.client.post(reverse('valida_cadastro'), {
            'nome': 'Usuario',
            'email': 'test@example.com',
            'senha': '123'  # Senha muito curta
        })
        self.assertEqual(response.status_code, 302)  # Verifica se o redirecionamento ocorreu (302)
        self.assertEqual(response['Location'], '/auth/cadastro/?status=2')  # Verifica a URL de redirecionamento

    def test_valida_cadastro_nome_ou_email_vazio(self):
        """Testa se campos nome ou email vazios são rejeitados."""
        response = self.client.post(reverse('valida_cadastro'), {
            'nome': '',  # Nome vazio
            'email': 'test@example.com',
            'senha': 'senha1234'
        })
        self.assertEqual(response.status_code, 302)  # Verifica se o redirecionamento ocorreu (302)
        self.assertEqual(response['Location'], '/auth/cadastro/?status=1')  # Verifica a URL de redirecionamento

    def test_sair(self):
        # Chamar a view de logout
        response = self.client.get(reverse('sair'))

        # Verifique se a sessão foi limpa
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/auth/login/')
        # Verifique se a sessão foi realmente limpa
        self.assertFalse('_auth_user_id' in self.client.session)
        
    def test_login_bem_sucedido(self):
        response = self.client.post(reverse('login'), {
            'email': 'test@example.com',
            'senha': '12345'  # Use a senha original
        })
        self.assertRedirects(response, '/livro/home/')
        self.assertEqual(self.client.session['usuario'], self.usuario.id)

    def test_login_senha_incorreta(self):
        response = self.client.post(reverse('login'), {
            'email': 'test@example.com',
            'senha': 'senha_incorreta'
        })
        self.assertRedirects(response, '/livro/home/')


    def test_login_email_inexistente(self):
        response = self.client.post(reverse('login'), {
            'email': 'nao_existente@exemplo.com',
            'senha': 'senha_qualquer'  # Senha qualquer
        })
        self.assertRedirects(response, '/livro/home/')
        

    def test_login_campos_vazios(self):
        response = self.client.post(reverse('login'), {
            'email': '',
            'senha': ''
        })
        self.assertRedirects(response, '/livro/home/')


    def test_login_email_vazio(self):
        response = self.client.post(reverse('login'), {
            'email': '',
            'senha': '12345'
        })
        self.assertRedirects(response, '/livro/home/')

    def test_login_senha_vazia(self):
        response = self.client.post(reverse('login'), {
            'email': 'test@example.com',
            'senha': ''
        })
        self.assertRedirects(response, '/livro/home/')

    #Cadastro
    def test_cadastro_usuario_logado(self):
        # Simulando um usuário logado na sessão
        session = self.client.session
        session['usuario'] = 1  # Id de um usuário fictício
        session.save()

        # Faz a requisição para a view de cadastro
        response = self.client.get(reverse('cadastro'))

        # Verifica se o usuário foi redirecionado para a página /livro/home/
        self.assertRedirects(response, '/livro/home/')



    def test_cadastro_usuario_deslogado(self):
        # Simulando um usuário deslogado (sem sessão)
        session = self.client.session
        session.pop('usuario', None)  # Remover qualquer dado de sessão do usuário
        session.save()

        # Faz a requisição para a view de cadastro
        response = self.client.get(reverse('cadastro'))

        # Verifica se a página de cadastro foi carregada corretamente
        self.assertEqual(response.status_code, 200)

        # Verifica se o template correto foi renderizado
        self.assertTemplateUsed(response, 'cadastro.html')



    
    def test_cadastro_com_status(self):
        # Simulando um usuário deslogado (sem sessão)
        session = self.client.session
        session.pop('usuario', None)  # Remove a sessão de usuário se houver
        session.save()

        # Faz a requisição para a view de cadastro com um status na URL
        response = self.client.get(reverse('cadastro') + '?status=1')

        # Verifica se a página de cadastro foi carregada corretamente
        self.assertEqual(response.status_code, 200)

        # Verifica se o status foi passado corretamente para o template
        self.assertIn('status', response.context)
        self.assertEqual(response.context['status'], '1')

        # Verifica se o template correto foi renderizado
        self.assertTemplateUsed(response, 'cadastro.html')



        # Verifica se a página de cadastro foi carregada corretamente
        self.assertEqual(response.status_code, 200)

        # Verifica se o status foi passado corretamente para o template
        self.assertIn('status', response.context)
        self.assertEqual(response.context['status'], '1')

        # Verifica se o template correto foi renderizado
        self.assertTemplateUsed(response, 'cadastro.html')