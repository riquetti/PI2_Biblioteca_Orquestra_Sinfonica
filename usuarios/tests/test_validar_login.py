from django.urls import reverse
from django.test import TestCase
from usuarios.models import Usuario
from hashlib import sha256

class TestViews(TestCase):

    def setUp(self):
        # Criação de um usuário para os testes
        self.usuario = Usuario.objects.create(
            nome='Test User',
            email='test@example.com',
            senha=sha256('senha123'.encode()).hexdigest()
        )

    def test_validar_login_com_credenciais_corretas(self):
        response = self.client.post(reverse('login'), {
        'email': 'test@example.com',
        'senha': 'senha123'
    })

    # Verifica se o redirecionamento está correto
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/livro/home/')

    def test_validar_login_com_senha_incorreta(self):
        response = self.client.post(reverse('login'), {
            'email': 'test@example.com',
            'senha': 'senha_errada'
        })

        # Verifica se o redirecionamento está correto
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/auth/login/?status=1')

    def test_validar_login_com_email_nao_cadastrado(self):
        response = self.client.post(reverse('login'), {
            'email': 'naoexiste@example.com',
            'senha': 'senha123'
        })

        # Verifica se o redirecionamento está correto
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/auth/login/?status=1')

    def test_validar_login_campos_vazios(self):
        response = self.client.post(reverse('login'), {
            'email': '',
            'senha': ''
        })

        # Verifica se o redirecionamento está correto
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/auth/login/?status=1')

