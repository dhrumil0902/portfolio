from email.quoprimime import decodestring
from datetime import datetime
import math
from tracemalloc import reset_peak
import gspread
import math
import time
sa = gspread.service_account(filename = 'credentials.json')
workbook= sa.open("General Information (Responses)")
form = workbook.worksheet("Form Responses 1")
dest = workbook.worksheet("Organized Responses 3")
form.update_cell( 10,5,'hrumil')
dest.merge_cells("A1:A5", "MERGE_ALL")
dest.clear()
dest.format("A:Z", {"horizontalAlignment": "CENTER"})



def print_application( x_index, y_index, form_row, form,dest):
    dest.update_cell( y_index, x_index + 1, time_convert(form.cell(form_row,1).value))
    dest.merge_cells(get_range_A1(y_index, x_index+ 1, y_index, x_index + 4), "MERGE_ALL")

    dest.format(get_addr_int(y_index,x_index + 2), {
    "backgroundColor": {
      "red": 22.0,
      "green": 224.0,
      "blue": 224.0
    }})
    
    dest.update_cell( y_index + 1, x_index, "Names")
    dest.update_cell( y_index + 2, x_index, "Status")
    dest.update_cell( y_index + 3, x_index, "Annual Income")
    dest.update_cell( y_index + 4, x_index, "Credit Score")
    dest.update_cell( y_index + 5, x_index, "Move In")
    
    dest.merge_cells(get_range_A1(y_index + 5, x_index+ 1, y_index + 10, x_index + 4), "MERGE_ROWS")
    dest.update_cell( y_index + 5, x_index + 1, form.cell(form_row,6).value)
    relation = form.cell(form_row,48).value
    if form.cell(form_row,48).value is None:
        relation = "Relation Not Specified"
    dest.update_cell( y_index + 6, x_index + 1, form.cell(form_row,4).value + " Occupants " + "(" + relation + ")")
    dest.update_cell( y_index + 7, x_index + 1, form.cell(form_row,3).value)
    dest.update_cell( y_index + 8, x_index + 1, "mailto:" + form.cell(form_row,2).value)
    dest.update_cell( y_index + 9, x_index + 1, "Notes:")
    dest.format(get_addr_int(y_index + 9, x_index + 1), {"horizontalAlignment": "LEFT"})
    column = 7
    while(form.cell(form_row,column).value == None):
        column+=1
    print(column)
    next_applicant = 0
    next_col = 1
    for i in range(int(form.cell(form_row,4).value)):
        print(i)
        applicant_info(dest, form,form_row,column + next_applicant,y_index + 1,x_index + next_col)
        next_col+=1
        next_applicant+=4

def applicant_info(dest,form,form_row,form_col,dest_row,dest_col):
    dest.update_cell(dest_row, dest_col, form.cell(form_row,form_col).value)
    dest.update_cell(dest_row + 1, dest_col, form.cell(form_row,form_col + 1).value)
    dest.update_cell(dest_row + 2, dest_col, form.cell(form_row,form_col + 2).value)
    dest.update_cell(dest_row + 3, dest_col, form.cell(form_row,form_col + 3).value)


def time_convert(time):
    return datetime.strptime(time, "%m/%d/%Y %H:%M:%S").strftime("%m/%d/%Y %r")


def get_addr_int(row, col):
    """Translates cell's tuple of integers to a cell label.
    The result is a string containing the cell's coordinates in label form.
    :param row: The row of the cell to be converted.
                Rows start at index 1.
    :param col: The column of the cell to be converted.
                Columns start at index 1.
    Example:
    >>> wks.get_addr_int(1, 1)
    A1
    """
   

    #if row < 1 or col < 1:
      #  raise IncorrectCellLabel('(%s, %s)' % (row, col))

    div = col
    column_label = ''

    while div:
        (div, mod) = divmod(div, 26)
        if mod == 0:
            mod = 26
            div -= 1
        column_label = chr(mod + 64) + column_label

    label = '%s%s' % (column_label, row)
    return label


def get_range_A1(firstx,firsty,lastx,lasty):
    res = get_addr_int(firstx,firsty) + ":" + get_addr_int(lastx,lasty)
    print(res)
    return res


dest_row_app = 50
dest_col_app = 2


for application in range(2, dest.row_count):
    if form.cell(application, 1).value == None:
        break
    print(application)
    time.sleep(30)
    print_application(dest_col_app, dest_row_app, application, form, dest)
    dest_row_app += 11








