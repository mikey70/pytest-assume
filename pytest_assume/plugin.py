import pytest
import inspect
import os.path

def pytest_namespace():
    def assume(expr, msg=''):
        if not expr:
            # get filename, line, and context
            (filename, line, funcname, contextlist) = inspect.stack()[1][1:5]
            filename = os.path.relpath(filename)
            context = contextlist[0]
            # format entry
            msg = '%s\n' % msg if msg else ''
            entry = '>%s%s%s:%s\n--------' % (context, msg, filename, line)
            # add entry
            pytest._failed_assumptions.append(entry)

    return {'_failed_assumptions': [],
            'assume': assume}

def pytest_runtest_setup(item):
    del pytest._failed_assumptions[:]

@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if call.when == "call" and pytest._failed_assumptions:
        summary = 'Failed Assumptions:%s' % len(pytest._failed_assumptions)
        pytest._failed_assumptions.append(summary)
        if report.longrepr:
            report.longrepr = str(report.longrepr) + \
                              '\n--------\n' + ('\n'.join(pytest._failed_assumptions))
        else:
            report.longrepr = '\n'.join(pytest._failed_assumptions)
        report.outcome = "failed"

