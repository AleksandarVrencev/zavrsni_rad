# imports
from tkinter import *
from tkinter import messagebox
import re
from db_sindikalna import Database
from datetime import *
from dateutil.relativedelta import relativedelta
import tkinter.font as tkFont

# initialize database
db_sindikalna = Database('sindikalna.db')

# functions
def set_number_of_rates():
    regex_check()
    pojedinacna_rata_text.set(int((ukupan_iznos_text.get() - uplaceno_text.get()) / broj_rata_text.get()))

def regex_check():
    re_sindikat_entry = re.match("^[A-Z][-a-zA-Z]+$", sindikat_entry.get())
    # if not re_sindikat_entry:
    if sindikat_entry.get().__len__() < 3 or sindikat_entry.get().__len__() > 30:
        messagebox.showinfo(message="Polje 'Sindikat' je prazno ili nije odgovarajuće dužine.")
        return False
    re_ime_entry = re.match("^[A-Z][-a-zA-Z]+$", ime_entry.get())
    # if not re_ime_entry:
    if ime_entry.get().__len__() < 3 or ime_entry.get().__len__() > 30:
        messagebox.showinfo(message="Polje 'Ime' je prazno,počinje brojem ili nije odgovarajuće dužine.")
        return False
    re_prezime_entry = re.match("^[A-Z][-a-zA-Z]+$", prezime_entry.get())
    # if not re_prezime_entry:
    if ime_entry.get().__len__() < 3 or ime_entry.get().__len__() > 30:
        messagebox.showinfo(message="Polje 'Prezime' je prazno,počinje brojem ili nije odgovarajuće dužine.")
        return False
    re_ukupan_iznos_entry = re.match("^[1-9]+[0-9]*$", ukupan_iznos_entry.get())
    if not re_ukupan_iznos_entry:
        messagebox.showinfo(message="Polje 'Ukupan iznos' nije popunjeno ili ne sadrži isključivo pozitivne brojeve.")
        return False
    re_uplaceno_entry = re.match(r"[0-9]{1,7}", uplaceno_entry.get())
    if not re_uplaceno_entry:
        messagebox.showinfo(message="Polje 'Uplaćeno pri kupovini' nije popunjeno ili ne sadrži isključivo pozitivne brojeve.")
        return False
    re_datum_prve_rate_entry = re.match(r"^20[0-2][0-9]-((0[1-9])|(1[0-2]))-(0[1-9]|[1-2][0-9]|3[0-1])$", datum_prve_rate_entry.get())
    if not re_datum_prve_rate_entry:
        messagebox.showinfo(message="Polje 'Datum prve rate' nije popunjeno ili nije upisano u ispravnom formatu.Primer 2022-06-24.")
        return False
    re_broj_rata_entry = re.match("^(1[0-2]|[1-9])$", broj_rata_entry.get())
    if not re_broj_rata_entry:
        messagebox.showinfo(message="Polje 'Broj rata' nije popunjeno ili nije u opsegu 1-12.")
        return False
    # if int(broj_rata_entry.get()) * int(float(pojedinacna_rata_entry.get())) != int(ukupan_iznos_entry.get()) - int(uplaceno_entry.get()):
    #     messagebox.showinfo(message="Broj rata pomnozen sa iznosom pojedinacnih rata nije jednak ukupnom iznosu za placanje umanjenom za iznos uplacen pri kupovini")
    #     return False
    if int(ukupan_iznos_entry.get()) < int(uplaceno_entry.get()):
        messagebox.showinfo(message="Iznos uplacen pri kupovini ne moze biti veci od ukupnog iznosa.")
        return False
    return True

def populate_list():
    global counter
    counter = 0
    parts_list.delete(0, END)
    for row in db_sindikalna.fetch():
        # parts_list.insert(END, "ID:"+str(row[0])+" Sindikat:"+row[1]+" Ime:"+row[2]+" Prezime:"+ str(row[3])+ " Ukupno:"+str(row[4])+" Uplaceno pri kupovini"+str(row[5])+" Br.rata:"+str(row[6])+" Iznos svake rate:"+str(row[7]))
        parts_list.insert(END, "ID: "+str(row[0])+"  "+row[2]+"  "+ str(row[3]))
        # parts_list.insert(END, "{:>3}{:<5}".format("ID:",str(row[0]))+"{:>12}{:<30}".format("Sindikat: ",row[1])+"{:>5}{:<30}".format("ime",row[2])+ "{:>10}{:<30}".format("Prezime:",str(row[3])))

def populate_list_date():
    global counter
    counter = 1
    parts_list.delete(0, END)
    for row in db_sindikalna.fetch():
        first_rate_date = datetime.strptime(row[8], "%Y-%m-%d").date()
        for i in range(row[6]):
            if first_rate_date + relativedelta(months=i) >= datetime.now().date():
                # naplata = str(row[1])+" "+row[2]+" "+row[3]+" Ukupno: "+str(row[4])+" Uplaceno: "+str(row[5])+" Datum prve rate: "+str(row[8])+" Br.rata: "+str(row[6])+" iznos svake rate: "+str(row[7])+" redni broj rate: "+str(i+1)+" sledeca rata: "+str(first_rate_date + relativedelta(months=i))
                parts_list.insert(END,"ID:  " + str(row[0]) +' Ime: '+row[2]+ ' Prezime: '+row[3] + "  Rata broj:  "+ str(i+1) +"  stize na naplatu:   "+str(first_rate_date + relativedelta(months=i)))
                break

    # change color for every row
    for i in range(100):
        if parts_list.get(i):
            parts_list.itemconfig(i,{'fg': 'red'})

def populate_list_search():
    global counter
    counter = 2
    parts_list.delete(0, END)

    if sindikat_entry.get() == '' and ime_entry.get() =='' and prezime_entry.get() =='':
        messagebox.showinfo(message='Polja za pretragu su prazna!')
        parts_list.insert(END, 'Upišite pojam za pretragu u polje za naziv sindikata ili u polje za ime ili prezime!')

    for row in db_sindikalna.fetch():
        if row[1] == sindikat_entry.get() and options_variable.get() == 'Sindikat' or row[2] == ime_entry.get() and options_variable.get() == 'Ime' or row[3] == prezime_entry.get() and options_variable.get() == 'Prezime':
            parts_list.insert(END, "ID: "+str(row[0])+"  "+row[2]+"  "+ str(row[3]))

def add_item():
    if regex_check():
        db_sindikalna.insert(sindikat_text.get(), ime_text.get(),
                            prezime_text.get(), ukupan_iznos_text.get(),
                            uplaceno_text.get(),broj_rata_text.get(),
                            pojedinacna_rata_text.get(),datetime.strptime(datum_prve_rate_text.get(), '%Y-%m-%d').date())
        parts_list.delete(0, END)
        parts_list.insert(END, (sindikat_text.get(), ime_text.get(),prezime_text.get(), ukupan_iznos_text.get(), uplaceno_text.get(), broj_rata_text.get(), pojedinacna_rata_text.get(), datum_prve_rate_text.get()))
        clear_text()
        populate_list()

def select_item(event):
    try:
        global selected_item
        global counter
        index = parts_list.curselection()[0]
        lista = []
        lista_date = []
        lista_search = []
        if counter == 0:
            for row in db_sindikalna.fetch():
                lista.append(row)
            # selected_item = lista[index+counter]
            selected_item = lista[index]
            sindikat_entry.delete(0, END)
            sindikat_entry.insert(END, selected_item[1])
            ime_entry.delete(0, END)
            ime_entry.insert(END, selected_item[2])
            prezime_entry.delete(0, END)
            prezime_entry.insert(END, selected_item[3])
            ukupan_iznos_entry.delete(0, END)
            ukupan_iznos_entry.insert(END, selected_item[4])
            uplaceno_entry.delete(0, END)
            uplaceno_entry.insert(END, selected_item[5])
            broj_rata_entry.delete(0, END)
            broj_rata_entry.insert(END, selected_item[6])
            pojedinacna_rata_entry.delete(0, END)
            pojedinacna_rata_entry.insert(END, selected_item[7])
            datum_prve_rate_entry.delete(0, END)
            datum_prve_rate_entry.insert(END, selected_item[8])
        #######################################################
        if counter == 1:
            for row in db_sindikalna.fetch():
                first_rate_date = datetime.strptime(row[8], "%Y-%m-%d").date()
                for i in range(row[6]):
                    if first_rate_date + relativedelta(months=i) >= datetime.now().date():
                        lista_date.append(row)
                        break
            # selected_item = lista[index+counter]
            selected_item = lista_date[index]
            sindikat_entry.delete(0, END)
            sindikat_entry.insert(END, selected_item[1])
            ime_entry.delete(0, END)
            ime_entry.insert(END, selected_item[2])
            prezime_entry.delete(0, END)
            prezime_entry.insert(END, selected_item[3])
            ukupan_iznos_entry.delete(0, END)
            ukupan_iznos_entry.insert(END, selected_item[4])
            uplaceno_entry.delete(0, END)
            uplaceno_entry.insert(END, selected_item[5])
            broj_rata_entry.delete(0, END)
            broj_rata_entry.insert(END, selected_item[6])
            pojedinacna_rata_entry.delete(0, END)
            pojedinacna_rata_entry.insert(END, selected_item[7])
            datum_prve_rate_entry.delete(0, END)
            datum_prve_rate_entry.insert(END, selected_item[8])
            #################################################
        if counter == 2:
            for row in db_sindikalna.fetch():
                if row[1] == sindikat_entry.get() and options_variable.get() == 'Sindikat' or row[2] == ime_entry.get() and options_variable.get() == 'Ime' or row[3] == prezime_entry.get() and options_variable.get() == 'Prezime':
                    lista_search.append(row)
            selected_item = lista_search[index]
            sindikat_entry.delete(0, END)
            sindikat_entry.insert(END, selected_item[1])
            ime_entry.delete(0, END)
            ime_entry.insert(END, selected_item[2])
            prezime_entry.delete(0, END)
            prezime_entry.insert(END, selected_item[3])
            ukupan_iznos_entry.delete(0, END)
            ukupan_iznos_entry.insert(END, selected_item[4])
            uplaceno_entry.delete(0, END)
            uplaceno_entry.insert(END, selected_item[5])
            broj_rata_entry.delete(0, END)
            broj_rata_entry.insert(END, selected_item[6])
            pojedinacna_rata_entry.delete(0, END)
            pojedinacna_rata_entry.insert(END, selected_item[7])
            datum_prve_rate_entry.delete(0, END)
            datum_prve_rate_entry.insert(END, selected_item[8])
    except IndexError:
        pass

def remove_item():
    remove_boolean = messagebox.askyesno(message="Da li zaista želite da obrišete izabrani podatak?")
    if remove_boolean:
        db_sindikalna.remove(selected_item[0])
        clear_text()
        populate_list()

def update_item():
    if regex_check():
        db_sindikalna.update(selected_item[0], sindikat_text.get(), ime_text.get(),
                  prezime_text.get(), ukupan_iznos_text.get(),uplaceno_entry.get(),
                  broj_rata_text.get(), pojedinacna_rata_text.get(), datum_prve_rate_text.get())
        populate_list()

def clear_text():
    sindikat_entry.delete(0, END)
    ime_entry.delete(0, END)
    prezime_entry.delete(0, END)
    ukupan_iznos_entry.delete(0, END)
    broj_rata_entry.delete(0, END)
    datum_prve_rate_entry.delete(0, END)
    pojedinacna_rata_entry.delete(0, END)
    uplaceno_entry.delete(0, END)
# Create window object
app = Tk()

# Labels and Entry fields
# Union
sindikat_text = StringVar()
sindikat_label = Label(app, text='Sindikat', font=('bold', 14))
sindikat_label.grid(row=2, column=0, sticky=W, pady=(100,10), padx=(50,5))
sindikat_entry = Entry(app, textvariable=sindikat_text, width=20)
sindikat_entry.grid(row=2, column=1, pady=(100,10), padx=30)
# First name
ime_text = StringVar()
ime_label = Label(app, text='Ime', font=('bold', 14))
ime_label.grid(row=3, column=0, sticky=W, pady=(0,10), padx=(50,5))
ime_entry = Entry(app, textvariable=ime_text)
ime_entry.grid(row=3, column=1, pady=(0,10), padx=30)
# Last name
prezime_text = StringVar()
prezime_label = Label(app, text='Prezime', font=('bold', 14))
prezime_label.grid(row=4, column=0, sticky=W, pady=(0,10), padx=(50,5))
prezime_entry = Entry(app, textvariable=prezime_text)
prezime_entry.grid(row=4, column=1, pady=(0,10), padx=30)
# Total amount
ukupan_iznos_text = IntVar()
ukupan_iznos_label = Label(app, text='Ukupan iznos', font=('bold', 14))
ukupan_iznos_label.grid(row=5, column=0, sticky=W, pady=(0,10), padx=(50,5))
ukupan_iznos_entry = Entry(app, textvariable=ukupan_iznos_text)
ukupan_iznos_entry.grid(row=5, column=1, pady=(0,10), padx=30)
# Label and Entry for the amount paid at the time of purchase
uplaceno_label = Label(app, text='Uplaćeno pri kupovini', font=('bold', 14))
uplaceno_label.grid(row=6, column=0, sticky=W, pady=(0,10), padx=(50,5))
uplaceno_text = IntVar()
uplaceno_entry = Entry(app, textvariable=uplaceno_text)
uplaceno_entry.grid(row=6, column=1, pady=(0,10), padx=30)
# Date for first rate
datum_prve_rate_text = StringVar()
datum_prve_rate_label = Label(app, text='Datum prve rate(format:yyyy-mm-dd)', font=('bold', 14))
datum_prve_rate_label.grid(row=7, column=0, sticky=W, pady=(0,10), padx=(50,5))
datum_prve_rate_entry = Entry(app, textvariable=datum_prve_rate_text)
datum_prve_rate_entry.grid(row=7, column=1, pady=(0,10), padx=50)
# Number of rates
BROJEVI = list(range(1,13))
broj_rata_text = IntVar()
broj_rata_label = Label(app, text='Broj rata', font=('bold', 14))
broj_rata_label.grid(row=8, column=0, sticky=W, pady=(0,10), padx=(50,5))
broj_rata_entry = Entry(app, textvariable=broj_rata_text)
broj_rata_entry.grid(row=8, column=1, sticky=W, pady=(0,10), padx=(50,5))
# Label and Entry for value of single rate
pojedinacna_rata_label = Label(app, text='Iznos pojedinačnih rata', font=('bold', 14))
pojedinacna_rata_label.grid(row=9, column=0, sticky=W, pady=(0,10), padx=(50,5))
pojedinacna_rata_text = IntVar()
pojedinacna_rata_entry = Entry(app, textvariable=pojedinacna_rata_text)
pojedinacna_rata_entry.grid(row=9, column=1, pady=(0,10), padx=30)
izracunaj_rate_btn = Button(app, text='Izračunaj', width=12, command=set_number_of_rates)
izracunaj_rate_btn.grid(row=10, column=1)
# Parts List (Listbox)
# small_font = tkFont.Font(size=10)
parts_list = Listbox(app, height=15, width=80, border=0)
parts_list.grid(row=2, column=5, columnspan=6, rowspan=6, pady=(100,0), padx=(0,0))
# Create scrollbar
scrollbar = Scrollbar(app, orient='vertical')
scrollbar.grid(row=3, column=11, sticky=NS)
# Set scroll to listbox
parts_list.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=parts_list.yview)
# Bind select
parts_list.bind('<<ListboxSelect>>', select_item)
# Buttons
add_btn = Button(app, text='Dodaj podatak', width=12, command=add_item)
add_btn.grid(row=9, column=5)

remove_btn = Button(app, text='Obriši podatak', width=12, command=remove_item)
remove_btn.grid(row=9, column=6)

update_btn = Button(app, text='Izmeni podatak', width=12, command=update_item)
update_btn.grid(row=10, column=6)

clear_btn = Button(app, text='Obriši sva polja', width=12, command=clear_text)
clear_btn.grid(row=9, column=8)

# Option menu
search_options = ['Sindikat', 'Ime', 'Prezime']
options_variable = StringVar()
options_variable.set('Pojam za pretragu')
search_option_menu = OptionMenu(app, options_variable, *search_options)
search_option_menu.grid(row=10, column=7)

charge_btn = Button(app, text='Uskoro za naplatu', width=15, command=populate_list_date)
charge_btn.grid(row=9, column=7)

show_btn = Button(app, text='Svi podaci', width=12, command=populate_list)
show_btn.grid(row=10, column=5)

search_btn = Button(app, text='Pretraga', width=12, command=populate_list_search)
search_btn.grid(row=10, column=8)

app.title('Sindikalna prodaja')
app.geometry( '1100x500' )

# Populate data
populate_list()

# Start program
app.mainloop()