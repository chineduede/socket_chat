import unittest
import server


class MyTestCase(unittest.TestCase):

    def test_chat_server(self):
        server.run_server()
        self.assertEqual(True, False)
        

    def test_something(self):
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
