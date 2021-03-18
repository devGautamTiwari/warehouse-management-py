from logging import basicConfig
from tkinter import*
from tkinter import ttk
from tkinter import messagebox
import mysql.connector  # importing mysql connector

# FRONT END
win = Tk()
win.title("WAREHOUSE MANAGEMENT")
win.geometry("1000x900+400+10")
# win.resizable(0,0)

'''Create the frame'''
Mainframe = Frame(win, bg="#efefef")
Mainframe.place(x=0, y=0, width=1000, height=900)

Heading_label = Label(Mainframe, font=("arial", 40, "bold"), fg="red",
                      text="Warehouse Inventory Sales Purchase ", bg="#efefef")
Heading_label.grid(row=0, column=0, padx=20, pady=40)

Entryframe = Frame(Mainframe, padx=50, pady=10, bg="green", relief=RAISED)
Entryframe.place(x=80, y=150, width=850, height=350)


labelId = Label(Entryframe, font=("arial", 15, "bold"),
                text="Product ID:", padx=2, pady=2, bg="yellow", fg="blue")
labelId.grid(row=0, column=0, sticky=W)
entryId = Entry(Entryframe, font=("arial", 20, "bold"), width=30, relief=SUNKEN, bd=2)
entryId.grid(row=0, column=1, sticky=W, pady=5, padx=10)

labelName = Label(Entryframe, font=("arial", 15, "bold"),
                  text="Product Name:", padx=2, pady=2, bg="yellow", fg="blue")
labelName.grid(row=1, column=0, sticky=W)
entryName = Entry(Entryframe, font=("arial", 20, "bold"), width=30, relief=SUNKEN, bd=2)
entryName.grid(row=1, column=1, sticky=W, pady=5, padx=10)


labelPrice = Label(Entryframe, font=("arial", 15, "bold"),
                   text="Product Price (Rs):", padx=2, pady=2, bg="yellow", fg="blue")
labelPrice.grid(row=2, column=0, sticky=W)
entryPrice = Entry(Entryframe, font=("arial", 20, "bold"), width=30, relief=SUNKEN, bd=2)
entryPrice.grid(row=2, column=1, sticky=W, pady=5, padx=10)


labelQty = Label(Entryframe, font=("arial", 15, "bold"),
                 text="Product Quantity:", padx=2, pady=2, bg="yellow", fg="blue")
labelQty.grid(row=3, column=0, sticky=W)
entryQty = Entry(Entryframe, font=("arial", 20, "bold"), width=30, relief=SUNKEN, bd=2)
entryQty.grid(row=3, column=1, sticky=W, pady=5, padx=10)

labelCompany = Label(Entryframe, font=("arial", 15, "bold"),
                     text="Mfg. Company :", padx=2, pady=2, bg="yellow", fg="blue")
labelCompany.grid(row=4, column=0, sticky=W, pady=5, padx=10)
entryCompany = Entry(Entryframe, font=("arial", 20, "bold"), width=30, relief=SUNKEN, bd=2)
entryCompany.grid(row=4, column=1, sticky=W, pady=5, padx=10)


labelContact = Label(Entryframe, font=("arial", 15, "bold"),
                     text="Company Contact :", padx=2, pady=2, bg="yellow", fg="blue")
labelContact.grid(row=5, column=0, sticky=W)
entryContact = Entry(Entryframe, font=("arial", 20, "bold"), width=30, relief=SUNKEN, bd=2)
entryContact.grid(row=5, column=1, sticky=W, pady=5, padx=10)

data_frame = Frame(Mainframe, padx=0, pady=10, relief=RAISED)
data_frame.place(x=0, y=620)

tree = ttk.Treeview(data_frame, column=("c1", "c2", "c3", "c4", "c5", "c6"), show='headings', selectmode ='browse')
tree.column("#1", anchor=CENTER, width=100, stretch=NO)
tree.heading("#1", text="ID")

tree.column("#2", anchor=CENTER)
tree.heading("#2", text="Name")

tree.column("#3", anchor=CENTER, width=149, stretch=NO)
tree.heading("#3", text="Price (Rs.)")

tree.column("#4", anchor=CENTER, width=149, stretch=NO)
tree.heading("#4", text="Quantity")

tree.column("#5", anchor=CENTER)
tree.heading("#5", text="Mfg Company")

tree.column("#6", anchor=CENTER)
tree.heading("#6", text="Contact")
tree.pack()

DB_NAME = "warehouse_management"
TABLE_NAME = "product_details"

# interacting with database
mydb = mysql.connector.connect(host="MSI",
                               user="gautam",
                               password="1234")
cur = mydb.cursor()
cur.execute(f'create database if not exists {DB_NAME}')
cur.execute('use warehouse_management')
cur.execute(
    f"""create table if not exists {TABLE_NAME}(Product_ID int(10)
primary key,Product_name varchar(40),Product_price int,Product_quantity int,
Mfg_company varchar(40),Company_contact_number varchar(20))""")
mydb.commit()


def insert_data_entry():
    Product_ID = entryId.get()
    Product_name = entryName.get()
    Product_price = entryPrice.get()
    Product_quantity = entryQty.get()
    Mfg_company = entryCompany.get()
    Company_contact_number = entryContact.get()

    insert = f"insert into {TABLE_NAME} values({Product_ID}, '{Product_name}',{Product_price},{Product_quantity}, '{Mfg_company}', '{Company_contact_number}')"
    try:
        cur.execute(insert)
        mydb.commit()
    except:
        messagebox.showerror(
            "Error", "Something went wrong when inserting data")
    else:
        messagebox.showinfo("Success", "Data inserted successfully")


def data_delete_entry():
    Product_ID = entryId.get()
    Product_name = entryName.get()
    Product_price = entryPrice.get()
    Product_quantity = entryQty.get()
    Mfg_company = entryCompany.get()
    Company_contact_number = entryContact.get()
    entries = {"Product_ID": Product_ID, "Product_name": Product_name, "Product_price": Product_price,
               "Product_quantity": Product_quantity, "Mfg_company": Mfg_company, "Company_contact_number": Company_contact_number}
    delete_all = False

    if Product_ID:
        delete = f'Delete from {TABLE_NAME} where Product_ID=({Product_ID})'
    else:
        for entry in entries:
            value = entries[entry]
            if value:
                delete = f"Delete from {TABLE_NAME} where {entry}='{value}'"
                if entry == "Product_price" or entry == "Product_quantity":
                    delete = f"Delete from {TABLE_NAME} where {entry}={value}"
                break
            else:
                if entry == "Company_contact_number":
                    delete_all = True
                    delete = f"TRUNCATE {TABLE_NAME}"
    
    del_msg = f"Are you sure you want to delete rows with {entry}={value}?"
    if delete_all:
        del_msg = "Are you sure you want to delete all rows?"
    if messagebox.askyesno("Confirm Delete?", del_msg):
        cur.execute(delete)
    mydb.commit()


def data_update_entry():
    Product_ID = entryId.get()
    Product_name = entryName.get()
    Product_price = entryPrice.get()
    Product_quantity = entryQty.get()
    Mfg_company = entryCompany.get()
    Company_contact_number = entryContact.get()
    entries = {"Product_ID": Product_ID, "Product_name": Product_name, "Product_price": Product_price,
               "Product_quantity": Product_quantity, "Mfg_company": Mfg_company, "Company_contact_number": Company_contact_number}
    for entry in entries:
        value = entries[entry]
        if value:
            update = f"update {TABLE_NAME} set {entry}='{entries[entry]}' where Product_ID={Product_ID}"
            if entry == "Product_price" or entry == "Product_quantity":
                print("entry", entry)
                update = f"update {TABLE_NAME} set {entry}={entries[entry]} where Product_ID={Product_ID}"
    try:
        cur.execute(update)
    except:
         messagebox.showerror(
            "Error", "Something went wrong when Updating data")
    else:
        messagebox.showinfo("Success", "Data updated successfully")

    mydb.commit()


def data_search_entry():
    Product_ID = entryId.get()
    Product_name = entryName.get()
    Product_price = entryPrice.get()
    Product_quantity = entryQty.get()
    Mfg_company = entryCompany.get()
    Company_contact_number = entryContact.get()
    entries = {"Product_ID": Product_ID, "Product_name": Product_name, "Product_price": Product_price,
               "Product_quantity": Product_quantity, "Mfg_company": Mfg_company, "Company_contact_number": Company_contact_number}
    query = ""
    for entry in entries:
        if entries[entry]:
            if entry == "Product_price" or entry == "Product_quantity":
                query += f" and {entry}={entries[entry]}"
            else:
                query += f" and {entry}='{entries[entry]}'"
    if query:
        query = " where" + query[4:]

    search = f'select * from {TABLE_NAME}{query}'
    cur.execute(search)

def display_data():
    global data_win, cur, tree
    for i in tree.get_children():
        tree.delete(i)
    data = cur.fetchall()
    mydb.commit()
    for row in data:
        tree.insert("", END, values=row)

'''button events functions'''


def save():
    insert_data_entry()
    clear_entries()


def delete():
    data_delete_entry()
    clear_entries()



def update():
    data_update_entry()
    clear_entries()


def search():
    data_search_entry()
    display_data()
    clear_entries()


def clear_entries():
    entryId.delete(0, END)
    entryName.delete(0, END)
    entryPrice.delete(0, END)
    entryQty.delete(0, END)
    entryCompany.delete(0, END)
    entryContact.delete(0, END)


'''Add the bottons to operation Frame'''

Operationframe = Frame(Mainframe, padx=50, pady=20, bg="red", relief=RAISED)
Operationframe.place(x=80, y=480, width=850)
buttonSaveData = Button(Operationframe, text='Save', font=(
    'arial', 12, 'bold'), height=2, command=save, relief=RAISED)
buttonSaveData.pack(fill=X, expand=True)

buttonDelete = Button(Operationframe, text='Delete', font=(
    'arial', 12, 'bold'), height=2, command=delete, relief=RAISED)
buttonDelete.pack(fill=X, expand=True, side=LEFT)

buttonSearch = Button(Operationframe, text='Search', font=(
    'arial', 12, 'bold'), height=2, command=search, relief=RAISED)
buttonSearch.pack(fill=X, expand=True, side=LEFT)

buttonUpdate = Button(Operationframe, text='Update', font=(
    'arial', 12, 'bold'), command=update, height=2, relief=RAISED)
buttonUpdate.pack(fill=X, expand=True,side=LEFT)

buttonClose = Button(Operationframe, text='Close', font=(
    'arial', 12, 'bold'), command=quit, height=2, relief=RAISED)
buttonClose.pack(fill=X, expand=True, side=LEFT)


win.mainloop()
