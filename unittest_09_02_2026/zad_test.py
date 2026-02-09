import unittest
import zad

class Test(unittest.TestCase):
    def setUp(self):
        self.app = zad.App()
        self.app.withdraw()

    def tearDown(self):
        self.app.destroy()

    def test_sum(self):
        self.app.lhs.insert(0, "5")
        self.app.rhs.insert(0, "10")
        self.app.submit.invoke()
        result = self.app.result.cget("text")
        self.assertEqual(result, "15")

    def test_bad(self):
        self.app.lhs.insert(0, "abc")
        self.app.rhs.insert(0, "5")
        self.app.submit.invoke()
        result = self.app.result.cget("text")
        self.assertEqual(result, zad.ERROR)

    def test_empty(self):
        self.assertEqual("", self.app.lhs.get())
        self.assertEqual("", self.app.rhs.get())
        self.app.submit.invoke()
        result = self.app.result.cget("text")
        self.assertEqual(result, zad.ERROR)


if __name__ == "__main__":
    unittest.main()
