from amazonAssignment.utilities import excel_utils

def get_test_data():
    path = "D://LambdaTestAssignment//amazonAssignment//test_data//test_data.xlsx"
    rows = excel_utils.get_row_count(path, "Sheet1")
    data = []
    for r in range(2, rows + 1):
        testcase_id = excel_utils.read_data(path, "Sheet1", r, 1)
        execute_flag = excel_utils.read_data(path, "Sheet1", r, 2)
        test_type = excel_utils.read_data(path, "Sheet1", r, 3)
        test_case_description = excel_utils.read_data(path, "Sheet1", r, 4)
        device_name = excel_utils.read_data(path, "Sheet1", r, 5)
        model_name = excel_utils.read_data(path, "Sheet1", r, 6)

        data.append((testcase_id, execute_flag, test_type, test_case_description, device_name, model_name))
    return data