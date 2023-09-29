from unittest import TestCase

from app import app, games

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with app.test_client() as client:
            response = client.get('/')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<title>Boggle</title>', html)
            self.assertIn('Homepage Template', html)

    def test_api_new_game(self):
        """Test starting a new game."""

        with app.test_client() as client:
            response = client.post('/api/new-game', json={'test':'false'})
            json = response.get_json()

            self.assertEqual(response.status_code, 200)
            self.assertIn('gameId', json.keys())
            self.assertEqual(type(json['board']), list)

    def test_api_score_word(self):
        """Test score the word"""

        with app.test_client() as client:
            new_game_response = client.post('/api/new-game', json={'test':'true'})

            ok_response = client.post('/api/score-word', json={'word':'CAT'}).get_json()
            not_word_response = client.post('/api/score-word', json={'word':'BOB4'}).get_json()
            not_on_board_response = client.post('/api/score-word', json={'word':'APPLE'}).get_json()

            self.assertEqual(ok_response['result'], 'ok')
            self.assertEqual(not_word_response['result'], 'not-word')
            self.assertEqual(not_on_board_response['result'], 'not-on-board')
