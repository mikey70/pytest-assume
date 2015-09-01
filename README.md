# pytest-assume
A pytest plugin that allows multiple failures per test

## Installation

  pip install git+https://github.com/astraw38/pytest-assume.git


Sample Usage:
```python
    import pytest
    
@pytest.mark.parametrize(('x', 'y'), [(1, 1), (1, 0), (0, 1)])
def test_simple_assume(x, y):
    pytest.assume(x == y)
    pytest.assume(True)
    pytest.assume(False)
```        
        
    ======================================== FAILURES =========================================
    _________________________________ test_simple_assume[1-1] _________________________________
    >    pytest.assume(False)
    test_assume.py:7
 
    y          = 1
    x          = 1
    ----------------------------------------
    Failed Assumptions:1
    _________________________________ test_simple_assume[1-0] _________________________________
    >    pytest.assume(x == y)
    test_assume.py:5

    y          = 0
    x          = 1
    >    pytest.assume(False)
    test_assume.py:7

    y          = 0
    x          = 1
    ----------------------------------------
    Failed Assumptions:2
    _________________________________ test_simple_assume[0-1] _________________________________
    >    pytest.assume(x == y)
    test_assume.py:5

    y          = 1
    x          = 0
    >    pytest.assume(False)
    test_assume.py:7

    y          = 1
    x          = 0
    ----------------------------------------
    Failed Assumptions:2
    ================================ 3 failed in 0.02 seconds =================================
