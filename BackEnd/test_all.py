import coverage
import pytest
from app import app
# from Test.test_temptest import *
from Test.test_courserc import *
from Test.test_calender import *
from Test.test_general import *
from Test.test_forum import *
from Test.test_tutorial import *
from Test.test_evaluation import *

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


if __name__ == '__main__':
    cov = coverage.Coverage()
    cov.start()
    pytest.main(['-s', 'test_all.py'])
    cov.stop()
    cov.save()

    # Optional: generate reports
    cov.html_report(directory='covhtml')
    


# import unittest
# from flask import current_app
# from app import app

# class BasicTestCase(unittest.TestCase):
#     def setUp(self):
#         self.app = app.test_client()
#         self.app.testing = True

#     def tearDown(self):
#         pass

#     def test_home_status_code(self):
#         """确保主页的状态码是200"""
#         result = self.app.get('/')
#         self.assertEqual(result.status_code, 200)

#     def test_404(self):
#         """确保请求一个不存在的页面返回404"""
#         result = self.app.get('/nonexistentpage')
#         self.assertEqual(result.status_code, 404)

# if __name__ == "__main__":
#     unittest.main()