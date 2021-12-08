from tkinter import *
from tkinter import messagebox
from backend import DatabaseContextManeger



class GUI(Tk):
    selected_data = ''
    database = DatabaseContextManeger('books.db')

    def __init__(self, *args, **kwags) -> None:
        super().__init__(*args, **kwags)
        
        self.title('BookStore')
        self.resizable(False, False)
        self['padx'] = 5
        self['pady'] = 5

        self.l1 = Label(self, text='Title')
        self.l2 = Label(self, text='Year')
        self.l3 = Label(self, text='Author')
        self.l4 = Label(self, text='ISBN')

        self.l1.grid(row=0, column=0)
        self.l2.grid(row=1, column=0)
        self.l3.grid(row=0, column=2)
        self.l4.grid(row=1, column=2)

        self.title_text = StringVar()
        self.author_text = StringVar()
        self.year_text = StringVar()
        self.isbn_text = StringVar()

        self.e1 = Entry(self, textvariable=self.title_text)
        self.e2 = Entry(self, textvariable=self.author_text)
        self.e3 = Entry(self, textvariable=self.year_text)
        self.e4 = Entry(self, textvariable=self.isbn_text)

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=0, column=3)
        self.e3.grid(row=1, column=1)
        self.e4.grid(row=1, column=3)

        self.list1 = Listbox(self, height=6, width=35)
        self.list1.grid(row=2, column=0, rowspan=6, columnspan=2)

        self.sb1 = Scrollbar(self)
        self.sb1.grid(row=2, column=2, rowspan=6)

        self.list1.configure(yscrollcommand=self.sb1.set)
        self.sb1.configure(command=self.list1.yview)

        self.list1.bind('<<ListboxSelect>>', self.get_selected_row)

        self.b1 = Button(self, text='View all', width=12, command=self.view_command)
        self.b2 = Button(self, text='Search', width=12, command=self.search_command)
        self.b3 = Button(self, text='Add', width=12, command=self.add_command)
        self.b4 = Button(self, text='Update', width=12, command=self.update_command)
        self.b5 = Button(self, text='Delete', width=12, command=self.delete_command)
        self.b6 = Button(self, text='Close', width=12, command=self.destroy)

        self.b1.grid(row=2, column=3)
        self.b2.grid(row=3, column=3)
        self.b3.grid(row=4, column=3)
        self.b4.grid(row=5, column=3)
        self.b5.grid(row=6, column=3)
        self.b6.grid(row=7, column=3)


        self.mainloop()



    def check_special_characters(self, text: str='', c_int=False):
            """Check special charecters and number
            Parameters:
                text(str): for check charecters
                c_int(bool): for check number
            Returns:
                bool: bool check
            """
            special_characters =  """!@#$%^&*()-+?_=,<>/"""
            if c_int:
                return  any(c not in list('0123456789') for c in text)
            return any(c in special_characters for c in text)


    def format_data_insert(self, row: tuple):
            """For view data 
            Parameters:
                row(tuple): data [e.g. (id, title, author, year, isbn)]
            Returns:
                str: formatting data
            """
            return f"{row[1]} : {row[2]} : {row[3]} : {row[4]}"


    def get_selected_row(self, event):
        global selected_data

        index = self.list1.curselection()
        if index:
            index = self.list1.curselection()[0]
            selected_data = self.list1.get(index).split(' : ')
            title = selected_data[0]
            author = selected_data[1]
            year = selected_data[2]
            barcode = selected_data[-1]

            self.clear_entry_value()
            self.e1.insert(END, title)
            self.e2.insert(END, author)
            self.e3.insert(END, year)
            self.e4.insert(END, barcode)

            return selected_data
        return ''


    def view_command(self):
        self.clear_text_value()
        self.list1.delete(0, END)
        
        with GUI.database as db:
            for row in db.view():
                format_data = self.format_data_insert(row)
                self.list1.insert(END, format_data)


    def search_command(self):
        self.list1.delete(0, END)
        try:
            title = self.title_text.get()
            author = self.author_text.get()
            year = self.year_text.get()
            isbn = self.isbn_text.get()
            c_title = self.check_special_characters(title)
            c_author = self.check_special_characters(author)
            c_year = self.check_special_characters(year, c_int=True)
            c_isbn = self.check_special_characters(isbn, c_int=True)

            if any((c_title, c_author, c_year, c_isbn)):
                raise ValueError

        except ValueError as err:
            print(err)
            messagebox.showerror('Error', 'Please not use special characters.')
        else:
            if  title or author or year or isbn:
                with GUI.database as db:
                    for row in db.search(title, author, year, isbn):
                        fm_data = self.format_data_insert(row)
                        self.list1.insert(END, fm_data)


    def add_command(self):
        try:
            title = self.title_text.get()
            author = self.author_text.get()
            year = self.year_text.get()
            isbn = self.isbn_text.get()

            c_title = self.check_special_characters(title)
            c_author = self.check_special_characters(author)
            c_year = self.check_special_characters(year, c_int=True)
            c_isbn = self.check_special_characters(isbn, c_int=True)

            if any((c_title, c_author, c_year, c_isbn)):
                raise ValueError

        except ValueError as err:
            print(err)
            messagebox.showwarning('Error', 
            'don\'t use ```!@#$%^&*()-+?_=,<>/``` and check type of data.')
        else:
            if  title and author and year and isbn:
                with GUI.database as db:
                    db.insert(title, author, year, isbn)

                self.list1.delete(0, END)
                fm_data = self.format_data_insert((None, title, author, year, isbn))
                self.list1.insert(END, fm_data)
                messagebox.showinfo('success', message='completed')
                self.clear_text_value()


    def delete_command(self):
        data = self.get_selected_row('')
        if data:
            author = data[1]
            barcode = data[-1]
            with GUI.database as db:
                db.delete(author=author, isbn=barcode)
            self.view_command()
            messagebox.showinfo('success', message='book is deleted')


    def update_command(self):
        if selected_data:
            author = selected_data[1]
            barcode = selected_data[-1]
            
            title_new = self.e1.get()
            author_new = self.e2.get()
            year_new = self.e3.get()
            isbn_new = self.e4.get()

            with GUI.database as db:
                search = db.search(author=author, isbn=barcode)[0]
                db.update(search[0], title_new, author_new, year_new, isbn_new)
            self.view_command()
            messagebox.showinfo('success', message='book is updated')


    def clear_entry_value(self):
        self.e1.delete(0, END)
        self.e2.delete(0, END)
        self.e3.delete(0, END)
        self.e4.delete(0, END)


    def clear_text_value(self):
        self.title_text.set('')
        self.e1.focus()
        self.author_text.set('')
        self.year_text.set('')
        self.isbn_text.set('')

if __name__ == '__main__':
    gui = GUI()