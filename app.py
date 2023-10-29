from tkinter import *
from tkinter import messagebox, PhotoImage
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
                root.geometry("1300x600")
                my_tree = ttk.Treeview(root)
                root.configure(bg="#0b2e3b")
                storeName = "Cadastre seus pedidos"
               
                # funções

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

           
                # estrutura

                titleLabel = Label(root, text=storeName, font=('Arial bold', 30), bd=2, foreground='white', bg='#0b2e3b')
                titleLabel.grid(row=0, column=1, columnspan=8, padx=20, pady=20)

                NomeLabel = Label(root, text="Nome", font=('Arial bold', 15), foreground='white', bg='#0b2e3b')
                valorLabel = Label(root, text="Valor", font=('Arial bold', 15), foreground='white', bg='#0b2e3b')
                formaLabel = Label(root, text="Forma de pg", font=('Arial bold', 15), foreground='white', bg='#0b2e3b')
                pedidoLabel = Label(root, text="Pedido", font=('Arial bold', 15), foreground='white', bg='#0b2e3b')
                quantidadeLabel = Label(root, text="Quantidade", font=('Arial bold', 15), foreground='white', bg='#0b2e3b')
           
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
                    bd=3, font=('Arial', 15),foreground='white', bg="#FF0000", command=acessando_Login)
                buttonVoltar.grid(row=8, column=1, columnspan=1)

           
                style = ttk.Style()
                style.configure("Treeview.Heading", font=('Arial bold', 15))

                my_tree['columns'] = ("ID", "Nome", "Valor", "Forma de pg", "Pedido", "Quantidade")
                my_tree.column("#0", width=0, stretch=NO)
                my_tree.column("ID", anchor=W, width=100)
                my_tree.column("Nome", anchor=W, width=150)
                my_tree.column("Valor", anchor=W, width=150)
                my_tree.column("Forma de pg", anchor=W, width=150)
                my_tree.column("Pedido", anchor=W, width=150)
                my_tree.column("Quantidade", anchor=W, width=150)

                my_tree.heading("ID", text="ID", anchor=W)
                my_tree.heading("Nome", text="Nome", anchor=W)
                my_tree.heading("Valor", text="Valor", anchor=W)
                my_tree.heading("Forma de pg", text="Forma de pg", anchor=W)
                my_tree.heading("Pedido", text="Pedido", anchor=W)
                my_tree.heading("Quantidade", text="Quantidade", anchor=W)

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

                  #~~ Criação do menu~~

 
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
                cad.geometry("600x420")  
                cad.resizable(width=False, height=False)

                imagem = tk.PhotoImage(file="cadastro.png")
                w = tk.Label(login, image=imagem, width=700, height=400)
                w.imagem = imagem
                w.pack()

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

passwordF = Entry(login, width=18, bd='3', font=('Arial bold', 15))
passwordF.place(x=297, y=220)

# Create a PhotoImage object with the image file
imgRedondo = PhotoImage(file='ENTRAR.png')

# Create a Button with the image
btnRedondo = Button(login, image=imgRedondo, bd=0, relief="flat", highlightthickness=0, command=acessando_Login)
btnRedondo.place(x=358, y=328)

#enter = ttk.Button(login, width='10', text='ENTRAR', style='Custom.TButton', command=acessando_Login)
#enter.place(x=365, y=300)


login.mainloop()
