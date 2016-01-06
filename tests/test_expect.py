pytest_plugins = "pytester",


def test_passing_expect(testdir):
    testdir.makepyfile(
        """
        import pytest

        def test_func():
            pytest.assume(1 == 1)
        """)
    result = testdir.runpytest_inprocess()
    result.assert_outcomes(1, 0, 0)
    assert '1 passed' in result.stdout.str()


def test_failing_expect(testdir):
    testdir.makepyfile(
        """
        import pytest
        def test_func():
            pytest.assume(1 == 2)
        """)
    result = testdir.runpytest_inprocess()
    result.assert_outcomes(0, 0, 1)
    assert '1 failed' in result.stdout.str()
    assert 'Failed Assumptions: 1' in result.stdout.str()


def test_passing_expect_doesnt_cloak_assert(testdir):
    testdir.makepyfile(
        """
        import pytest
        def test_func():
            pytest.assume(1 == 1)
            assert 1 == 2
        """)
    result = testdir.runpytest_inprocess()
    result.assert_outcomes(0, 0, 1)
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
    result = testdir.runpytest_inprocess()
    result.assert_outcomes(0, 0, 1)
    assert '1 failed' in result.stdout.str()
    assert 'AssertionError' in result.stdout.str()
    assert 'Failed Assumptions: 1' in result.stdout.str()


def test_msg_is_in_output(testdir):
    testdir.makepyfile(
        """
        import pytest
        def test_func():
            a = 1
            b = 2
            pytest.assume(a == b, 'a:%s b:%s' % (a,b))
        """)
    result = testdir.runpytest_inprocess()
    result.assert_outcomes(0, 0, 1)
    assert '1 failed' in result.stdout.str()
    assert 'Failed Assumptions: 1' in result.stdout.str()
    assert 'a:1 b:2' in result.stdout.str()


def test_with_locals(testdir):
    testdir.makepyfile(
        """
        import pytest
        def test_func():
            a = 1
            b = 2
            pytest.assume(a == b)
        """)
    result = testdir.runpytest_inprocess("--showlocals")
    result.assert_outcomes(0, 0, 1)
    stdout = result.stdout.str()
    assert '1 failed' in stdout
    assert 'Failed Assumptions: 1' in stdout
    assert "a          = 1" in stdout
    assert "b          = 2" in stdout


def test_without_locals(testdir):
    testdir.makepyfile(
        """
        import pytest
        def test_func():
            a = 1
            b = 2
            pytest.assume(a == b)
        """)
    result = testdir.runpytest_inprocess()
    stdout = result.stdout.str()
    result.assert_outcomes(0, 0, 1)
    assert '1 failed' in stdout
    assert 'Failed Assumptions: 1' in stdout
    assert "a          = 1" not in stdout
    assert "b          = 2" not in stdout

def test_xfail_assumption(testdir):
    testdir.makepyfile(
        """
        import pytest
        @pytest.mark.xfail(run=True, reason="testfail")
        def test_func():
            pytest.assume(1 == 2)
        """)
    result = testdir.runpytest_inprocess("-rxs")
    stdout = result.stdout.str()
    outcomes = result.parseoutcomes()
    assert outcomes.get("xfailed", 0) == 1
    assert "testfail" in stdout


def test_xpass_assumption(testdir):
    testdir.makepyfile(
        """
        import pytest
        @pytest.mark.xfail(run=True, reason="testfail")
        def test_func():
            pytest.assume(True)
        """)
    result = testdir.runpytest_inprocess()
    outcomes = result.parseoutcomes()
    assert outcomes.get("xpassed", 0) == 1
