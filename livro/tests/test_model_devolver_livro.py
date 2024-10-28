from django.urls import reverse
from django.test import TestCase
from ..models import Emprestimos, Usuario, Livros
from django.utils import timezone

class DevolverLivroTest(TestCase):

    def setUp(self):
        self.usuario = Usuario.objects.create(
            nome="testeuser",
            email="teste@teste.com",
            senha="teste123"
        )
        self.usuario.save()

        self.livro = Livros.objects.create(
            obra='Livro de Teste',
            autor='Autor Teste',
            emprestado=True,
            usuario=self.usuario  # Adicione o usuário aqui
        )

        self.emprestimo = Emprestimos.objects.create(livro=self.livro, usuario=self.usuario)

    def test_devolver_livro(self):
        # Simule a devolução do livro
        response = self.client.post(reverse('devolver_livro'), {
            'id_livro_devolver': self.livro.id,
        })
        
        # Verifique se o redirecionamento foi para a página correta
        self.assertRedirects(response, '/livro/home')

        # Verifique se o livro foi marcado como disponível
        self.livro.refresh_from_db()
        self.assertFalse(self.livro.emprestado)

        # Verifique se a data de devolução foi atualizada
        self.emprestimo.refresh_from_db()
        self.assertIsNotNone(self.emprestimo.data_devolucao)

    def test_devolver_livro_sem_emprestimo(self):
        # Simule um livro que não tem empréstimo ativo
        outro_livro = Livros.objects.create(obra='Outro Livro', autor='Outro Autor', emprestado=True)
        
        # Tente devolver o livro sem um empréstimo ativo
        response = self.client.post(reverse('devolver_livro'), {
            'id_livro_devolver': outro_livro.id,
        })
        
        # Verifique se o livro ainda está emprestado
        outro_livro.refresh_from_db()
        self.assertTrue(outro_livro.emprestado)
