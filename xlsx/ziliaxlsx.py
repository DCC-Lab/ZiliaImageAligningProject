from xlsx.xlsx import XLSX


class ZiliaXLSX(XLSX):
    def __init__(self, xlsxPath):
        super().__init__(xlsxPath)

    def monkeyKeys(self):
        # Get the keys with data type
        keys = {}
        for worksheet in self.worksheets:
            if worksheet.name == 'Summary':
                for col in range(worksheet.ncols):
                    cell = 0
                    key = str(worksheet.cell_value(cell, col)).lower().replace(' ', '_')
                    if key == '':
                        cell = 1
                        key = str(worksheet.cell_value(cell, col)).lower().replace(' ', '_')
                    key = key.replace('#', '')

                    if key == 'monkey':
                        keys[key] = 'INT PRIMARY KEY'
                    elif key == 'age' or key == 'weight' or key == 'iop_right' or key == 'iop_left':
                        keys[key] = 'INT'
                    elif key == 'animal_id' or key == 'sex' or key == 'condition' or key == 'comments':
                        keys[key] = 'TEXT'
                    elif key == 'date_of_birth':
                        keys[key] = 'DATE'
        return keys