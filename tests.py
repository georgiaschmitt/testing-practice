"""Testsq for Balloonicorn's Flask app."""

import unittest
import party


class PartyTests(unittest.TestCase):
    """Tests for my party site."""

    def setUp(self):
        """Code to run before every test."""

        self.client = party.app.test_client()
        party.app.config['TESTING'] = True

    def test_homepage(self):
        """Can we reach the homepage?"""

        result = self.client.get("/")
        self.assertIn(b"having a party", result.data)

    def test_no_rsvp_yet(self):
        """Do users who haven't RSVPed see the correct view?"""

        result = self.client.get("/")
        self.assertIn(b"email", result.data)
        

    def test_rsvp(self):
        """Do RSVPed users see the correct view?"""

        rsvp_info = {'name': "Jane", 'email': "jane@jane.com"}

        result = self.client.post("/rsvp", data=rsvp_info,
                                    follow_redirects=True)

        self.assertNotIn(b"Email", result.data) 
        self.assertIn(b"Party Details", result.data)

    def test_rsvp_mel(self):
        """Can we keep Mel out?"""

        rsvp_info = {'name': "Mel Melitpolski", 'email': "mel@ubermelon.com"}
        result = self.client.post("/rsvp", data=rsvp_info, 
                                    follow_redirects=True)

        self.assertNotIn(b"Party Details", result.data)
        self.assertIn(b"Please RSVP", result.data)
        self.assertNotIn(b"Yay!", result.data)

    def test_rsvp_capital_mel(self):
        """Can we keep Mel out if he uses strange capitalization?"""

        rsvp_info = {'name': "Mel MeLIToPolSKI", 'email': "MEL@ubermelon.com"}
        result = self.client.post("/rsvp", data=rsvp_info, 
                                    follow_redirects=True)

        self.assertNotIn(b"Party Details", result.data)
        self.assertIn(b"Please RSVP", result.data)
        self.assertNotIn(b"Yay!", result.data)

    def test_rsvp_shortname_mel(self):
        """Can we keep Mel out if he uses just his first name?"""

        rsvp_info = {'name': "Mel", 'email': "test@ubermelon.com"}
        result = self.client.post("/rsvp", data=rsvp_info, 
                                    follow_redirects=True)

        self.assertNotIn(b"Party Details", result.data)
        self.assertIn(b"Please RSVP", result.data)
        self.assertNotIn(b"Yay!", result.data)


if __name__ == "__main__":
    unittest.main()
