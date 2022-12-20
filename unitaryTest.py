import unittest
import search4web
import databaseFunction

databaseFunction.insertarUsuario("example","1234","example@gmail.com")

class TestInit(unittest.TestCase):
    def test_search_for_letters(self):
        self.assertEqual(search4web.search4letters("a","aeiou"), set("a"))
    def test_valid_login_name(self):
        self.assertEqual(databaseFunction.validLogin("example", "1234"),True)
    def test_buscar_usuario(self):
        self.assertEqual(databaseFunction.buscarUsuario("example"),True)
