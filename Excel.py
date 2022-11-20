import xlsxwriter
import datetime
import Settings as s
from Joint import Joint


def create_workbook():
    current_time = datetime.datetime.now()
    workbook_name = str(current_time.day) + "." + str(current_time.month) + " " + str(current_time.hour) + "." + \
                     str(current_time.minute) + "." + str(current_time.second) + ".xlsx"
    s.excel_workbook = xlsxwriter.Workbook(workbook_name)


def wf_joints(ex_name, list_joints):
    """
    Writing joints data for an exercise in Excel file in two versions
    :param ex_name:
    :param list_joints:
    :return:
    """
    current_time = datetime.datetime.now()
    name = ex_name + str(current_time.minute) + str(current_time.second)
    s.worksheet = s.excel_workbook.add_worksheet(name)
    frame_number = 1

    for l in range(1, len(list_joints)):
        row = 1
        s.worksheet.write(0, frame_number, frame_number)
        for j in list_joints[l]:
            if type(j) == Joint:
                j_ar = j.joint_to_array()
                for i in range(len(j_ar)):
                    s.worksheet.write(row, frame_number, str(j_ar[i]))
                    row += 1
            else:
                s.worksheet.write(row, frame_number, j)
                row += 1
        frame_number += 1

    s.excel_workbook.close()