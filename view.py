import sqlite3
import tkinter as tk
import cliente
import vendedor
import venda
import produto

banco = sqlite3.connect('banco_mercado.db')
cursor = banco.cursor()

cor2 = 'lightblue'
root = tk.Tk()

root.geometry('800x600')
root.title("Mercado")
root.resizable(False, False)
bg = tk.PhotoImage(file='Market_bg.png')

tela = tk.Canvas(root, width=800, height=600)
tela.pack(fill='both', expand=True)
tela.create_image(0,0, image=bg,anchor = 'nw')
tela.create_text(400,100,text="Mercado RAD",font=("Helvetica", 50), fill='white')
btn_cliente = tk.Button(root, text="Cliente", width=9, font=("arial", 14),
                        bg=cor2, relief='raised', overrelief='ridge', command=cliente.open_cliente)
btn_cliente.place(relx=0.15, rely=0.4)

btn_vendedor = tk.Button(root, text="Vendedor", width=9, font=("arial", 14),
                         bg=cor2, relief='raised', overrelief='ridge', command=vendedor.open_vendedor)
btn_vendedor.place(relx=0.35, rely=0.4)

btn_venda = tk.Button(root, text="Venda", width=9, font=("arial", 14),
                      bg=cor2, relief='raised', overrelief='ridge', command=venda.open_venda)
btn_venda.place(relx=0.55, rely=0.4)

btn_produto = tk.Button(root, text="Produto", width=9, font=("arial", 14),
                        bg=cor2, relief='raised', overrelief='ridge', command=produto.open_produto)
btn_produto.place(relx=0.75, rely=0.4)

root.mainloop()
