from __init__ import CURSOR, CONN
from department import Department
from employee import Employee


class Review:
    def __init__(self, id=None, year=None, summary=None, employee_id=None):
        self.id = id
        self.year = year
        self.summary = summary
        self.employee_id = employee_id

    def save(self):
        sql = """
            INSERT INTO reviews (year, summary, employee_id)
            VALUES (?, ?, ?)
        """
        CURSOR.execute(sql, (self.year, self.summary, self.employee_id))
        CONN.commit()
        
        sql = "SELECT last_insert_rowid()"
        self.id = CURSOR.execute(sql).fetchone()[0]

    @classmethod
    def create(cls, year, summary, employee_id):
        sql = """
            INSERT INTO reviews (year, summary, employee_id)
            VALUES (?, ?, ?)
        """
        CURSOR.execute(sql, (year, summary, employee_id))
        CONN.commit()
        
        sql = "SELECT last_insert_rowid()"
        review_id = CURSOR.execute(sql).fetchone()[0]
        return cls.instance_from_db((review_id, year, summary, employee_id))

    @classmethod
    def instance_from_db(cls, row):
        if row:
            id, year, summary, employee_id = row
            return cls(id=id, year=year, summary=summary, employee_id=employee_id)
        return None

    @classmethod
    def find_by_id(cls, review_id):
        sql = "SELECT * FROM reviews WHERE id = ?"
        row = CURSOR.execute(sql, (review_id,)).fetchone()
        return cls.instance_from_db(row)

    def update(self):
        sql = """
            UPDATE reviews SET year = ?, summary = ?, employee_id = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.year, self.summary, self.employee_id, self.id))
        CONN.commit()

    def delete(self):
        sql = "DELETE FROM reviews WHERE id = ?"
        CURSOR.execute(sql, (self.id,))
        CONN.commit()

    @classmethod
    def get_all(cls):
        sql = "SELECT * FROM reviews"
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]


