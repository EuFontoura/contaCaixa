import win32print

printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL)
for printer in printers:
    print(printer[2])