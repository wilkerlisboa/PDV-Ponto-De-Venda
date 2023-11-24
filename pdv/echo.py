import tkinter as tk
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
import subprocess

# Lista para armazenar os produtos no carrinho
carrinho = []

# Variáveis de opções
opcoes_acabamento = ["Saia", "Furo de Boca", "Furo de Copa", "Roda Pe", "Furo Lateral"]
opcoes_quantidade = ["1x", "2x", "3x", "4x", "5x"]

# Função para calcular o pagamento
def calcular_pagamento():
    try:
        global valor_por_unidade
        largura = float(entry_largura.get())
        comprimento = float(entry_comprimento.get())
        quantidade_valor = int(quantidade.get().split("x")[0])

        # Verifica se os campos contêm valores numéricos
        if not (largura > 0 and comprimento > 0 and quantidade_valor > 0):
            raise ValueError("Insira valores válidos para largura, comprimento e quantidade.")

        valor_por_unidade_float = float(valor_por_unidade.get())

        valor_pagar = largura * comprimento * valor_por_unidade_float * quantidade_valor

        # Se houver acabamento e valor de acabamento, adicione ao valor a pagar
        if acabamento.get() == opcoes_acabamento[0]:
            valor_acabamento = float(valor_acabamento_entry.get()) if valor_acabamento_entry.get() else 0
            valor_pagar += valor_acabamento

        produto = entry_produto.get()
        label_total.config(text=f"Total a pagar: R$ {valor_pagar:.2f} - Produto: {produto} - Quantidade: {quantidade.get()}")
    except ValueError as e:
        label_total.config(text=f"Erro: {str(e)}")


# Função para adicionar ao carrinho
def adicionar_ao_carrinho():
    try:
        produto = entry_produto.get()
        largura = float(entry_largura.get())
        comprimento = float(entry_comprimento.get())
        quantidade_valor = int(quantidade.get().split("x")[0])

        # Verifica se os campos contêm valores numéricos
        if not (largura > 0 and comprimento > 0 and quantidade_valor > 0):
            raise ValueError("Insira valores válidos para largura, comprimento e quantidade.")

        valor_acabamento = 0
        if acabamento.get() == opcoes_acabamento[0]:
            valor_acabamento_entry_value = valor_acabamento_entry.get()
            valor_acabamento = float(valor_acabamento_entry_value) if valor_acabamento_entry_value else 0

        valor_por_unidade_float = float(valor_por_unidade.get())
        valor_pagar = largura * comprimento * valor_por_unidade_float * quantidade_valor + valor_acabamento

        carrinho.append({
            "produto": produto,
            "largura": largura,
            "comprimento": comprimento,
            "valor": valor_pagar,
            "quantidade": quantidade_valor,
            "acabamento": acabamento.get()
        })

        entry_produto.delete(0, tk.END)
        entry_largura.delete(0, tk.END)
        entry_comprimento.delete(0, tk.END)
        quantidade.set(opcoes_quantidade[0])
        acabamento.set(opcoes_acabamento[0])

        if 'valor_acabamento_entry' in globals() and valor_acabamento_entry is not None:
            valor_acabamento_entry.delete(0, tk.END)

        label_total.config(text="Total a pagar: R$ 0.00 - Produto: N/A")
    except ValueError as e:
        label_total.config(text=f"Erro: {str(e)}")


# Função para gerar recibo do carrinho
def gerar_recibo_carrinho():
    if not carrinho:
        print("Carrinho vazio. Adicione produtos antes de gerar o recibo.")
        return

    # Cria o recibo com todos os produtos no carrinho
    nome_arquivo = "recibo_carrinho.pdf"
    caminho_pdf = os.path.abspath(nome_arquivo)
    c = canvas.Canvas(nome_arquivo, pagesize=letter)

    y_position = 750
    for item in carrinho:
        # Adiciona uma linha no final
        c.drawString(100, y_position, "______________________________")
        y_position -= 20
        c.drawString(100, y_position, f"Produto: ..............................{item['produto']}")
        y_position -= 20
        c.drawString(100, y_position, f"Quantidade: ...........................{item['quantidade']}")
        y_position -= 20
        c.drawString(100, y_position, f"Acabamento: ...........................{item['acabamento']}")
        y_position -= 20
        c.drawString(100, y_position, f"Largura: ..............................{item['largura']} cm")
        y_position -= 20
        c.drawString(100, y_position, f"Comprimento: ...........................{item['comprimento']} cm")
        y_position -= 20
        c.drawString(100, y_position, f"Total a pagar: .........................R$ {item['valor']}")
        y_position -= 30  # Adiciona espaço entre os produtos

    # Adiciona uma linha no final
    c.drawString(100, y_position, "______________________________")
    y_position -= 20

    # Adiciona um salmo em várias linhas
    c.drawString(100, y_position, "O Senhor é meu pastor, nada me faltará.")
    y_position -= 20
    c.drawString(100, y_position, "- Salmo 23:1")

    c.save()

    # Limpa o carrinho após gerar o recibo
    carrinho.clear()
    print(f"Recibo gerado com sucesso: {caminho_pdf}")
    # Abre o arquivo PDF com o leitor padrão
    subprocess.Popen([caminho_pdf], shell=True)

# Criação da janela principal
root = tk.Tk()
root.title("GRAN BRASIL - Pedra e Granitos")

# Configurar o posicionamento com o grid
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Frame principal usando grid
frame_principal = tk.Frame(root)
frame_principal.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")  # sticky="nsew" para centralizar

# ICONE DA INTERFACE
icon = tk.PhotoImage(file='./logo2.png')
root.iconphoto(False, icon)

# Frame do logo
frame_logo = tk.Frame(frame_principal)
frame_logo.grid(row=0, column=0, pady=5)  # Centraliza a logo

# Logo
logo_fundo = tk.PhotoImage(file="./logo.png")
logo_fundo = logo_fundo.subsample(2)
label_logo_fundo = tk.Label(frame_logo, image=logo_fundo)
label_logo_fundo.grid(row=0, column=2, pady=5)  # Centraliza a logo

# Frame para os campos de produto
frame_produto = tk.Frame(frame_principal)
frame_produto.grid(row=0, column=2, pady=10, sticky="nsew")  # Adiciona sticky="nsew" para centralizar

# Campos para adicionar produto
label_produto = tk.Label(frame_produto, text="Produto:")
label_produto.grid(row=0, column=0, pady=5, padx=10, sticky="w")

entry_produto = tk.Entry(frame_produto)
entry_produto.grid(row=1, column=0, pady=5, padx=10)

label_largura = tk.Label(frame_produto, text="Largura:")
label_largura.grid(row=2, column=0, pady=5, sticky="w")

entry_largura = tk.Entry(frame_produto)
entry_largura.grid(row=3, column=0, pady=5, padx=10)

label_comprimento = tk.Label(frame_produto, text="Comprimento:")
label_comprimento.grid(row=4, column=0, pady=5, sticky="w")

entry_comprimento = tk.Entry(frame_produto)
entry_comprimento.grid(row=5, column=0, pady=5, padx=10)

# Opções de quantidade
label_quantidade = tk.Label(frame_produto, text="Quantidade:")
label_quantidade.grid(row=0, column=1, pady=5, padx=10, sticky="w")

quantidade = tk.StringVar()
quantidade.set(opcoes_quantidade[0])
menu_quantidade = tk.OptionMenu(frame_produto, quantidade, *opcoes_quantidade)
menu_quantidade.grid(row=1, column=1, pady=5, padx=10)

# Opções de acabamento
label_acabamento = tk.Label(frame_produto, text="Acabamento:")
label_acabamento.grid(row=2, column=1, pady=5, padx=10, sticky="w")

acabamento = tk.StringVar()
acabamento.set(opcoes_acabamento[0])
menu_acabamento = tk.OptionMenu(frame_produto, acabamento, *opcoes_acabamento)
menu_acabamento.grid(row=3, column=1, pady=5, padx=10)

# Rótulo para mostrar o valor por unidade
label_valor_por_unidade = tk.Label(frame_produto, text="Valor por Unidade:")
label_valor_por_unidade.grid(row=4, column=1, pady=5, padx=10, sticky="w")

# Botão de opção para o valor por unidade
valor_por_unidade = tk.StringVar()
valor_por_unidade.set("10.00")  # Valor inicial
opcao_valor_por_unidade = tk.OptionMenu(frame_produto, valor_por_unidade, "10.00", "15.00", "20.00")  # Adicione mais opções conforme necessário
opcao_valor_por_unidade.grid(row=5, column=1, pady=5, padx=10)

# Opções de pagamento
label_pagamento = tk.Label(frame_produto, text="Pagamento:")
label_pagamento.grid(row=6, column=1, pady=5, padx=10, sticky="w")

opcoes_pagamento = ["Dinheiro", "Cartão de Crédito", "Cartão de Débito", "PIX"]
pagamento = tk.StringVar()
pagamento.set(opcoes_pagamento[0])
menu_pagamento = tk.OptionMenu(frame_produto, pagamento, *opcoes_pagamento)
menu_pagamento.grid(row=7, column=1, pady=5, padx=10)

# Botões para calcular, adicionar ao carrinho e gerar recibo
button_calcular = tk.Button(frame_produto, text="Calcular Valor a Pagar", command=calcular_pagamento)
button_calcular.grid(row=8, column=0, columnspan=2, pady=10, padx=10)

label_total = tk.Label(frame_produto, text="Total a pagar: R$ 0.00 - Produto: N/A")
label_total.grid(row=9, column=0, columnspan=2, pady=5, padx=10)

# Organizando os botões usando grid
frame_botoes = tk.Frame(frame_principal)
frame_botoes.grid(row=1, column=0, columnspan=2, pady=5, sticky="nsew")  # Adicionei sticky="nsew" para centralizar

button_adicionar_carrinho = tk.Button(frame_botoes, text="Adicionar ao Carrinho", command=adicionar_ao_carrinho)
button_adicionar_carrinho.grid(row=0, column=0, padx=5)

button_gerar_recibo_carrinho = tk.Button(frame_botoes, text="Gerar Recibo do Carrinho", command=gerar_recibo_carrinho)
button_gerar_recibo_carrinho.grid(row=0, column=1, padx=5)

# Inicia o loop principal
root.mainloop()
