from unittest import TestCase
from unittest.mock import MagicMock, patch

from bot.checks import SkillCheck, GenericCheck, AttributeCheck
from bot import check, note
from test.mocks import MockAuthor, MockMessage


class TestSkillCheck(TestCase):
    def test_parse(self):
        user = MockAuthor("TestUser")
        self.assertIsInstance(check.create_check("13 14 15@2", user), SkillCheck)
        self.assertIsInstance(check.create_check("13", user), AttributeCheck)
        self.assertIsInstance(check.create_check("13 @2", user), AttributeCheck)
        self.assertIsInstance(check.create_check("13 14 -2", user), GenericCheck)
        self.assertIsInstance(check.create_check("13 14 @2", user), GenericCheck)

    @patch("random.randint", new_callable=MagicMock())
    def test_fate(self, mock_randint: MagicMock):
        user = MockAuthor("TestUser")
        note.create_note("schips_{}".format(str(user)), 3, user)

        mock_randint.return_value = 12
        first, _ = check.create_response(MockMessage(user, "11,9,9@4"))
        self.assertEqual(
            first,
            "@TestUser \n"
            "```py\n"
            "EEW:     11   9   9\n"
            "Würfel:  12  12  12\n"
            "FW 4     -1  -3  -3 = -3 FP\n"
            "Nicht bestanden\n"
            "```",
        )
        other_message = MockMessage(MockAuthor("NotTestUser"), "14,14,10@6")
        check.create_response(other_message)
        self.assertNotEqual(user, other_message.author)

        mock_randint.return_value = 2
        second, _ = check.create_response(MockMessage(user, "schips rrr"))
        self.assertEqual(
            second,
            "@TestUser \n"
            "```py\n"
            "EEW:     11   9   9\n"
            "Würfel:   2   2   2\n"
            "FW 4                = 4 FP\n"
            "Bestanden mit QS 2\n"
            "```",
        )
        mock_randint.return_value = 10
        third, _ = check.create_response(MockMessage(user, "schips rkk"))
        self.assertEqual(
            third,
            "@TestUser \n"
            "```py\n"
            "EEW:     11   9   9\n"
            "Würfel:  10   2   2\n"
            "FW 4                = 4 FP\n"
            "Bestanden mit QS 2\n"
            "```",
        )
        mock_randint.return_value = 10
        fourth, _ = check.create_response(MockMessage(user, "schips rkk"))
        self.assertEqual(
            fourth,
            "@TestUser \n"
            "```py\n"
            "EEW:     11   9   9\n"
            "Würfel:  10   2   2\n"
            "FW 4                = 4 FP\n"
            "Bestanden mit QS 2\n"
            "```",
        )
        mock_randint.return_value = 10
        fifth, _ = check.create_response(MockMessage(user, "schips rkk"))
        self.assertEqual(fifth, "@TestUser Keine Schips übrig!")

        note.delete_note(user, "schips_{}".format(str(user)))

    @patch("random.randint", new_callable=MagicMock())
    def test_force(self, mock_randint: MagicMock):
        user = MockAuthor("TestUser")
        mock_randint.return_value = 12
        first, _ = check.create_response(MockMessage(user, "14,14,14@12"))
        self.assertEqual(
            first, "@TestUser \n```py\nRoutineprobe: 6 FP = QS 2\n```",
        )
        second, _ = check.create_response(MockMessage(user, "force"))
        self.assertEqual(
            second,
            "@TestUser \n"
            "```py\n"
            "EEW:     14  14  14\n"
            "Würfel:  12  12  12\n"
            "FW 12               = 12 FP\n"
            "Bestanden mit QS 4\n"
            "```",
        )

    @patch("random.randint", new_callable=MagicMock())
    def test_retry_repeat(self, mock_randint: MagicMock):
        user = MockAuthor("TestUser")
        mock_randint.return_value = 12
        first, _ = check.create_response(MockMessage(user, "11,9,9@4"))
        self.assertEqual(
            first,
            "@TestUser \n"
            "```py\n"
            "EEW:     11   9   9\n"
            "Würfel:  12  12  12\n"
            "FW 4     -1  -3  -3 = -3 FP\n"
            "Nicht bestanden\n"
            "```",
        )
        mock_randint.return_value = 10
        second, _ = check.create_response(MockMessage(user, "repeat"))
        self.assertEqual(
            second,
            "@TestUser \n"
            "```py\n"
            "EEW:     11   9   9\n"
            "Würfel:  10  10  10\n"
            "FW 4         -1  -1 = 2 FP\n"
            "Bestanden mit QS 1\n"
            "```",
        )
        mock_randint.return_value = 9
        third, _ = check.create_response(MockMessage(user, "retry"))
        self.assertEqual(
            third,
            "@TestUser \n"
            "```py\n"
            "EEW:     10   8   8\n"
            "Würfel:   9   9   9\n"
            "FW 4         -1  -1 = 2 FP\n"
            "Bestanden mit QS 1\n"
            "```",
        )
