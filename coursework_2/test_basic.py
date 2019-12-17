from app import app, db, models
import os
import unittest

TEST_DB = 'test.db' 

class BasicUnitTests(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        base = os.path.abspath(os.path.dirname(__file__))
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base, 'tmp', TEST_DB)
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
        
    def tearDown(self):
        pass

    def test_home_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()

