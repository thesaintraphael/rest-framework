from django.test import TransactionTestCase
from django.test.runner import DiscoverRunner

from unittest.suite import TestSuite


class UnitTestRunner(DiscoverRunner):

    def setup_databases(self, **kwargs) -> None:
        # disabling database setup for unittests
        pass

    def teardown_databases(self, old_config, **kwargs) -> None:
        pass
    
    def build_suite(self, test_labels, extra_tests, **kwargs) -> TestSuite:
        suite = super().build_suite(**kwargs)
        tests = [test for test in suite._tests if self.is_unittest(test)]

        return TestSuite(tests=tests)

    def is_unittest(self, test) -> bool:
        return not issubclass(test.__class__, TransactionTestCase)
