import tkinter as tk
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def criar_recibo(produto, largura, comprimento, valor):
    conteudo_recibo = f"Produto: {produto}\nLargura: {largura}\nComprimento: {comprimento}\nTotal a pagar: R${valor:.2f}"
    c = canvas.Canvas("recibo.pdf", pagesize=letter)
    c.drawString(100, 750, "Recibo")
    c.drawString(100, 730, "____________________")
    y_position = 700
    for line in conteudo_recibo.split('\n'):
        c.drawString(100, y_position, line)
        y_position -= 20  # Ajuste para a próxima linha
    c.save()

# Definindo as variáveis globais
global produto, largura, comprimento, valor

def salvar_recibo():
    criar_recibo(produto, largura, comprimento, valor)

def calcular_pagamento():
    global produto, largura, comprimento, valor
    largura = float(entry_largura.get())
    comprimento = float(entry_comprimento.get())
    valor_pagar = largura * comprimento * float(valor_por_unidade.get())
    if acabamento.get() == 1:
        valor_pagar += float(valor_acabamento.get())
    valor = valor_pagar  # Definindo o valor global
    label_total["text"] = f"Total a pagar: R${valor_pagar:.2f}\nProduto: {entry_produto.get()}"

def criar_interface_grafica():
    root = tk.Tk()
    root.title("GRAN BRASIL - Pedra e Granitos")
    root.geometry("800x600")

    
    global valor_por_unidade
    valor_por_unidade = tk.DoubleVar()
    valor_por_unidade.set(600)

    global valor_acabamento
    valor_acabamento = tk.DoubleVar()
    valor_acabamento.set(2000)

    # ICONE DA INTERFACE
    icon = tk.PhotoImage(file='./logo2.png')
    root.iconphoto(False, icon)

    # Frame para a logo de fundo
    frame_logo_fundo = tk.Frame(root)
    frame_logo_fundo.pack(expand=True, pady=10) 

    logo_fundo = tk.PhotoImage(file="./logo.png")
    logo_fundo = logo_fundo.subsample(3)
    label_logo_fundo = tk.Label(frame_logo_fundo, image=logo_fundo)
    label_logo_fundo.pack()

    # Frame para as perguntas
    frame_perguntas = tk.Frame(root)
    frame_perguntas.pack(expand=True, padx=20, pady=0.5)

    label_produto = tk.Label(frame_perguntas, text="Produto:", padx=10)
    label_produto.pack()

    global entry_produto
    entry_produto = tk.Entry(frame_perguntas)
    entry_produto.pack(padx=10, pady=5)

    label_largura = tk.Label(frame_perguntas, text="Largura:", padx=10)
    label_largura.pack()

    global entry_largura
    entry_largura = tk.Entry(frame_perguntas)
    entry_largura.pack(padx=10, pady=5)

    label_comprimento = tk.Label(frame_perguntas, text="Comprimento:", padx=10)
    label_comprimento.pack()

    global entry_comprimento
    entry_comprimento = tk.Entry(frame_perguntas)
    entry_comprimento.pack(padx=10, pady=5)

    global acabamento
    acabamento = tk.IntVar()
    check_acabamento = tk.Checkbutton(frame_perguntas, text="Acabamento", variable=acabamento)
    check_acabamento.pack()

    button_calcular = tk.Button(frame_perguntas, text="Calcular Valor a Pagar", command=calcular_pagamento)
    button_calcular.pack(pady=10)

    global label_total
    label_total = tk.Label(root, text="Texto do recibo")
    label_total.pack()

    button_salvar = tk.Button(root, text="Salvar Recibo", command=salvar_recibo)
    button_salvar.pack()

    root.mainloop()

criar_interface_grafica()
