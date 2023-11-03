import sqlite3
import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
def open_produto():
    banco = sqlite3.connect('banco_mercado.db')
    cursor = banco.cursor()
    try:
        cursor.execute("CREATE TABLE produto (id_produto INTEGER PRIMARY KEY , nome TEXT, pc_unit FLOAT, "
                       "qtde_estq INTEGER, categoria TEXT)")
    except:
        pass
    cursor.execute("PRAGMA foreign_keys = ON")
    banco.commit()


    def clear():
        nome_textbox.delete(0, 'end')
        pc_unit_textbox.delete(0, 'end')
        qtde_estq_textbox.delete(0, 'end')
        categoria_textbox.delete(0, 'end')


    def deletar():
        try:
            for i in table.selection():
                valor = table.item(i)['values']
                cursor.execute("DELETE FROM produto where id_produto = ? and nome =? and pc_unit = ? and qtde_estq =? and categoria =?", valor)
                table.delete(i)
                banco.commit()
                clear()
        except sqlite3.IntegrityError:
            tkinter.messagebox.showwarning("Erro", "Esse registro não pode ser deletado")
            banco.commit()


    def entrada():
        ls = []
        input = nome_textbox.get(), pc_unit_textbox.get(), qtde_estq_textbox.get(), categoria_textbox.get()
        try:
            nome = str(nome_textbox.get())
            pc_unit = float(pc_unit_textbox.get())
            qtde_estq = int(qtde_estq_textbox.get())
            categoria = str(categoria_textbox.get())
        except ValueError:
            tkinter.messagebox.showwarning("Erro", "Insira os dados corretamente")
            return
        if nome_textbox.get() and pc_unit_textbox.get() and qtde_estq_textbox.get() and categoria_textbox.get():
            ls.append(input)
            for i in ls:
                cursor.execute("INSERT INTO produto (nome,pc_unit,qtde_estq, categoria) VALUES (?,?,?,?) ", i)
                cursor.execute("SELECT * FROM produto where nome =? and pc_unit = ? and qtde_estq =? and categoria = ?", i)
                data = cursor.fetchall()
                for d in data:
                    table.insert(parent='', index=0, values=d)
            banco.commit()
            clear()
        else:
            tkinter.messagebox.showwarning("Erro", "Preencha todos os campos")


    def confirmar():
        ls = []
        input = nome_textbox.get(), pc_unit_textbox.get(), qtde_estq_textbox.get(), categoria_textbox.get()
        for i in table.selection():
            valor = table.item(i)['values']
            cursor.execute("SELECT id_produto FROM produto where id_produto = ? and nome =? and pc_unit = ? and qtde_estq =? and categoria =?",
                           valor)
            data = cursor.fetchall()
            for d in data:
                for m in d:
                    id = m
            cursor.execute("""UPDATE produto SET
            nome = :nome,
            pc_unit = :preco,
            qtde_estq = :qtde,
            categoria = :categoria
    
            WHERE id_produto = :id
            """, {
                'id': id,
                'nome': nome_textbox.get(),
                'preco': pc_unit_textbox.get(),
                'qtde': qtde_estq_textbox.get(),
                'categoria': categoria_textbox.get()
            })
            ls.append(input)
            table.delete(i)
            for n in ls:
                cursor.execute("SELECT * FROM produto where nome =? and pc_unit = ? and qtde_estq =? and categoria =?", n)
                data = cursor.fetchall()
                for d in data:
                    table.insert(parent='', index=0, values=d)
            banco.commit()
        clear()
        banco.commit()
        btn_confirmar.place_forget()
        btn_enviar.place(relx=0.85, rely=0.05)
        btn_deletar.place(relx=0.85, rely=0.24)
        btn_atualizar.place(relx=0.85, rely=0.43)


    def atualizar():
        ls = []
        if len(table.selection()) != 1:
            tkinter.messagebox.showwarning("Erro", "Insira os dados corretamente")
            return
        else:
            for i in table.selection():
                valor = table.item(i)['values']
                cursor.execute("SELECT * FROM produto where id_produto = ? and nome = ? and pc_unit = ? and qtde_estq = ? and categoria =?",
                               valor)
                data = cursor.fetchall()
                for d in data:
                    for i in d:
                        ls.append(i)
                nome_textbox.insert("1", ls[1])
                pc_unit_textbox.insert("1", ls[2])
                qtde_estq_textbox.insert("1", ls[3])
                categoria_textbox.insert("1", ls[4])
            btn_confirmar.place(relx=0.85, rely=0.24)
            btn_atualizar.place_forget()
            btn_enviar.place_forget()
            btn_deletar.place_forget()


    cor = '#70b5ad'
    window = tk.Tk()
    window.geometry('1000x600')
    window.title("Produto")

    lista = []

    table = ttk.Treeview(window, columns=('id', 'nome', 'pc_unit', 'qtde_estq', 'categoria'), show='headings')
    table.heading('id', text='Id_Produto')
    table.heading('nome', text='Nome')
    table.heading('pc_unit', text='Preço Unitário')
    table.heading('qtde_estq', text='Qtde. em Estoque')
    table.heading('categoria', text='Categoria')
    table.pack(fill='both', expand=True)

    frame = tk.Frame(window, bg=cor, highlightthickness=1, highlightbackground='black')
    frame.place(relx=0, rely=0.7, relwidth=1, relheight=0.5)

    btn_enviar = tk.Button(frame, text="Enviar", width=8, command=entrada, font=("arial", 14), bg='#038cfc', relief='raised', overrelief='ridge')
    btn_deletar = tk.Button(frame, text="Deletar", width=8, command=deletar, font=("arial", 14), bg='#ef5350', relief='raised', overrelief='ridge')
    btn_atualizar = tk.Button(frame, text="Atualizar", width=8, command=atualizar, font=("arial", 14), bg='#efca50', relief='raised', overrelief='ridge')
    btn_confirmar = tk.Button(frame, text="Confirmar", width=8, command=confirmar, font=("arial", 14), bg='#41c48c', relief='raised', overrelief='ridge')
    btn_enviar.place(relx=0.85, rely=0.05)
    btn_deletar.place(relx=0.85, rely=0.24)
    btn_atualizar.place(relx=0.85, rely=0.43)

    nome_label = tk.Label(frame, text="Nome:", bg=cor)
    nome_label.place(relx=0.05, rely=0)
    nome_textbox = tk.Entry(frame)
    nome_textbox.place(relx=0.05, rely=0.1)

    pc_unit_label = tk.Label(frame, text="Preço do Produto:", bg=cor)
    pc_unit_label.place(relx=0.05, rely=0.2)
    pc_unit_textbox = tk.Entry(frame)
    pc_unit_textbox.place(relx=0.05, rely=0.3)

    qtde_estq_label = tk.Label(frame, text="Quantidade em Estoque:", bg=cor)
    qtde_estq_label.place(relx=0.05, rely=0.4)
    qtde_estq_textbox = tk.Entry(frame)
    qtde_estq_textbox.place(relx=0.05, rely=0.5)

    categoria_label = tk.Label(frame, text="Categoria do Produto:", bg=cor)
    categoria_label.place(relx=0.3, rely=0)
    categoria_textbox = tk.Entry(frame)
    categoria_textbox.place(relx=0.3, rely=0.1)

    cursor.execute("SELECT * FROM produto")
    data = cursor.fetchall()
    for d in data:
        table.insert(parent='', index=0, values=d)

    window.mainloop()
    table.mainloop()