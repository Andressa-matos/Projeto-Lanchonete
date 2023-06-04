from tkinter import *
from tkinter import messagebox
import banco as banco
import tkinter as tk
from tkinter import ttk
import sqlite3

################ cores ###############
co0 = "#f0f3f5"  # Preta
co1 = "#feffff"  # branca
co2 = "#4fa882"  # verde
co3 = "#38576b"  # valor
co4 = "#403d3d"   # letra
co5 = "#e06636"   # - profit
co6 = "#038cfc"   # azul
co7 = "#ef5350"   # vermelha
co8 = "#263238"   # + verde
co9 = "#e9edf5"   # sky blue

def bt_Sair():
    login.destroy()
    

def registrar_Cadastro(name, usuario, password):
    # Pegar informações para o Banco
    NameBanco = name
    UsuarioBanco = usuario
    PasswordBanco = password

    if NameBanco == "" or UsuarioBanco == "" or PasswordBanco == "":
        messagebox.showerror(title="Erro de Registro", message="Preencha todos os Campos")
    else:
        # Inserir no Banco
        banco.cursor.execute("""
        INSERT INTO Users(Name, Usuario, Password) VALUES(?, ?, ?)
        """, (NameBanco, UsuarioBanco, PasswordBanco))
        banco.conn.commit()
        messagebox.showinfo(title="Conta criada", message="Cadastrado(a) com sucesso!")


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

#   ~~ TELA DE MENU ~~
            app = tk.Tk()
            app.geometry("500x300")
            app.title("Menu")
            app.configure(bg='#0b2e3b')

            # Criação dos comandos das opções do menu
            def fazer_pedido():

                root = Tk()
                root.title("Pedidos")
                root.geometry("1290x600")
                my_tree = ttk.Treeview(root)
                root.configure(bg="#0b2e3b")
                storeName = "Cadastre seus pedidos"

                # funções

                def reverse(tuples):
                    new_tup = tuples[::-1]
                    return new_tup


                def insert( id, nome, numero, endereco, pedido, quantidade):
                    conn = sqlite3.connect("data.db")
                    cursor = conn.cursor()

                    cursor.execute("""CREATE TABLE IF NOT EXISTS 
                        PEDIDOS(itemId TEXT, itemNome TEXT, itemNumero TEXT, itemEndereco TEXT, itempedido TEXT, itemquantidade TEXT)""")

                    cursor.execute("INSERT INTO PEDIDOS VALUES ('" + str(id) + "','" + str(nome) + "','" + str(numero) + "','" + str(endereco) + "','" + str(pedido) + "','" + str(quantidade) + "')")
                    conn.commit()


                def delete(data):
                    conn = sqlite3.connect("data.db")
                    cursor = conn.cursor()

                    cursor.execute("""CREATE TABLE IF NOT EXISTS 
                        PEDIDOS(itemId TEXT, itemNome TEXT, itemNumero TEXT, itemEndereco TEXT, itempedido TEXT, itemquantidade TEXT)""")
                    
                    cursor.execute("DELETE FROM PEDIDOS WHERE itemId = '" + str(data) + "'")
                    conn.commit()


                def update(id, nome, numero, endereco, pedido, quantidade, idName):
                    conn = sqlite3.connect("data.db")
                    cursor = conn.cursor()

                    cursor.execute("""CREATE TABLE IF NOT EXISTS 
                        PEDIDOS(itemId TEXT, itemNome TEXT, itemNumero TEXT, itemEndereco TEXT, itempedido TEXT, itemquantidade TEXT)""")

                    cursor.execute("UPDATE PEDIDOS SET itemId = '" + str(id) + "', itemNome = '" + str(nome) + "', itemNumero = '" + str(numero) + "', itemEndereco = '" + str(endereco) + "', itempedido = '" + str(pedido) + "', itemquantidade = '" + str(quantidade) + "' WHERE itemId='" + str(idName) + "'")

                    conn.commit()


                def read():
                    conn = sqlite3.connect("data.db")
                    cursor = conn.cursor()

                    cursor.execute("""CREATE TABLE IF NOT EXISTS 
                        PEDIDOS(itemId TEXT, itemNome TEXT, itemNumero TEXT, itemEndereco TEXT, itempedido TEXT, itemquantidade TEXT)""")

                    cursor.execute("SELECT * FROM PEDIDOS")
                    results = cursor.fetchall()
                    conn.commit()
                    return results


                def insert_data():
                    itemId = str(entryId.get())
                    itemNome = str(entryNome.get())
                    itemNumero = str(entryNumero.get())
                    itemEndereco = str(entryEndereco.get())
                    itempedido = str(entrypedido.get())
                    itemquantidade = str(entryquantidade.get())

                    if itemId == "" or itemId == " ":
                        print("Erro ao inserir o Id")

                    if itemNome == "" or itemNome == " ":
                        print("Erro ao inserir o Nome")

                    if itemNumero == "" or itemNumero == " ":
                        print("Erro ao inserir o Telefone")

                    if itemEndereco == "" or itemEndereco == " ":
                        print("Erro ao inserir o Endereço")

                    if itempedido == "" or itempedido == " ":
                        print("Erro ao inserir o Pedido")

                    if itemquantidade == "" or itemquantidade == " ":
                        print("Erro ao inserir a Quantidade")

                    else:
                        insert(str(itemId), str(itemNome), str(itemNumero), str(itemEndereco), str(itempedido), str(itemquantidade))

                    for data in my_tree.get_children():
                        my_tree.delete(data)

                    for result in reverse(read()):
                        my_tree.insert(parent='', index='end', iid=result, text="", values=(result), tag="orow")

                    my_tree.tag_configure('orow', background='#EEEEEE')
                    my_tree.grid(row=1, column=5, columnspan=4, rowspan=5, padx=10, pady=10)


                def delete_data():
                    selected_items = my_tree.selection()
                    if not selected_items:
                        print("Nenhum item selecionado.")
                        return

                    selected_item = my_tree.selection()[0]
                    deleteData = str(my_tree.item(selected_item)['values'][0])
                    delete(deleteData)

                    my_tree.delete(selected_item)  # Remove o item selecionado da treeview

                    my_tree.tag_configure('orow', background='#EEEEEE')
                    my_tree.grid(row=1, column=5, columnspan=4, rowspan=5, padx=10, pady=10)


                def update_data():

                    selected_items = my_tree.selection()
                    if not selected_items:
                        print("Nenhum item selecionado.")
                        return

                    selected_item = my_tree.selection()[0]
                    update_name = my_tree.item(selected_item)['values'][0]
                    update(entryId.get(), entryNome.get(), entryNumero.get(), entryEndereco.get(), entrypedido.get(), entryquantidade.get(), update_name)

                    for data in my_tree.get_children():
                        my_tree.delete(data)

                    for result in reverse(read()):
                        my_tree.insert(parent='', index='end', iid=result, text="", values=(result), tag="orow")

                    my_tree.tag_configure('orow', background='#EEEEEE')
                    my_tree.grid(row=1, column=5, columnspan=4, rowspan=5, padx=10, pady=10)


                # estrutura

                titleLabel = Label(root, text=storeName, font=('Arial bold', 30), bd=2, foreground='white', bg='#0b2e3b')
                titleLabel.grid(row=0, column=1, columnspan=8, padx=20, pady=20)

                idLabel = Label(root, text="ID", font=('Arial bold', 15), foreground='white', bg='#0b2e3b')
                NomeLabel = Label(root, text="Nome", font=('Arial bold', 15), foreground='white', bg='#0b2e3b')
                NumeroLabel = Label(root, text="Número", font=('Arial bold', 15), foreground='white', bg='#0b2e3b')
                EnderecoLabel = Label(root, text="Endereço", font=('Arial bold', 15), foreground='white', bg='#0b2e3b')
                pedidoLabel = Label(root, text="Pedido", font=('Arial bold', 15), foreground='white', bg='#0b2e3b')
                quantidadeLabel = Label(root, text="Quantidade", font=('Arial bold', 15), foreground='white', bg='#0b2e3b')

                idLabel.grid(row=1, column=0, padx=10, pady=10)
                NomeLabel.grid(row=2, column=0, padx=10, pady=10)
                NumeroLabel.grid(row=3, column=0, padx=10, pady=10)
                EnderecoLabel.grid(row=4, column=0, padx=10, pady=10)
                pedidoLabel.grid(row=5, column=0, padx=10, pady=10)
                quantidadeLabel.grid(row=6, column=0, padx=10, pady=10)

                entryId = Entry(root, width=25, bd=5, font=('Arial bold', 15))
                entryNome = Entry(root, width=25, bd=5, font=('Arial bold', 15))
                entryNumero = Entry(root, width=25, bd=5, font=('Arial bold', 15))
                entryEndereco = Entry(root, width=25, bd=5, font=('Arial bold', 15))
                entrypedido = Entry(root, width=25, bd=5, font=('Arial bold', 15))
                entryquantidade = Entry(root, width=25, bd=5, font=('Arial bold', 15))

                entryId.grid(row=1, column=1, columnspan=3, padx=5, pady=5)
                entryNome.grid(row=2, column=1, columnspan=3, padx=5, pady=5)
                entryNumero.grid(row=3, column=1, columnspan=3, padx=5, pady=5)
                entryEndereco.grid(row=4, column=1, columnspan=3, padx=5, pady=5)
                entrypedido.grid(row=5, column=1, columnspan=3, padx=5, pady=5)
                entryquantidade.grid(row=6, column=1, columnspan=3, padx=5, pady=5)

                buttonEnter = Button(
                    root, text="Enter", padx=5, pady=5, width=5,
                    bd=3, font=('Arial', 15),foreground='white', bg="#32CD32", command=insert_data)
                buttonEnter.grid(row=7, column=1, columnspan=1)

                buttonUpdate = Button(
                    root, text="Update", padx=5, pady=5, width=5,
                    bd=3, font=('Arial', 15),foreground='white', bg="#FFD700", command=update_data)
                buttonUpdate.grid(row=7, column=2, columnspan=1)

                buttonDelete = Button(
                    root, text="Delete", padx=5, pady=5, width=5,
                    bd=3, font=('Arial', 15),foreground='white', bg="#FF0000", command=delete_data)
                buttonDelete.grid(row=7, column=3, columnspan=1)

                buttonVoltar = Button(
                    root, text="Voltar", padx=5, pady=5, width=5,
                    bd=3, font=('Arial', 15),foreground='white', bg="#FF0000", command=root.destroy)
                buttonVoltar.grid(row=7, column=4, columnspan=1)

                style = ttk.Style()
                style.configure("Treeview.Heading", font=('Arial bold', 15))

                my_tree['columns'] = ("ID", "Nome", "Número", "Endereço", "Pedido", "Quantidade")
                my_tree.column("#0", width=0, stretch=NO)
                my_tree.column("ID", anchor=W, width=100)
                my_tree.column("Nome", anchor=W, width=150)
                my_tree.column("Número", anchor=W, width=150)
                my_tree.column("Endereço", anchor=W, width=150)
                my_tree.column("Pedido", anchor=W, width=150)
                my_tree.column("Quantidade", anchor=W, width=150)

                my_tree.heading("ID", text="ID", anchor=W)
                my_tree.heading("Nome", text="Nome", anchor=W)
                my_tree.heading("Número", text="Número", anchor=W)
                my_tree.heading("Endereço", text="Endereço", anchor=W)
                my_tree.heading("Pedido", text="Pedido", anchor=W)
                my_tree.heading("Quantidade", text="Quantidade", anchor=W)

                def display_data():
                    for data in my_tree.get_children():
                        my_tree.delete(data)

                    results = reverse(read())

                    for i, result in enumerate(results, start=1):
                        my_tree.insert(parent='', index='end', iid="item_" + str(i), text="", values=result, tag="orow")

                    my_tree.tag_configure('orow', background='#EEEEEE')
                    my_tree.grid(row=1, column=5, columnspan=4, rowspan=5, padx=14, pady=10)




                    my_tree.tag_configure('orow', background='#EEEEEE', font=('Arial bold', 15))
                    my_tree.grid(row=1, column=5, columnspan=4, rowspan=5, padx=10, pady=10)

                    root.mainloop()
 
            def cadastrarUsers():
                def registrar():
                    name = nameF.get()
                    Usuario = UsuarioF.get()
                    password = passwordF.get()
                    registrar_Cadastro(name, Usuario, password)


                # TELA DE CADASTRO
                cad = Tk()
                corDeFundo= '#0b2e3b'
                cad.title('cadastro')
                cad["bg"] = corDeFundo
                cad.geometry("300x300+100+100")
                cad.resizable(width=False, height=False)

                title = Label(cad, text='Cadastro', bg=corDeFundo, foreground='white', font=20)
                title.pack(side=TOP, fill=X)

                name = Label(cad, text='Nome:', bg=corDeFundo, foreground='white')
                name.place(x=46, y=50)
                nameF = Entry(cad)
                nameF.place(x=90, y=90)

                Usuario = Label(cad, text='Usuario:', bg=corDeFundo, foreground='white')
                Usuario.place(x=36, y=90)
                UsuarioF = Entry(cad)
                UsuarioF.place(x=90, y=50)

                password = Label(cad, text='Senha:', bg=corDeFundo, foreground='white')
                password.place(x=44, y=130)
                passwordF = Entry(cad, show="•")
                passwordF.place(x=90, y=130)

                enter = Button(cad, width='11', text='Cadastrar', command=registrar)
                enter.place(x=115, y=180)
                enter = Button(cad, width='11', text='Voltar', command=cad.destroy)
                enter.place(x=115, y=220)

                cad.mainloop()
                

            #~ Criação do menu~
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
    
# TELA DE LOGIN
login = Tk()
corDeFundo= '#0b2e3b'
login.title('LOGIN')
login["bg"] = corDeFundo
login.geometry("300x300+100+100")
login.resizable(width=False, height=False)


title = Label(login, text='LOGIN', bg=corDeFundo, foreground='white')
title.pack(side=TOP, fill=X)

user = Label(login, text='Usuario:', bg=corDeFundo, foreground='white')
user.place(x=46, y=90)
userF = Entry(login)
userF.place(x=100, y=90)

password = Label(login, text='Senha:', bg=corDeFundo, foreground='white')
password.place(x=50, y=130)
passwordF = Entry(login, show="•")
passwordF.place(x=100, y=130)


enter = ttk.Button(login, width='10', text='ENTRAR', style='Custom.TButton', command=acessando_Login)
enter.place(x=115, y=180)


login.mainloop()
