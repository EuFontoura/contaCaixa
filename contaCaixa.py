import customtkinter as ctk
from tkinter import messagebox, StringVar
from customtkinter import CTkToplevel
import datetime, win32print

# ======== UTIL ======== #
def brl(v: float) -> str:
    s = f"{v:,.2f}"
    return "R$ " + s.replace(",", "X").replace(".", ",").replace("X", ".")

def parse_int(text: str) -> int:
    text = (text or "").strip()
    return int(text) if text.isdigit() else 0

def only_digits(new_value: str) -> bool:
    return new_value.isdigit() or new_value == ""

# ======== CONFIGURAÇÕES ======== #
printer_name = "ELGIN i9(USB)"
margens = {"top": 0, "bottom": 0, "left": 0, "right": 0}

def abrir_configuracoes():
    global printer_name, margens

    top = ctk.CTkToplevel(app)
    top.title("Configurações de Impressão")
    top.geometry("400x320")
    top.grab_set()

    impressoras = [p[2] for p in win32print.EnumPrinters(2)]
    impressora_var = StringVar(value=printer_name)

    ctk.CTkLabel(top, text="Selecione a Impressora:", font=("Arial", 14)).pack(pady=(10, 4))
    impressora_menu = ctk.CTkOptionMenu(top, values=impressoras, variable=impressora_var, width=250)
    impressora_menu.pack(pady=6)
    
    frame_margens = ctk.CTkFrame(top, corner_radius=10)
    frame_margens.pack(fill="x", padx=10, pady=10)

    ctk.CTkLabel(frame_margens, text="Margens (mm)", font=("Arial", 13, "bold")).grid(row=0, column=0, columnspan=2, pady=6)

    margin_vars = {}
    for i, (nome, key) in enumerate([("Superior", "top"), ("Inferior", "bottom"), ("Esquerda", "left"), ("Direita", "right")]):
        var = StringVar(value=str(margens[key]))
        margin_vars[key] = var
        ctk.CTkLabel(frame_margens, text=nome + ":", font=("Arial", 12)).grid(row=i+1, column=0, sticky="e", padx=6, pady=3)
        ctk.CTkEntry(frame_margens, width=80, textvariable=var, justify="right").grid(row=i+1, column=1, padx=6, pady=3)

    def salvar():
        global printer_name, margens
        printer_name = impressora_var.get()
        for k, var in margin_vars.items():
            margens[k] = parse_int(var.get())
        messagebox.showinfo("Configurações", "Configurações salvas com sucesso!")
        top.destroy()

    ctk.CTkButton(top, text="Salvar", command=salvar).pack(pady=8)

# ======== IMPRESSÃO ======== #
def imprimir_recibo(total: float):
    agora = datetime.datetime.now()
    data_formatada = agora.strftime("%d/%m/%Y %H:%M:%S")
    recibo = f"\nTotal Caixa:\n{brl(total)}\n\nData:\n{data_formatada}\n"

    recibo = ("\n" * margens["top"]) + (" " * margens["left"]) + recibo
    recibo += ("\n" * margens["bottom"])

    try:
        hprinter = win32print.OpenPrinter(printer_name)
        win32print.StartDocPrinter(hprinter, 1, ("Recibo", None, "RAW"))
        win32print.StartPagePrinter(hprinter)
        win32print.WritePrinter(hprinter, recibo.encode("cp1252"))
        win32print.WritePrinter(hprinter, b"\n\n\n\n\n\n")
        win32print.WritePrinter(hprinter, b"\x1D\x56\x00")
        win32print.EndPagePrinter(hprinter)
        win32print.EndDocPrinter(hprinter)
        win32print.ClosePrinter(hprinter)
        messagebox.showinfo("Impressão", "Recibo enviado para a impressora.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao imprimir: {e}")

# ======== APP ======== #
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Contagem de Caixa")
largura = 400
altura = 640

screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

x = (screen_width - largura) // 2
y = (screen_height - altura) // 3

app.geometry(f"{largura}x{altura}+{x}+{y}")
app.minsize(380, 620)

topbar = ctk.CTkFrame(app, fg_color="transparent")
topbar.pack(fill="x", padx=10, pady=(6,0))

ctk.CTkButton(topbar, text="Configurações de Impressão", command=abrir_configuracoes, width=190).pack(side="right", padx=4)

main = ctk.CTkFrame(app, corner_radius=12)
main.pack(padx=10, pady=10, fill="both", expand=True)

header = ctk.CTkLabel(main, text="💰 Contagem de Caixa", font=("Arial", 20, "bold"))
header.pack(pady=(10, 8))

content = ctk.CTkFrame(main, corner_radius=10)
content.pack(fill="both", expand=True, padx=10, pady=6)
content.grid_columnconfigure(0, weight=1)
content.grid_columnconfigure(1, weight=0)

validate_cmd = app.register(only_digits)

vars_moedas, vars_notas = [], []
row_index = 0

def add_line(parent, rotulo: str, var: StringVar):
    global row_index
    lbl = ctk.CTkLabel(parent, text=rotulo, font=("Arial", 14))
    lbl.grid(row=row_index, column=0, sticky="w", pady=2, padx=(4, 6))
    ent = ctk.CTkEntry(parent, width=70, justify="right", textvariable=var,
                       validate="key", validatecommand=(validate_cmd, "%P"))
    ent.grid(row=row_index, column=1, sticky="e", pady=2, padx=(6, 4))
    row_index += 1

ctk.CTkLabel(content, text="Moedas", font=("Arial", 16, "bold")).grid(row=row_index, column=0, columnspan=2, sticky="w", pady=(6, 2), padx=4)
row_index += 1
for rot, val in [("0,05", 0.05), ("0,10", 0.10), ("0,25", 0.25), ("0,50", 0.50), ("1,00", 1.0)]:
    v = StringVar()
    add_line(content, f"{rot}", v)
    vars_moedas.append((val, v))

ctk.CTkLabel(content, text="Notas", font=("Arial", 16, "bold")).grid(row=row_index, column=0, columnspan=2, sticky="w", pady=(6, 2), padx=4)
row_index += 1
for rot, val in [("2,00", 2), ("5,00", 5), ("10,00", 10), ("20,00", 20), ("50,00", 50), ("100,00", 100)]:
    v = StringVar()
    add_line(content, f"{rot}", v)
    vars_notas.append((val, v))

# ======== FOOTER ======== #
footer = ctk.CTkFrame(main, fg_color="transparent")
footer.pack(fill="x", padx=10, pady=10)

valor_total_label = ctk.CTkLabel(footer, text="Total: R$ 0,00", font=("Arial", 18, "bold"))
valor_total_label.pack(pady=(4, 6))

def calcular_total(*_):
    total = 0.0
    for valor, var in vars_moedas + vars_notas:
        total += parse_int(var.get()) * valor
    valor_total_label.configure(text=f"Total: {brl(total)}")
    return total

for _, v in vars_moedas + vars_notas:
    v.trace_add("write", calcular_total)

def on_imprimir():
    total = calcular_total()
    if total <= 0 and not messagebox.askyesno("Imprimir", "Total é zero. Deseja imprimir mesmo assim?"):
        return
    imprimir_recibo(total)

buttons_frame = ctk.CTkFrame(footer, fg_color="transparent")
buttons_frame.pack(pady=6)

ctk.CTkButton(
    buttons_frame,
    text="Apagar Campos",
    command=lambda: [v.set("") for _, v in vars_moedas + vars_notas],
    fg_color="red",
    hover_color="#a60000", 
    width=160
).grid(row=0, column=0, padx=(0, 8))

ctk.CTkButton(
    buttons_frame,
    text="Imprimir Recibo",
    command=on_imprimir,
    width=160
).grid(row=0, column=1)

ctk.CTkLabel(footer, text="Dica: use apenas números inteiros nas quantidades.", font=("Arial", 11)).pack(pady=(2, 6))

calcular_total()
app.mainloop()
