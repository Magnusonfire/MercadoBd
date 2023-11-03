import sqlite3
import tkinter as tk
import tkinter.messagebox
from tkinter import ttk


def open_venda():
    banco = sqlite3.connect('banco_mercado.db')
    cursor = banco.cursor()
    try:
        cursor.execute("CREATE TABLE venda (id_venda integer PRIMARY KEY, id_cliente integer,"
                       "id_vendedor integer, data_venda text,valor_total float,id_produto integer,FOREIGN KEY(id_produto) REFERENCES "
                       "produto (id_produto) ,FOREIGN KEY(id_cliente) REFERENCES "
                       "cliente (id_cliente), FOREIGN KEY(id_vendedor) REFERENCES vendedor (id_vendedor))")
    except:
        pass
    cursor.execute("PRAGMA foreign_keys = ON")
    banco.commit()

    def clear():
        id_cliente_textbox.delete(0, 'end')
        id_vendedor_textbox.delete(0, 'end')
        data_venda_textbox.delete(0, 'end')
        valor_total_textbox.delete(0, 'end')
        id_produto_textbox.delete(0,'end')


    def entrada():
        try:
            ls = []
            input = id_cliente_textbox.get(), id_vendedor_textbox.get(), data_venda_textbox.get(), valor_total_textbox.get(),id_produto_textbox.get()
            try:
                id_cliente = int(id_cliente_textbox.get())
                id_vendedor = int(id_vendedor_textbox.get())
                data_venda = str(data_venda_textbox.get())
                valor_total = float(valor_total_textbox.get())
                id_produto = int(id_produto_textbox.get())
            except ValueError:
                tkinter.messagebox.showwarning("Erro", "Insira os dados corretamente")
                return
            if data_venda_textbox.get() and valor_total_textbox.get():
                ls.append(input)
                for i in ls:
                    cursor.execute("INSERT INTO venda (id_cliente, id_vendedor, data_venda, valor_total, id_produto) VALUES (?,?,?,?,?) ",
                                   i)
                    cursor.execute(
                        "SELECT * FROM venda where id_cliente =? and id_vendedor =? and data_venda =? and valor_total = ? and id_produto = ?",
                        i)
                    data = cursor.fetchall()
                    for d in data:
                        table.insert(parent='', index=0, values=d)
                banco.commit()
                clear()
            else:
                tkinter.messagebox.showwarning("Erro", "Preencha todos os campos")
        except sqlite3.IntegrityError:
            tkinter.messagebox.showwarning("Erro", "Esse Id não existe")
            banco.commit()

    cor = '#70b5ad'
    window = tk.Tk()
    window.geometry('1200x600')
    window.title("Venda")
    lista = []
    table = ttk.Treeview(window, columns=('id_venda', 'id_cliente', 'id_vendedor', 'data_venda', 'valor_total', 'id_produto'),
                         show='headings')

    table.heading('id_venda', text='Id_venda')
    table.heading('id_cliente', text='Id_cliente')
    table.heading('id_vendedor', text='Id_vendedor')
    table.heading('data_venda', text='Data_venda')
    table.heading('valor_total', text='Valor_total')
    table.heading('id_produto', text='Id_produto')
    table.pack(fill='both', expand=True)

    frame = tk.Frame(window, bg=cor, highlightthickness=1, highlightbackground='black')
    frame.place(relx=0, rely=0.7, relwidth=1, relheight=0.5)

    btn_enviar = tk.Button(frame, text="Enviar", width=8, command=entrada, font=("arial", 14), bg='#038cfc',
                           relief='raised', overrelief='ridge')
    btn_enviar.place(relx=0.85, rely=0.05)

    id_cliente_label = tk.Label(frame, text="ID Cliente:", bg=cor)
    id_cliente_label.place(relx=0.05, rely=0)
    id_cliente_textbox = tk.Entry(frame)
    id_cliente_textbox.place(relx=0.05, rely=0.1)

    id_vendedor_label = tk.Label(frame, text="ID Vendedor:", bg=cor)
    id_vendedor_label.place(relx=0.05, rely=0.2)
    id_vendedor_textbox = tk.Entry(frame)
    id_vendedor_textbox.place(relx=0.05, rely=0.3)

    data_venda_label = tk.Label(frame, text="Data da Venda:", bg=cor)
    data_venda_label.place(relx=0.05, rely=0.4)
    data_venda_textbox = tk.Entry(frame)
    data_venda_textbox.place(relx=0.05, rely=0.5)

    valor_total_label = tk.Label(frame, text="Valor Total:", bg=cor)
    valor_total_label.place(relx=0.3, rely=0)
    valor_total_textbox = tk.Entry(frame)
    valor_total_textbox.place(relx=0.3, rely=0.1)

    id_produto_label = tk.Label(frame, text="Id Produto:", bg=cor)
    id_produto_label.place(relx=0.3, rely=0.2)
    id_produto_textbox = tk.Entry(frame)
    id_produto_textbox.place(relx=0.3, rely=0.3)

    cursor.execute("SELECT * FROM venda")
    data = cursor.fetchall()
    for d in data:
        table.insert(parent='', index=0, values=d)
    window.mainloop()

    table.mainloop()
