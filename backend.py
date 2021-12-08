import sqlite3


class DatabaseContextManeger:
    """Database with Context Manager"""

    def __init__(self, database):
        self.__database = database
        self.__conn = None
        self.__curr = None


    @property
    def database(self):
        return self.__database

    @property
    def connection(self):
        return self.__conn

    @property
    def cursor(self):
        return self.__curr 

    def __enter__(self):
        self.__conn = sqlite3.connect(self.database)
        self.__curr = self.__conn.cursor()
        self.create_database()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_type:
            print(f"*** Error occured: {exc_type}, {exc_value}")
        self.__conn.commit()
        self.__curr.close()
        return False


    def create_database(self):
        """ Create database """

        self.__curr.execute("CREATE TABLE IF NOT EXISTS book \
            (id INTEGER PRIMARY KEY,\
            title text, author text,\
            year integer, isbn integer)")

        
        
    def insert(self, title, author, year, isbn):
        """Insert data to database
        Parameters:
            title(str): Name of book
            author(str): Author name
            year(str): Year of book
            isbn(str): barcode
        """
        self.__curr.execute("INSERT INTO book VALUES (NULL,?,?,?,?)",
                (title, author, year, isbn))


    def view(self):
        """View data in database
        
        Return:
            list: list of data 
        """
        self.__curr.execute("SELECT * FROM book")
        rows = self.__curr.fetchall()
        return rows


    def search(self, title="", author="", year="", isbn=""):
        """Search data in database
        Parameters:
            title(str): Name of book
            author(str): Author name
            year(str): Year of book
            isbn(str): isbn
        Returns:
            list: list of data
        """
        self.__curr.execute("SELECT * FROM book WHERE title=? OR author=? OR year=? OR isbn=?",
            (title, author, year, isbn))
        rows = self.__curr.fetchall()
        return rows


    def delete(self, title='', author='', isbn=''):
        """Delete data in database
        Parameters:
            title(str): Name of book
            author(str): Author name
            isbn(str): isbn
        Returns: None
        """
        self.__curr.execute("DELETE FROM book WHERE title=? OR (author=? AND isbn=?)",
                (title, author, isbn))


    def update(self, id_, title, author, year, isbn):
        """Update data to database
        Parameters:
            title(str): Name of book
            year(str): Year of book
            author(str): Author name
            isbn(str): isbn
        Returns: None
        """

        self.__curr.execute("UPDATE book SET title=?, author=?, year=?, isbn=? WHERE id=?",
            (title, author, year, isbn, id_))


if __name__ == '__main__':
    database = DatabaseContextManeger('books.db')

    with database as db:
        print(db.view())

    # pprint(db.view())
    # print()

    # # insert("Shorklock home", "pop sakkara", 1996, 2334349)
    # # insert("The moon", "John Cleese", 1991, 3234545)
    # db.delete('The moon', 'John Cleese')
    # pprint(db.view())

    # db.close_database()