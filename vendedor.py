import sqlite3
import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
def open_vendedor():
    banco = sqlite3.connect('banco_mercado.db')
    cursor = banco.cursor()
    try:
        cursor.execute("CREATE TABLE vendedor (id_vendedor integer PRIMARY KEY , nome text, cpf integer, "
                       "endereco text)")
    except:
        pass
    cursor.execute("PRAGMA foreign_keys = ON")
    banco.commit()


    def clear():
        nome_textbox.delete(0, 'end')
        cpf_textbox.delete(0, 'end')
        ender_textbox.delete(0, 'end')


    def deletar():
        try:
            for i in table.selection():
                valor = table.item(i)['values']
                cursor.execute("DELETE FROM vendedor where id_vendedor = ? and nome =? and cpf = ? and endereco =?", valor)
                table.delete(i)
                banco.commit()
                clear()
        except:
            tkinter.messagebox.showwarning("Erro", "Esse registro não pode ser deletado")
            banco.commit()



    def entrada():
        ls = []
        input = nome_textbox.get(), cpf_textbox.get(), ender_textbox.get()
        try:
            name = str(nome_textbox.get())
            cpf = int(cpf_textbox.get())
            endereco = str(ender_textbox.get())
        except ValueError:
            tkinter.messagebox.showwarning("Erro", "Insira os dados corretamente")
            return
        if nome_textbox.get() and cpf_textbox.get() and ender_textbox.get():
            ls.append(input)
            for i in ls:
                cursor.execute("INSERT INTO vendedor (nome,cpf,endereco) VALUES (?,?,?) ", i)
                cursor.execute("SELECT * FROM vendedor where nome =? and cpf = ? and endereco =?", i)
                data = cursor.fetchall()
                for d in data:
                    table.insert(parent='', index=0, values=d)
            banco.commit()
            clear()
        else:
            tkinter.messagebox.showwarning("Erro", "Preencha todos os campos")


    def confirmar():
        ls = []
        input = nome_textbox.get(), cpf_textbox.get(), ender_textbox.get()
        for i in table.selection():
            valor = table.item(i)['values']
            cursor.execute("SELECT id_vendedor FROM vendedor where id_vendedor = ? and nome =? and cpf = ? and endereco =?",
                           valor)
            data = cursor.fetchall()
            for d in data:
                for m in d:
                    id = m
            cursor.execute("""UPDATE vendedor SET
            nome = :nome,
            cpf = :cpf,
            endereco = :ender
    
            WHERE id_vendedor = :id
            """, {
                'id': id,
                'nome': nome_textbox.get(),
                'cpf': cpf_textbox.get(),
                'ender': ender_textbox.get()
            })
            ls.append(input)
            table.delete(i)
            for n in ls:
                cursor.execute("SELECT * FROM vendedor where nome =? and cpf = ? and endereco =?", n)
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
                cursor.execute("SELECT * FROM vendedor where id_vendedor = ? and nome = ? and cpf = ? and endereco = ?",
                               valor)
                data = cursor.fetchall()
                for d in data:
                    for i in d:
                        ls.append(i)
                nome_textbox.insert("1", ls[1])
                cpf_textbox.insert("1", ls[2])
                ender_textbox.insert("1", ls[3])
            btn_confirmar.place(relx=0.85, rely=0.24)
            btn_atualizar.place_forget()
            btn_enviar.place_forget()
            btn_deletar.place_forget()


    cor = '#70b5ad'
    window = tk.Tk()
    window.geometry('800x600')
    window.title("Vendedor")
    lista = []
    table = ttk.Treeview(window, columns=('id', 'nome', 'cpf', 'endereço'), show='headings')

    table.heading('id', text='Id_vendedor')
    table.heading('nome', text='Nome')
    table.heading('cpf', text='Cpf')
    table.heading('endereço', text='Endereço')
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

    cpf_label = tk.Label(frame, text="CPF:", bg=cor)
    cpf_label.place(relx=0.05, rely=0.2)
    cpf_textbox = tk.Entry(frame)
    cpf_textbox.place(relx=0.05, rely=0.3)

    ender_label = tk.Label(frame, text="Endereço:", bg=cor)
    ender_label.place(relx=0.05, rely=0.4)
    ender_textbox = tk.Entry(frame)
    ender_textbox.place(relx=0.05, rely=0.5)

    cursor.execute("SELECT * FROM vendedor")
    data = cursor.fetchall()
    for d in data:
        table.insert(parent='', index=0, values=d)
    window.mainloop()

    table.mainloop()