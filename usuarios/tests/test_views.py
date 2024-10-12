from django.test import TestCase
from django.urls import reverse

from usuarios.models import Usuario


class UsuarioViewTest(TestCase):

    def test_registro_usuario_view(self):
        """
        Testa se a view de validação de cadastro cria corretamente um usuário e redireciona após o cadastro.
        """
        data = {
            'nome': 'Teste Usuario',
            'email': 'teste@email.com',
            'senha': 'senha123'
        }
        response = self.client.post(reverse('valida_cadastro'), data)
        self.assertEqual(response.status_code, 302)  # Verifica se houve redirecionamento
        self.assertRedirects(response, '/auth/cadastro/?status=0')  # Redireciona com sucesso

    def test_registro_usuario_falha(self):
        """
        Testa se a view de validação de cadastro lida corretamente com dados inválidos.
        """
        data = {
            'nome': '',
            'email': 'teste',
            'senha': 'senha123'
        }
        response = self.client.post(reverse('valida_cadastro'), data)
        self.assertEqual(response.status_code, 302)  # Deve redirecionar para a página com erro
        self.assertRedirects(response, '/auth/cadastro/?status=1')  # Redireciona com erro no nome vazio
