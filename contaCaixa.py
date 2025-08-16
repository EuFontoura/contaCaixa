import datetime
import win32print

def imprimir_recibo(total):
    agora = datetime.datetime.now()
    data_formatada = agora.strftime("%d/%m/%Y %H:%M:%S")

    recibo = f"""
Total Caixa:
R$ {total:.2f}

Data:
{data_formatada}
"""

    try:
        printer_name = "ELGIN i9(USB)"
        hprinter = win32print.OpenPrinter(printer_name)
        hprinter_dc = win32print.StartDocPrinter(hprinter, 1, ("Recibo", None, "RAW"))
        win32print.StartPagePrinter(hprinter)

        # Envia o texto
        win32print.WritePrinter(hprinter, recibo.encode("cp437"))

        # Dá avanço de papel (5 linhas) e corta
        win32print.WritePrinter(hprinter, b"\n\n\n\n\n")  
        win32print.WritePrinter(hprinter, b"\x1D\x56\x00")  # comando ESC/POS: corte total

        win32print.EndPagePrinter(hprinter)
        win32print.EndDocPrinter(hprinter)
        win32print.ClosePrinter(hprinter)

        print("Recibo enviado para a impressora.")
    except Exception as e:
        print("Erro ao imprimir:", e)


total = 0

moeda5 = int(input("Insira quantidade de moedas de 0,05: "))
total += moeda5 * 0.05

moeda10 = int(input("Insira quantidade de moedas de 0,10: "))
total += moeda10 * 0.10

moeda25 = int(input("Insira quantidade de moedas de 0,25: "))
total += moeda25 * 0.25

moeda50 = int(input("Insira quantidade de moedas de 0,50: "))
total += moeda50 * 0.50

moeda1 = int(input("Insira quantidade de moedas de 1,00: "))
total += moeda1 * 1

print(f"Subtotal (moedas): R${total:.2f}")

while True:
    continuar = input("Deseja contar as notas também? (S/N): ").strip().upper()
    
    if continuar == "S":
        nota2 = int(input("Insira quantidade de notas de 2,00: "))
        total += nota2 * 2
        
        nota5 = int(input("Insira quantidade de notas de 5,00: "))
        total += nota5 * 5
        
        nota10 = int(input("Insira quantidade de notas de 10,00: "))
        total += nota10 * 10
        
        nota20 = int(input("Insira quantidade de notas de 20,00: "))
        total += nota20 * 20
        
        nota50 = int(input("Insira quantidade de notas de 50,00: "))
        total += nota50 * 50
        
        nota100 = int(input("Insira quantidade de notas de 100,00: "))
        total += nota100 * 100
        
        print(f"Total final: R${total:.2f}")
        break

    elif continuar == "N":
        print(f"Total final (somente moedas): R${total:.2f}")
        break

    else:
        print("Entrada inválida. Digite apenas 'S' ou 'N'.")

while True:
    imprimir = input("Deseja imprimir o total? (S/N): ").strip().upper()
    if imprimir == "S":
        imprimir_recibo(total)
        break
    elif imprimir == "N":
        print("Ok, encerrando sem imprimir.")
        break
    else:
        print("Entrada inválida. Digite apenas 'S' ou 'N'.")
