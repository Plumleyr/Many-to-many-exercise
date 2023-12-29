from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test_db'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):

    def setUp(self):

        User.query.delete()

        user = User(first_name = "Test", last_name = "User", image_url = "https://thumbs.dreamstime.com/b/test-icon-vector-question-mark-male-user-person-profile-avatar-symbol-help-sign-glyph-pictogram-test-icon-vector-168495430.jpg")

        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
    
    def tearDown(self):

        db.session.rollback()
    
    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text = True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test User', html)

    def test_create_user_form(self):
        with app.test_client() as client:
            resp = client.get('/users/new')
            html = resp.get_data(as_text = True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<form action="/users/new" method="post">',html)
    
    def test_create_user(self):
        with app.test_client() as client:
            d = {'first_name': 'Test', 'last_name': 'User2', 'image_url': 'https://i.pinimg.com/736x/a8/57/00/a85700f3c614f6313750b9d8196c08f5.jpg'}
            resp = client.post('/users/new', data = d, follow_redirects = True)
            html = resp.get_data(as_text = True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test User2', html)

    def test_edit_user(self):
        with app.test_client() as client:
            d = {'first_name': "Test", 'last_name': "User3", 'image_url': "https://thumbs.dreamstime.com/b/test-icon-vector-question-mark-male-user-person-profile-avatar-symbol-help-sign-glyph-pictogram-test-icon-vector-168495430.jpg"}
            resp= client.post(f'/users/{self.user_id}/edit', data = d, follow_redirects = True)
            html = resp.get_data(as_text = True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test User3', html)
