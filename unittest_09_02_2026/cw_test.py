import unittest
import cw

class Test(unittest.TestCase):
    def setUp(self):
        self.app = cw.App()
        self.app.withdraw()

    def tearDown(self):
        self.app.destroy()

    def test_greeting(self):
        self.app.entry.insert(0, "asd")
        self.app.btn.invoke()
        result = self.app.label.cget("text")
        self.assertEqual(result, "Witaj, asd!")

    def test_clear(self):
        self.app.entry.insert(0, "asd")
        self.app.btn.invoke()
        result = self.app.label.cget("text")
        self.assertEqual(result, "Witaj, asd!")

        self.app.clear.invoke()
        result = self.app.label.cget("text")
        self.assertEqual(result, "")
        result = self.app.entry.get()
        self.assertEqual(result, "")

    def test_visible(self):
        self.app.update()
        self.assertTrue(not self.app.btn.winfo_ismapped())


if __name__ == "__main__":
    unittest.main()
