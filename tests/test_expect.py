pytest_plugins = "pytester",


def test_passing_expect(testdir):
    testdir.makepyfile(
        """
        import pytest

        def test_func():
            pytest.assume(1 == 1)
        """)
    result = testdir.runpytest()
    assert '1 passed' in result.stdout.str()


def test_failing_expect(testdir):
    testdir.makepyfile(
        """
        import pytest
        def test_func():
            pytest.assume(1 == 2)
        """)
    result = testdir.runpytest()
    assert '1 failed' in result.stdout.str()
    assert 'Failed Assumptions:1' in result.stdout.str()


def test_passing_expect_doesnt_cloak_assert(testdir):
    testdir.makepyfile(
        """
        import pytest
        def test_func():
            pytest.assume(1 == 1)
            assert 1 == 2
        """)
    result = testdir.runpytest()
    assert '1 failed' in result.stdout.str()
    assert 'AssertionError' in result.stdout.str()


def test_failing_expect_doesnt_cloak_assert(testdir):
    testdir.makepyfile(
        """
        import pytest
        def test_func():
            pytest.assume(1 == 2)
            assert 1 == 2
        """)
    result = testdir.runpytest()
    assert '1 failed' in result.stdout.str()
    assert 'AssertionError' in result.stdout.str()
    assert 'Failed Assumptions:1' in result.stdout.str()


def test_msg_is_in_output(testdir):
    testdir.makepyfile(
        """
        import pytest
        def test_func():
            a = 1
            b = 2
            pytest.assume(a == b, 'a:%s b:%s' % (a,b))
        """)
    result = testdir.runpytest()
    assert '1 failed' in result.stdout.str()
    assert 'Failed Assumptions:1' in result.stdout.str()
    assert 'a:1 b:2' in result.stdout.str()


