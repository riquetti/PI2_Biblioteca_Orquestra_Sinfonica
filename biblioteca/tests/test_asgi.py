from django.core.asgi import get_asgi_application
import os
from django.test import TestCase

class ASGITest(TestCase):
    def test_asgi_application_initialization(self):
        # Verifica se o módulo de configurações está corretamente definido
        self.assertEqual(os.getenv('DJANGO_SETTINGS_MODULE'), 'biblioteca.settings')
        
        # Tenta inicializar a aplicação ASGI
        try:
            application = get_asgi_application()
            self.assertIsNotNone(application)
        except Exception as e:
            self.fail(f"Falha ao inicializar a aplicação ASGI: {e}")
