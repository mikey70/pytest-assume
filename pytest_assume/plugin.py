import pytest
import inspect
import os.path
from py.io import saferepr

def pytest_namespace():
    def assume(expr, msg=''):
        if not expr:
            # get filename, line, and context
            (frame, filename, line, funcname, contextlist) = inspect.stack()[1][0:5]
            filename = os.path.relpath(filename)
            context = contextlist[0]
            # format entry
            msg = '%s\n' % msg if msg else ''
            entry = '>%s%s%s:%s\n' % (context, msg, filename, line)
            # add entry
            pytest._failed_assumptions.append(entry)
            pretty_locals = ["%-10s = %s" %(name, saferepr(val))
                             for name, val in frame.f_locals.items()]
            pytest._assumption_locals.append(pretty_locals)

    return {'_assumption_locals': [],
            '_failed_assumptions': [],
            'assume': assume}

def pytest_runtest_setup(item):
    del pytest._failed_assumptions[:]
    del pytest._assumption_locals[:]

@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if call.when == "call" and pytest._failed_assumptions:
        summary = 'Failed Assumptions:%s' % len(pytest._failed_assumptions)
        if report.longrepr:
            report.sections.append((summary, "\n".join(pytest._failed_assumptions)))
        else:
            assume_data = zip(pytest._failed_assumptions, pytest._assumption_locals)
            longrepr = ["{}\n{}".format(assumption, "\n".join(locals))
                        for assumption, locals in assume_data]
            longrepr.append("-" * 40)
            longrepr.append(summary)
            report.longrepr = '\n'.join(longrepr)
        report.outcome = "failed"

