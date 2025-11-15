import unittest
from app import app
import werkzeug

# Patch temporário para adicionar o atributo '__version__' em werkzeug 
if not hasattr(werkzeug, '__version__'): 
    werkzeug.__version__ = "mock-version"

class APITestCase(unittest.TestCase): 
    @classmethod 
    def setUpClass(cls): 
        # Criação do cliente de teste 
        cls.client = app.test_client()
    
    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "API is running"})

    def test_login(self):
        response = self.client.post('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.json)

    def test_protected_no_token(self):
        response = self.client.get('/protected')
        self.assertEqual(response.status_code, 401)


    def test_items_returns_list(self):
        """Verifica se /items retorna uma lista válida"""
        response = self.client.get('/items')
        self.assertEqual(response.status_code, 200)
        self.assertIn("items", response.json)
        self.assertIsInstance(response.json["items"], list)
        self.assertGreater(len(response.json["items"]), 0)


    def test_login_returns_valid_jwt(self):
        """Verifica se o /login retorna um token JWT em string"""
        response = self.client.post('/login')
        self.assertEqual(response.status_code, 200)
        token = response.json.get("access_token")
        self.assertIsInstance(token, str)
        self.assertGreater(len(token), 10)  # valida token minimamente


    def test_protected_with_valid_token(self):
        """Acessa /protected com um token válido"""
        # Primeiro gera o token
        login_response = self.client.post('/login')
        token = login_response.json.get("access_token")

        # Chama rota /protected usando o token
        headers = {"Authorization": f"Bearer {token}"}
        response = self.client.get('/protected', headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json)
        self.assertEqual(response.json["message"], "Protected route")




if __name__ == '__main__':
    unittest.main()
