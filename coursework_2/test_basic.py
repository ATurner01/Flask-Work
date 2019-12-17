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

    #############################
    # Setup some helper methods #
    #############################
    
    def register(self, username, password, email):
        return self.app.post('/register', data=dict(username=username, password=password, email=email), follow_redirects=True)

    def login(self, username, password):
        return self.app.post('/login', data=dict(username=username, password=password), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    ################################
    # Tests routes to basic pages  #
    ################################
    
    def test_home_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        response = self.app.get('/login', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_register_page(self):
        response = self.app.get('/register', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_list_book_page(self):
        response = self.app.get('/list_books', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    ####################################
    # Test basic account functionality #
    ####################################

    #Each test in this section looks for 2 things,
    #1. The request redirects successfully with code 200
    #2. The request redirects to a page containing relevating information relating to the request
    #An example for the second point would be when an account is created, a message is flashed to the page
    #Our unit test will look at the data from the response to check if this flashed message is present
    
    def test_register(self):
        response = self.register('Test', 'Password', 'anEmail@email.co.uk')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Account creation successful. You may now login.', response.data)

    def test_failed_register(self):
        account1 = self.register('Test', 'Password', 'anEmail@email.co.uk')
        response = self.register('Test', 'Password', 'anEmail@email.co.uk')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Error. Username is already in use. Please choose a different one.', response.data)

    def test_login(self):
        account = self.register('Test', 'Password', 'anEmail@email.co.uk')
        response = self.login('Test', 'Password')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Home', response.data) #Upon successful login, the user should be redirected to the Homepage

    def test_failed_login(self):
        account = self.register('Test', 'Password', 'anEmail@email.co.uk')
        response = self.login('Test', 'FlaskLogin')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Incorrect username or password.', response.data)

    def test_logout(self):
        account = self.register('Test', 'Password', 'anEmail@email.co.uk')
        login = self.login('Test', 'Password')
        response = self.logout()
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data) #The 'logout' button in the navbar should change to 'login' when no user is logged in


if __name__ == '__main__':
    unittest.main()

