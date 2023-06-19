from tkinter import *
from tkinter import messagebox, PhotoImage
import banco as banco
import tkinter as tk
from tkinter import ttk
import sqlite3

def registrar_Cadastro(name, usuario, password):
    # Pegar informações para o Banco
    NameBanco = name
    UsuarioBanco = usuario
    PasswordBanco = password

    if NameBanco == "" or UsuarioBanco == "" or PasswordBanco == "":
        messagebox.showerror(title="Erro de Registro", message="Preencha todos os Campos")
    elif verificar_usuario_existente(UsuarioBanco):
        messagebox.showerror(title="Erro de Registro", message="Nome de usuário já existente.")

    else:
        # Inserir no Banco
        banco.cursor.execute("""
        INSERT INTO Users(Name, Usuario, Password) VALUES(?, ?, ?)
        """, (NameBanco, UsuarioBanco, PasswordBanco))
        banco.conn.commit()
        messagebox.showinfo(title="Conta criada", message="Cadastrado(a) com sucesso!")

def verificar_usuario_existente(UsuarioBanco):  
    conn = sqlite3.connect('UserData.db')
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM Users WHERE Usuario = ?", (UsuarioBanco,))
    resultado = cursor.fetchone()
   
    cursor.close()
    conn.close()

    if resultado[0] > 0:
        return True
    else:
        return False

def acessando_Login():
   
    UsuarioLogin = userF.get()
    PasswordLogin = passwordF.get()

    banco.cursor.execute("""
    SELECT * FROM Users
    WHERE Usuario = ? AND Password = ?
    """,(UsuarioLogin, PasswordLogin))
    VerificarLogin = banco.cursor.fetchone()
    try:
        if(UsuarioLogin in VerificarLogin and PasswordLogin in VerificarLogin):
            messagebox.showinfo(title="Login", message="Seja Bem-vindo!")

            login.destroy()
#   ~~~~~ TELA DE MENU ~~~~~
            app = tk.Tk()
            app.geometry("300x300+100+100")
            app.geometry("600x400")      
            app.title("Menu")
            app.configure(bg='#0b2e3b')
            imagem = tk.PhotoImage(file="menu.png")
            w = tk.Label(app, image=imagem, width=600, height=400)
            w.imagem = imagem
            w.pack()

            barraDeMenus = Menu(app)
            menuContatos = Menu(barraDeMenus, tearoff=0)
            menuContatos.add_command(label="Fazer pedido", command=fazer_pedido)
            menuContatos.add_command(label="Cadastrar", command=cadastrarUsers)
            menuContatos.add_separator()
           

            menuContatos.add_command(label="Sair", command=exit)
            barraDeMenus.add_cascade(label="Menu", menu=menuContatos)
            app.config(menu=barraDeMenus)


    except:
            messagebox.showerror(title="Conta não encontrada", message="Certifique-se que já está cadastrado! ")

   
    mainloop()

def fazer_pedido():
                root = Tk()
                root.title("Pedidos")
                root.geometry("300x300+100+100")
                root.geometry("1100x600")
                my_tree = ttk.Treeview(root)
                root.configure(bg="#F0F0F0")
                storeName = "Cadastre seus pedidos"

                # Create a connection to the database
                conn = sqlite3.connect("pedido.db")

                # Create a cursor
                cursor = conn.cursor()

                # Create table if it doesn't exist
                cursor.execute("CREATE TABLE IF NOT EXISTS PEDIDOS (id INTEGER PRIMARY KEY AUTOINCREMENT, Nome TEXT, valor TEXT, forma TEXT, Pedido TEXT, Quantidade INTEGER)")

                def insert(nome, valor, forma, pedido, quantidade):
                    cursor.execute("INSERT INTO PEDIDOS (Nome, valor, forma, Pedido, Quantidade) VALUES (?, ?, ?, ?, ?)", (nome, valor, forma, pedido, quantidade))
                    conn.commit()

                def read():
                    cursor.execute("SELECT * FROM PEDIDOS")
                    results = cursor.fetchall()
                    return results

                def delete(data):
                    cursor.execute("DELETE FROM PEDIDOS WHERE id = ?", (data,))
                    conn.commit()

                def update(data, nome, valor, forma, pedido, quantidade):
                    cursor.execute("UPDATE PEDIDOS SET Nome = ?, valor = ?, forma = ?, Pedido = ?, Quantidade = ? WHERE id = ?", (nome, valor, forma, pedido, quantidade, data))
                    conn.commit()

                def reverse(data):
                    return data[::-1]

                # Treeview
                my_tree = ttk.Treeview(root)
                my_tree.grid(row=1, column=5, columnspan=4, rowspan=5, padx=10, pady=10)

                # Function to insert data
                def insert_data():
                    itemNome = entryNome.get()
                    itemvalor = entryvalor.get()
                    itemforma = entryforma.get()
                    itempedido = entrypedido.get()
                    itemquantidade = entryquantidade.get()

                    if itemNome and itemvalor and itemforma and itempedido and itemquantidade:
                        insert(itemNome, itemvalor, itemforma, itempedido, itemquantidade)
                        entryNome.delete(0, END)
                        entryvalor.delete(0, END)
                        entryforma.delete(0, END)
                        entrypedido.delete(0, END)
                        entryquantidade.delete(0, END)
                        display_data()

                # Function to delete data
                def delete_data():
                    selected_item = my_tree.selection()
                    for item in selected_item:
                        delete(item)
                    display_data()

                # Function to update data
                def update_data():
                    selected_item = my_tree.selection()
                    for item in selected_item:
                        data = my_tree.item(item, "values")[0]
                        itemNome = entryNome.get()
                        itemvalor = entryvalor.get()
                        itemforma = entryforma.get()
                        itempedido = entrypedido.get()
                        itemquantidade = entryquantidade.get()
                        if itemNome and itemvalor and itemforma and itempedido and itemquantidade:
                            update(data, itemNome, itemvalor, itemforma, itempedido, itemquantidade)
                            entryNome.delete(0, END)
                            entryvalor.delete(0, END)
                            entryforma.delete(0, END)
                            entrypedido.delete(0, END)
                            entryquantidade.delete(0, END)
                            display_data()

                def on_treeview_double_click(event):
                    selected_item = my_tree.focus()  # Obter o item selecionado
                    values = my_tree.item(selected_item, "values")  # Obter os valores da linha selecionada

                    # Preencher as caixas de texto com os valores da linha selecionada
                    entryNome.delete(0, END)
                    entryNome.insert(0, values[1])  # Nome
                    entryvalor.delete(0, END)
                    entryvalor.insert(0, values[2])  # Valor
                    entryforma.delete(0, END)
                    entryforma.insert(0, values[3])  # Forma de pagamento
                    entrypedido.delete(0, END)
                    entrypedido.insert(0, values[4])  # Pedido
                    entryquantidade.delete(0, END)
                    entryquantidade.insert(0, values[5])  # Quantidade

                my_tree.bind("<Double-1>", on_treeview_double_click)  # Vincular o evento de clique duplo ao Treeview
                
                def cozinha():
                    def mark_order_ready(event):
                            selected_item = my_tree.focus()
                            my_tree.item(selected_item, values=("Pronto",))
                            coz.event_generate("<<PedidoPronto>>", when="tail")  # Acionar evento de pedido pronto
                        
                    def on_pedido_pronto(event):
                            messagebox.showinfo("Pedido Pronto", "Um pedido está pronto para entrega!")
                        
                    def update_orders():
                            # Aqui você pode adicionar a lógica para verificar se há novos pedidos
                            # e atualizar a tabela da cozinha em conformidade
                            display_data()
                            coz.after(5000, update_orders)  # Atualiza a cada 5 segundos (5000 ms)

                    coz = tk.Tk()
                    coz.title("Tela da Cozinha")

                    # Criar Treeview
                    my_tree = ttk.Treeview(coz)
                    my_tree['columns'] = ("ID", "Nome", "Valor", "Forma de pg", "Pedido", "Quantidade")
                    my_tree.column("#0", width=0, stretch=tk.NO)
                    my_tree.column("ID", anchor=tk.W, width=100)
                    my_tree.column("Nome", anchor=tk.W, width=150)
                    my_tree.column("Valor", anchor=tk.W, width=150)
                    my_tree.column("Forma de pg", anchor=tk.W, width=150)
                    my_tree.column("Pedido", anchor=tk.W, width=150)
                    my_tree.column("Quantidade", anchor=tk.W, width=150)
                    
                    my_tree.heading("ID", text="ID", anchor=tk.W)
                    my_tree.heading("Nome", text="Nome", anchor=tk.W)
                    my_tree.heading("Valor", text="Valor", anchor=tk.W)
                    my_tree.heading("Forma de pg", text="Forma de pg", anchor=tk.W)
                    my_tree.heading("Pedido", text="Pedido", anchor=tk.W)
                    my_tree.heading("Quantidade", text="Quantidade", anchor=tk.W)

                    # Adicionar dados à tabela
                    def display_data():
                        for data in my_tree.get_children():
                            my_tree.delete(data)

                        results = reverse(read())

                        for result in results:
                            my_tree.insert(parent='', index='end', iid=result[0], text="", values=result, tag="orow")

                        my_tree.tag_configure('orow', background='#EEEEEE')
                        my_tree.grid(row=1, column=5, columnspan=4, rowspan=5, padx=10, pady=10)

                    display_data()
                    
                    # Configurar evento de duplo clique para marcar pedido como pronto
                    my_tree.bind("<Double-1>", mark_order_ready)
                    coz.bind("<<PedidoPronto>>", on_pedido_pronto)
                    coz.after(5000, update_orders)
                    coz.mainloop()

                def imprimir_nota_fiscal():
                       # Obter itens selecionados na Treeview
                    selecionados = my_tree.selection()

                    if len(selecionados) == 0:
                        messagebox.showinfo("Atenção", "Nenhum item selecionado.")
                        return

                    # Obter o nome do cliente
                    nome_cliente = entryNome.get()

                    if not nome_cliente:
                        messagebox.showinfo("Atenção", "Digite o nome do cliente.")
                        return

                    # Nome do arquivo de nota fiscal
                    nome_arquivo = f"Notas Fiscais/{nome_cliente}_nota_fiscal.txt"

                    try:
                        with open(nome_arquivo, 'w') as arquivo:
                            for item_id in selecionados:
                                # Obter valores das colunas para o item selecionado
                                valores = my_tree.item(item_id)['values']
                                linha = f"ID: {valores[0]}\nNome: {valores[1]}\nValor: {valores[2]}\nForma de pg: {valores[3]}\nPedido: {valores[4]}\nQuantidade: {valores[5]}\n\n"
                                arquivo.write(linha)

                        messagebox.showinfo("Sucesso", f"Nota fiscal salva em '{nome_arquivo}'.")
                    except IOError:
                        messagebox.showerror("Erro", "Ocorreu um erro ao criar o arquivo.")

                    
                # estrutura

                titleLabel = Label(root, text=storeName, font=('Arial bold', 30), bd=2, foreground='#F2044E', bg='#F0F0F0')
                titleLabel.grid(row=0, column=1, columnspan=8, padx=20, pady=20)

                NomeLabel = Label(root, text="Nome", font=('Arial bold', 15), foreground='#F2044E', bg='#F0F0F0')
                valorLabel = Label(root, text="Valor", font=('Arial bold', 15), foreground='#F2044E', bg='#F0F0F0')
                formaLabel = Label(root, text="Forma de pg", font=('Arial bold', 15), foreground='#F2044E', bg='#F0F0F0')
                pedidoLabel = Label(root, text="Pedido", font=('Arial bold', 15), foreground='#F2044E', bg='#F0F0F0')
                quantidadeLabel = Label(root, text="Quantidade", font=('Arial bold', 15), foreground='#F2044E', bg='#F0F0F0')
           
                NomeLabel.grid(row=1, column=0, padx=10, pady=10)
                valorLabel.grid(row=2, column=0, padx=10, pady=10)
                formaLabel.grid(row=3, column=0, padx=10, pady=10)
                pedidoLabel.grid(row=4, column=0, padx=10, pady=10)
                quantidadeLabel.grid(row=5, column=0, padx=10, pady=10)

                entryNome = Entry(root, width=25, bd=2, font=('Arial bold', 15))
                entryvalor = Entry(root, width=25, bd=2, font=('Arial bold', 15))
                entryforma = Entry(root, width=25, bd=2, font=('Arial bold', 15))
                entrypedido = Entry(root, width=25, bd=2, font=('Arial bold', 15))
                entryquantidade = Entry(root, width=25, bd=2, font=('Arial bold', 15))

                entryNome.grid(row=1, column=1, columnspan=3, padx=5, pady=5)
                entryvalor.grid(row=2, column=1, columnspan=3, padx=5, pady=5)
                entryforma.grid(row=3, column=1, columnspan=3, padx=5, pady=5)
                entrypedido.grid(row=4, column=1, columnspan=3, padx=5, pady=5)
                entryquantidade.grid(row=5, column=1, columnspan=3, padx=5, pady=5)

                buttonEnter = Button(
                    root, text="Enter", padx=5, pady=5, width=6,
                    font=('Arial', 15), foreground='white', bg="#F2044E", command=insert_data)
                buttonEnter.grid(row=7, column=1, columnspan=1)

                buttonUpdate = Button(
                    root, text="Atualizar", padx=5, pady=5, width=6,
                    font=('Arial', 15),foreground='white', bg="#F2044E", command=update_data)
                buttonUpdate.grid(row=7, column=2, columnspan=1)

                buttonDelete = Button(
                    root, text="Delete", padx=5, pady=5, width=6,
                    font=('Arial', 15),foreground='white', bg="#F2044E", command=delete_data)
                buttonDelete.grid(row=7, column=3, columnspan=1)

                buttonVoltar = Button(
                    root, text="Voltar", padx=5, pady=5, width=6,
                    font=('Arial', 15),foreground='white', bg="#F2044E", command= root.destroy)
                buttonVoltar.grid(row=8, column=1, columnspan=1)

                buttonImprimir = Button(
                    root, text="Imprimir", padx=5, pady=5, width=6,
                    font=('Arial', 15),foreground='white', bg="#F2044E", command=imprimir_nota_fiscal)
                buttonImprimir.grid(row=8, column=2, columnspan=1)

                buttonCozinha = Button(
                    root, text="Cozinha", padx=5, pady=5, width=6,
                    font=('Arial', 15),foreground='white', bg="#F2044E", command=cozinha)
                buttonCozinha.grid(row=8, column=3, columnspan=1)

                style = ttk.Style()
                style.configure("Treeview.Heading", font=('Arial bold', 15))

                my_tree['columns'] = ("ID", "Nome", "Valor", "Forma de pg", "Pedido", "Quantidade")
                my_tree.column("#0", width=0, stretch=tk.NO)
                my_tree.column("ID", anchor=tk.W, width=100)
                my_tree.column("Nome", anchor=tk.W, width=150)
                my_tree.column("Valor", anchor=tk.W, width=100)
                my_tree.column("Forma de pg", anchor=tk.W, width=100)
                my_tree.column("Pedido", anchor=tk.W, width=100)
                my_tree.column("Quantidade", anchor=tk.W, width=100)

                my_tree.heading("ID", text="ID", anchor=tk.W)
                my_tree.heading("Nome", text="Nome", anchor=tk.W)
                my_tree.heading("Valor", text="Valor", anchor=tk.W)
                my_tree.heading("Forma de pg", text="Forma de pg", anchor=tk.W)
                my_tree.heading("Pedido", text="Pedido", anchor=tk.W)
                my_tree.heading("Quantidade", text="Quantidade", anchor=tk.W)


                # Função para exibir dados no Treeview
                def display_data():
                    for data in my_tree.get_children():
                        my_tree.delete(data)

                    results = reverse(read())

                    for result in results:
                        my_tree.insert(parent='', index='end', iid=result[0], text="", values=result, tag="orow")

                    my_tree.tag_configure('orow', background='#EEEEEE')
                    my_tree.grid(row=1, column=5, columnspan=4, rowspan=5, padx=10, pady=10)

                display_data()
                root.mainloop()


 
def cadastrarUsers():
                def registrar():
                    name = nameF.get()
                    Usuario = UsuarioF.get()
                    password = passwordF.get()
                    registrar_Cadastro(name, Usuario, password)


                # TELA DE CADASTRO
                cad = Tk()
                corDeFundo= '#F0F0F0'
                cad.title('cadastro')
                cad["bg"] = corDeFundo
                cad.geometry("300x300+100+100")
                cad.geometry("600x420")  
                cad.resizable(width=False, height=False)
                # Carrega a imagem


                title = Label(cad, text='Cadastro', bg=corDeFundo, foreground='#F2044E', font=20)
                title.pack(side=TOP, fill=X)

                name = Label(cad, text='Nome:', bg=corDeFundo, foreground='#F2044E')
                name.place(x=180, y=80)
                nameF = Entry(cad)
                nameF.place(x=240, y=80)

                Usuario = Label(cad, text='Usuario:', bg=corDeFundo, foreground='#F2044E')
                Usuario.place(x=180, y=130)
                UsuarioF = Entry(cad)
                UsuarioF.place(x=240, y=130)

                password = Label(cad, text='Senha:', bg=corDeFundo, foreground='#F2044E')
                password.place(x=180, y=180)
                passwordF = Entry(cad, show="•")
                passwordF.place(x=240, y=180)

                enter = Button(cad, width='11', text='Cadastrar', bg='#F2044E', command=registrar)
                enter.place(x=260, y=250)
                enter = Button(cad, width='11', text='Voltar', bg='#F2044E', command=cad.destroy)
                enter.place(x=260, y=300)

                cad.mainloop()
                 
# TELA DE LOGIN
login = Tk()
corDeFundo= '#0b2e3b'
login.title('LOGIN')
login["bg"] = corDeFundo
login.geometry("600x400")
login.resizable(width=False, height=False)


# Carrega a imagem

imagem = tk.PhotoImage(file="login.png")
w = tk.Label(login, image=imagem, width=700, height=400)
w.imagem = imagem
w.pack()

userF = Entry(login, width=18, bd='3', font=('Arial bold', 15))
userF.place(x=297, y=160)

passwordF = Entry(login, width=18, bd='3', show="•", font=('Arial bold', 15))
passwordF.place(x=297, y=220)

# Create a PhotoImage object with the image file
imgRedondo = PhotoImage(file='bnt_login.png')

# Create a Button with the image
btnRedondo = Button(login, image=imgRedondo, bd=0, relief="flat", highlightthickness=0, command=acessando_Login)
btnRedondo.place(x=358, y=328)



login.mainloop()
