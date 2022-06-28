import sqlite3
# podaci
# id, sindikat, ime, prezime, ukupan iznos, uplaceno, broj rata, pojedinacna rata, datum prve rate

class Database:
    def __init__(self, db_sindikalna):
        self.conn = sqlite3.connect(db_sindikalna)
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS sindikalci (id INTEGER PRIMARY KEY, sindikat text, ime text, prezime text, ukupan_iznos int, uplaceno int, broj_rata int,pojedinacna_rata int, datum_prve_rate text)")
        self.conn.commit()

    def fetch(self):
        self.cur.execute("SELECT * FROM sindikalci")
        rows = self.cur.fetchall()
        return rows

    def fetchDate(self):
        self.cur.execute("SELECT * FROM sindikalci WHERE ime='aca'")
        row = self.cur.fetchall()
        return row

    def insert(self, sindikat, ime, prezime, ukupan_iznos, uplaceno, broj_rata,pojedinacna_rata, datum_prve_rate):
        self.cur.execute("INSERT INTO sindikalci VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?)",
                         (sindikat, ime, prezime, ukupan_iznos, uplaceno, broj_rata,pojedinacna_rata, datum_prve_rate))
        self.conn.commit()

    def remove(self, id):
        self.cur.execute("DELETE FROM sindikalci WHERE id=?", (id,))
        self.conn.commit()

    def update(self, id, sindikat, ime, prezime, ukupan_iznos, uplaceno, broj_rata,pojedinacna_rata, datum_prve_rate):
        self.cur.execute("UPDATE sindikalci SET sindikat = ?, ime = ?, prezime = ?, ukupan_iznos = ?, uplaceno = ?, broj_rata = ?, pojedinacna_rata = ?, datum_prve_rate = ? WHERE id = ?",
                         (sindikat, ime, prezime, ukupan_iznos, uplaceno, broj_rata,pojedinacna_rata, datum_prve_rate, id))
        self.conn.commit()

    def __del__(self):
        self.conn.close()
