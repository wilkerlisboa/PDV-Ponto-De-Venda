import tkinter as tk
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
import subprocess

try:
    import win32print
except ImportError:
    win32print = None

def calcular_pagamento():
    try:
        largura = float(entry_largura.get())
        comprimento = float(entry_comprimento.get())
        quantidade_valor = int(quantidade.get().split("x")[0])
        valor_pagar = largura * comprimento * float(valor_por_unidade.get()) * quantidade_valor
        if acabamento.get() == "Sim":
            valor_pagar += float(valor_acabamento.get())
        produto = entry_produto.get()
        label_total["text"] = f"Total a pagar: R$ {valor_pagar:.2f}\nProduto: {produto}\nQuantidade: {quantidade.get()}"
    except ValueError:
        label_total["text"] = "Erro: Insira valores válidos para largura, comprimento e valor por unidade."

def salvar_recibo():
    produto = entry_produto.get()
    largura = entry_largura.get()
    comprimento = entry_comprimento.get()
    valor = label_total["text"].split(":")[1].split(" -")[0].strip()
    arquivo_pdf = criar_recibo(produto, largura, comprimento, valor, quantidade.get(), acabamento.get())

    abrir_pdf_com_leitor_padrao(arquivo_pdf)

    if win32print:
        imprimir_pdf_no_windows(arquivo_pdf)

def abrir_pdf_com_leitor_padrao(arquivo_pdf):
    try:
        subprocess.run(["start", arquivo_pdf], shell=True)
    except Exception as e:
        print(f"Erro ao abrir o PDF: {e}")

def imprimir_pdf_no_windows(arquivo_pdf):
    try:
        impressora_padrao = win32print.GetDefaultPrinter()
        hPrinter = win32print.OpenPrinter(impressora_padrao)
        hJob = win32print.StartDocPrinter(hPrinter, 1, ("Recibo", None, "RAW"))

        with open(arquivo_pdf, "rb") as pdf_file:
            win32print.StartPagePrinter(hPrinter)
            win32print.WritePrinter(hPrinter, pdf_file.read())
            win32print.EndPagePrinter(hPrinter)

        win32print.EndDocPrinter(hPrinter)
        win32print.ClosePrinter(hPrinter)

        print("Impressão concluída.")
    except Exception as e:
        print(f"Erro ao imprimir o PDF: {e}")

def criar_recibo(produto, largura, comprimento, valor, quantidade, acabamento):
    nome_arquivo = f"recibo_{produto.replace(' ', '_')}.pdf"
    conteudo_recibo = f"Produto: ................................{produto}\nQuantidade: ..........................{quantidade}\nAcabamento: .........................{acabamento}\nLargura: .................................{largura} cm\nComprimento: ........................{comprimento} cm\nTotal a pagar: ........................{valor}\n______________________________\nO Senhor é meu pastor, nada me faltará.\n-Salmo 23:1"
    caminho_pdf = os.path.abspath(nome_arquivo)
    c = canvas.Canvas(nome_arquivo, pagesize=letter)
    c.drawString(100, 750, "Recibo")
    c.drawString(100, 730, "______________________________")
    y_position = 700
    for line in conteudo_recibo.split('\n'):
        c.drawString(100, y_position, line)
        y_position -= 20
    c.save()

    return caminho_pdf

root = tk.Tk()
root.title("GRAN BRASIL - Pedra e Granitos")
root.geometry("800x600")

valor_por_unidade = tk.DoubleVar()
valor_por_unidade.set(600)

valor_acabamento = tk.DoubleVar()
valor_acabamento.set(2000)

frame_logo_fundo = tk.Frame(root)
frame_logo_fundo.pack(expand=True, pady=10)

logo_fundo = tk.PhotoImage(file="./logo.png")
logo_fundo = logo_fundo.subsample(3)
label_logo_fundo = tk.Label(frame_logo_fundo, image=logo_fundo)
label_logo_fundo.pack()

frame = tk.Frame(root)
frame.pack(expand=True, padx=20, pady=10)

label_produto = tk.Label(frame, text="Produto:")
label_produto.grid(row=0, column=0, sticky="E", padx=(10, 0))

entry_produto = tk.Entry(frame)
entry_produto.grid(row=0, column=1, padx=10, pady=5)

label_quantidade = tk.Label(frame, text="Quantidade:")
label_quantidade.grid(row=0, column=2, sticky="E", padx=(10, 0))

opcoes_quantidade = ["1x", "2x", "3x", "4x", "5x"]
quantidade = tk.StringVar()
quantidade.set(opcoes_quantidade[0])
menu_quantidade = tk.OptionMenu(frame, quantidade, *opcoes_quantidade)
menu_quantidade.grid(row=0, column=3, padx=10, pady=5)

label_acabamento = tk.Label(frame, text="Acabamento:")
label_acabamento.grid(row=2, column=2, sticky="E", padx=(10, 0))

opcoes_acabamento = ["Saia", "Furo de Boca", "Furo de Copa", "Roda Pe", "Furo Lateral"]
acabamento = tk.StringVar()
acabamento.set(opcoes_acabamento[0])
menu_acabamento = tk.OptionMenu(frame, acabamento, *opcoes_acabamento)
menu_acabamento.grid(row=2, column=3, padx=10, pady=9)

label_largura = tk.Label(frame, text="Largura:")
label_largura.grid(row=1, column=0, sticky="E", padx=(10, 0))

entry_largura = tk.Entry(frame)
entry_largura.grid(row=1, column=1, padx=10, pady=5)

label_comprimento = tk.Label(frame, text="Comprimento:")
label_comprimento.grid(row=2, column=0, sticky="E", padx=(10, 0))

entry_comprimento = tk.Entry(frame)
entry_comprimento.grid(row=2, column=1, padx=10, pady=5)

button_calcular = tk.Button(frame, text="Calcular Valor a Pagar", command=calcular_pagamento)
button_calcular.grid(row=4, column=0, columnspan=2, pady=10)

label_total = tk.Label(frame, text="Total a pagar: R$ 0.00\nProduto: N/A\n", font=("Arial", 13))
label_total.grid(row=5, column=0, columnspan=2, pady=10)

button_salvar = tk.Button(frame, text="Salvar Recibo", command=salvar_recibo)
button_salvar.grid(row=6, column=0, columnspan=2, pady=10)

root.mainloop()
