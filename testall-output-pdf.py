# script to run all test scripts

from test1_output_pdf import inject_text
from test2_output_pdf import test_print
from test3_output_pdf import test_png


def test_all():
    inject_text()
    test_print()
    test_png()


test_all()
