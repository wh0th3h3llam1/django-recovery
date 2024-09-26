from unittest import TestCase

from recovery.utils import get_list_of_recovery_codes


class RecoveryCodesTest(TestCase):

    def test_list_of_recovery_codes(self):

        codes = get_list_of_recovery_codes()
        assert len(codes) == 10

        for code in codes:
            assert code.isnumeric()
