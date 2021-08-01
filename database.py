import sqlite3

def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance

@singleton
class Conn:
    
    def get_cursor(self) -> None:
        self.con = sqlite3.connect('db.sqlite')
        self.cur = self.con.cursor()

    def migrate(self) -> None:
        self.run_query('''CREATE TABLE IF NOT EXISTS files
                    (
                        id integer PRIMARY KEY,
                        file_path text NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )''')
                    # Insert a row of data
    
    def run_query(self, query, args = list()) -> None:
        self.get_cursor()
        self.cur.execute(query, args)
        self.con.commit()
        self.con.close()

    def save(self, file_path) -> None:
        query = "INSERT INTO files(file_path) VALUES(?)"
        self.run_query(query, [file_path])
    
    def update(self, file_path, new_file_path) -> None:
        query = "UPDATE files SET file_path = ? WHERE file_path = ?"
        self.run_query(query, [new_file_path, file_path])

    def delete(self, file_path) -> None:
        query = "DELETE FROM files WHERE file_path = ?"
        self.run_query(query, [file_path])

    def get_all(self, order = 'id') -> list:
        query = "SELECT * FROM files ORDER BY ?"
        self.get_cursor()
        self.cur.execute(query, [order])
        files = self.cur.fetchall()
        self.con.commit()
        self.con.close()

        return files


if __name__ == '__main__':
    w = Conn()
    w.migrate()
