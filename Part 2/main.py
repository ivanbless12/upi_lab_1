import sqlite3
import sys

if __name__ == '__main__':
    db_path = sys.argv[-1]
    try:
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        res = cur.execute("SELECT student_id, mark FROM exam_results")
    except Exception as e:
        print(f'The database could not be opened at the specified path ({db_path})!\nMake sure that the path to the database is set correctly.')
        exit(1)
    av_mark = dict()
    for row in res.fetchall():
        if row[0] in av_mark.keys():
            av_mark[row[0]] = (av_mark[row[0]] + row[1])/2
        else:
            av_mark[row[0]] = row[1]
    best_student_id = (max(av_mark, key=av_mark.get))
    res = cur.execute(("SELECT fio_name FROM students WHERE id=?"), (best_student_id,))
    best_student_name = res.fetchone()[0]
    res = cur.execute(("SELECT disciplines.name, exam_results.mark FROM disciplines JOIN exam_results ON exam_results.descipline_id = disciplines.id WHERE exam_results.student_id=?"), (best_student_id,))
    disciplines_info = str()
    for discipline_mark in res.fetchall():
        disciplines_info += '\n' + str(discipline_mark[0]) + ": " + str(discipline_mark[1])
    print(f"Top student: {best_student_name}\nAverage mark: {av_mark[best_student_id]}\n\nDisciplines:{disciplines_info}")
    cur.close()
    con.close()