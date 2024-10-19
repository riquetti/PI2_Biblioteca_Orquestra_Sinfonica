from django.test import TestCase
from usuarios.models import Usuario
from livro.models import Categoria

class CategoriaModelTest(TestCase):
    
    def setUp(self):
        # Cria um usuário de teste
        self.usuario = Usuario.objects.create(
            nome="Usuario Teste",
            email="teste@email.com",
            senha="senha123"
        )
    
    def test_categoria_criacao(self):
        """
        Testa se a categoria é criada corretamente.
        """
        categoria = Categoria.objects.create(
            nome="Ficção",
            descricao="Descrição da categoria Ficção",
            usuario=self.usuario
        )
        
        self.assertEqual(str(categoria), categoria.nome)  # Verifica o método __str__
        self.assertEqual(categoria.nome, "Ficção")
        self.assertEqual(categoria.usuario, self.usuario)  # Verifica o relacionamento com o usuário
