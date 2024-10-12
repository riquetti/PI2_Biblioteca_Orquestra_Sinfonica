# Testes de model
import os

import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'biblioteca.settings'
django.setup()

from django.core.exceptions import ValidationError
from django.test import TestCase

from usuarios.models import Usuario  # Importa o modelo correto


class UsuarioModelTest(TestCase):

    # Criação de um usuário
    def test_criacao_de_usuario_simples(self):
        """
        Testa a criação simples de um usuário.
        """
        usuario = Usuario.objects.create(
            nome='Teste Simples',
            email='teste.simples@email.com',
            senha='senha123',
            ativo=True
        )
        
        # Verifica se o usuário foi criado e se os atributos estão corretos
        self.assertIsInstance(usuario, Usuario)
        self.assertEqual(usuario.nome, 'Teste Simples')
        self.assertEqual(usuario.email, 'teste.simples@email.com')
        self.assertTrue(usuario.ativo)

    def test_email_unico(self):
        Usuario.objects.create(nome='Usuario 1', email='test1@email.com', senha='senha123', ativo=True)
        with self.assertRaises(ValidationError):
            usuario = Usuario(nome='Usuario 2', email='test1@email.com', senha='senha123', ativo=True)
            usuario.full_clean()  # Gera a validação

    def test_nome_vazio(self):
        with self.assertRaises(ValidationError):
            usuario = Usuario(nome='', email='test@email.com', senha='senha123', ativo=True)
            usuario.full_clean()

    def test_senha_vazia(self):
        with self.assertRaises(ValidationError):
            usuario = Usuario(nome='Usuario', email='test@email.com', senha='', ativo=True)
            usuario.full_clean()

    def test_email_invalido(self):
        with self.assertRaises(ValidationError):
            usuario = Usuario(nome='Usuario', email='invalid-email', senha='senha123', ativo=True)
            usuario.full_clean()

    def test_str_method(self):
        usuario = Usuario.objects.create(nome='Teste Simples', email='teste.simples@email.com', senha='senha123', ativo=True)
        self.assertEqual(str(usuario), 'Teste Simples')

    def test_atualizacao_usuario(self):
        usuario = Usuario.objects.create(nome='Usuario Original', email='original@email.com', senha='senha123', ativo=True)
        usuario.nome = 'Usuario Atualizado'
        usuario.save()
        self.assertEqual(usuario.nome, 'Usuario Atualizado')

    def test_deletar_usuario(self):
        usuario = Usuario.objects.create(nome='Usuario Para Deletar', email='delete@email.com', senha='senha123', ativo=True)
        usuario.delete()
        with self.assertRaises(Usuario.DoesNotExist):
            Usuario.objects.get(email='delete@email.com')

    def test_usuario_ativo(self):
        usuario = Usuario.objects.create(nome='Usuario Ativo', email='ativo@email.com', senha='senha123', ativo=True)
        self.assertTrue(usuario.ativo)

    def test_usuario_inativo(self):
        usuario = Usuario.objects.create(nome='Usuario Inativo', email='inativo@email.com', senha='senha123', ativo=False)
        self.assertFalse(usuario.ativo)
