from tkinter import *
from tkinter import messagebox
from db_sindikalna import Database
from tkcalendar import Calendar
import datetime
db_sindikalna = Database('sindikalna.db')

def IzborBrojaRata(event):
    d = datetime.datetime.strptime(datum_prve_rate_text.get(),"%d.%m.%y")
    for i in range(broj_rata_text.get()):
        l = Label(app, text=d)
        r=i+1
        l.grid(row=3, column=r, sticky=W)
    pojedinacna_rata_text.set((ukupan_iznos_text.get()-uplaceno_text.get())/broj_rata_text.get())

def populate_list():
    parts_list.delete(0, END)
    for row in db_sindikalna.fetch():
        parts_list.insert(END, row)

def populate_list_date():
    parts_list.delete(0, END)
    for row in db_sindikalna.fetchDate():
        parts_list.insert(END, row)
    
    for i in range(100):
        if parts_list.get(i):
            parts_list.itemconfig(i,{'fg': 'red'})


def add_item():
    if sindikat_text.get() == '' or ime_text.get() == '' or prezime_text.get() == '' or ukupan_iznos_text.get() == '' or broj_rata_text.get() == '' or datum_prve_rate_text.get() == '':
        messagebox.showerror('Required Fields', 'Please include all fields')
        return
    db_sindikalna.insert(sindikat_text.get(), ime_text.get(), 
                        prezime_text.get(), ukupan_iznos_text.get(), 
                        broj_rata_text.get(), datum_prve_rate_text.get())
    parts_list.delete(0, END)
    parts_list.insert(END, (sindikat_text.get(), ime_text.get(),prezime_text.get(), ukupan_iznos_text.get(), broj_rata_text.get(), datum_prve_rate_text.get()))
    clear_text()
    populate_list()


def select_item(event):
    try:
        global selected_item
        index = parts_list.curselection()[0]
        selected_item = parts_list.get(index)

        sindikat_entry.delete(0, END)
        sindikat_entry.insert(END, selected_item[1])
        ime_entry.delete(0, END)
        ime_entry.insert(END, selected_item[2])
        prezime_entry.delete(0, END)
        prezime_entry.insert(END, selected_item[3])
        ukupan_iznos_entry.delete(0, END)
        ukupan_iznos_entry.insert(END, selected_item[4])
        # broj_rata_entry.delete(0, END)
        # broj_rata_entry.insert(END, selected_item[5])
        datum_prve_rate_entry.delete(0, END)
        datum_prve_rate_entry.insert(END, selected_item[6])
    except IndexError:
        pass


def remove_item():
    db_sindikalna.remove(selected_item[0])
    clear_text()
    populate_list()


def update_item():
    db_sindikalna.update(selected_item[0], sindikat_text.get(), ime_text.get(),
              prezime_text.get(), ukupan_iznos_text.get(), broj_rata_text.get(), datum_prve_rate_text.get())
    populate_list()


def clear_text():
    sindikat_entry.delete(0, END)
    ime_entry.delete(0, END)
    prezime_entry.delete(0, END)
    ukupan_iznos_entry.delete(0, END)
    # broj_rata_entry.delete(0, END)
    datum_prve_rate_entry.delete(0, END)

# Create window object
app = Tk()

# Sindikat
sindikat_text = StringVar()
sindikat_label = Label(app, text='Sindikat', font=('bold', 14))
sindikat_label.grid(row=0, column=0, sticky=W)
sindikat_entry = Entry(app, textvariable=sindikat_text)
sindikat_entry.grid(row=0, column=1)
# Ime
ime_text = StringVar()
ime_label = Label(app, text='Ime', font=('bold', 14))
ime_label.grid(row=0, column=2, sticky=W)
ime_entry = Entry(app, textvariable=ime_text)
ime_entry.grid(row=0, column=3)
# Prezime
prezime_text = StringVar()
prezime_label = Label(app, text='Prezime', font=('bold', 14))
prezime_label.grid(row=0, column=4, sticky=W)
prezime_entry = Entry(app, textvariable=prezime_text)
prezime_entry.grid(row=0, column=5)
# labela za iznos pojedinacnih rata
pojedinacna_rata_label = Label(app, text='Iznos pojedinacnih rata', font=('bold', 14))
pojedinacna_rata_label.grid(row=0, column=6, sticky=W)
# labela za iznos koji je uplacen
uplaceno_label = Label(app, text='Uplaceno pri kupovini', font=('bold', 14))
uplaceno_label.grid(row=0, column=7, sticky=W, padx=10)
# Datum prve rate
datum_prve_rate_text = StringVar()
datum_prve_rate_label = Label(app, text='Datum prve rate', font=('bold', 14))
datum_prve_rate_label.grid(row=1, column=0, sticky=W)
datum_prve_rate_entry = Entry(app, textvariable=datum_prve_rate_text)
datum_prve_rate_entry.grid(row=1, column=1)
# calendar = Calendar(app,selectmode='day', year=2022,month=6,day=26)
# calendar.grid(row=2, column=0)
# Ukupan iznos
ukupan_iznos_text = IntVar()
ukupan_iznos_label = Label(app, text='Ukupan iznos', font=('bold', 14))
ukupan_iznos_label.grid(row=1, column=2, sticky=W)
ukupan_iznos_entry = Entry(app, textvariable=ukupan_iznos_text)
ukupan_iznos_entry.grid(row=1, column=3)
# Broj rata
BROJEVI = list(range(1,13))
broj_rata_text = IntVar()
broj_rata_text.set(BROJEVI[0])
broj_rata_label = Label(app, text='Broj rata', font=('bold', 14))
broj_rata_label.grid(row=1, column=4, sticky=W)
broj_rata_drop_down = OptionMenu(app, broj_rata_text, *BROJEVI, command=IzborBrojaRata)
broj_rata_drop_down.grid(row=1, column=5)
# broj_rata_entry = Entry(app, textvariable=broj_rata_text)
# broj_rata_entry.grid(row=1, column=1)
# pojedinacne rate entry
pojedinacna_rata_text = IntVar()
pojedinacna_rata_entry = Entry(app, textvariable=pojedinacna_rata_text)
pojedinacna_rata_entry.grid(row=1, column=6)
# uplaceno pri kupovini entry
uplaceno_text = IntVar()
uplaceno_entry = Entry(app, textvariable=uplaceno_text)
uplaceno_entry.grid(row=1, column=7)
# Labele
rate_label = Label(app, text='Rate: ', font=('bold', 14))
rate_label.grid(row=3, column=0)
iznosi_label = Label(app, text='Iznosi: ', font=('bold', 14))
iznosi_label.grid(row=4, column=0)
# Parts List (Listbox)
parts_list = Listbox(app, height=12, width=80, border=0)
parts_list.grid(row=5, column=0, columnspan=5, rowspan=5)
# Create scrollbar
scrollbar = Scrollbar(app)
scrollbar.grid(row=5, column=4)
# Set scroll to listbox
parts_list.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=parts_list.yview)
# Bind select
parts_list.bind('<<ListboxSelect>>', select_item)

# Buttons
add_btn = Button(app, text='Dodaj podatak', width=12, command=add_item)
add_btn.grid(row=2, column=0, pady=20, padx=20)

remove_btn = Button(app, text='Obrisi podatak', width=12, command=remove_item)
remove_btn.grid(row=2, column=1)

update_btn = Button(app, text='Izmeni podatak', width=12, command=update_item)
update_btn.grid(row=2, column=2)

clear_btn = Button(app, text='Obrisi sva polja', width=12, command=clear_text)
clear_btn.grid(row=2, column=3)

charge_btn = Button(app, text='Uskoro za naplatu', width=15, command=populate_list_date)
charge_btn.grid(row=2, column=4)

show_btn = Button(app, text='Svi podaci', width=12, command=populate_list)
show_btn.grid(row=2, column=5)

app.title('Sindikala prodaja')
app.geometry('1200x600')

# Populate data
populate_list()

# Start program
app.mainloop()