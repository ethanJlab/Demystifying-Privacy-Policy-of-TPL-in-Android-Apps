# test script that tests if output_pdf.py outputs text to a pdf

from output_pdf import main as m


def inject_text():
    prelude = []
    list1 = []
    list2 = []
    list3 = []
    list4 = []

    prelude.append("successfully printed out to the prelude section")

    list1.append("successfully printed out to the part 1 section")

    list2.append("successfully printed out to the part 2 section")

    list4.append("successfully printed out to the part 4 section")

    m('test_report_1', True, kwargs_0=prelude, kwargs_1=list1, kwargs_2=list2, kwargs_3=list3, kwargs_4=list4)


inject_text()
