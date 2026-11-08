from datetime import datetime, timedelta
import calendar
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return f"{self.task}"



engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

session = Session()

table = Table()


def show_tasks_by_day(selected_day, day_name):
    print(f"{day_name} {selected_day.strftime('%-d %b')}:")

    rows_s = session.query(Table).filter(Table.deadline == selected_day.date()).all()
    if rows_s.__len__() > 0:
        for i in range(rows_s.__len__()):
            if rows_s[i].deadline == selected_day.date():
                print(f"{i + 1}. {rows_s[i]}")
        print()
    else:
        print("Nothing to do!")
        print()


def today_tasks():
    show_tasks_by_day(datetime.today(), 'Today')


def week_tasks():
    today = datetime.today()

    for d in range(7):
        current_day = today + timedelta(days=d)
        current_day_on_week = calendar.day_name[current_day.weekday()]
        show_tasks_by_day(current_day, current_day_on_week)


def all_tasks():
    # global rows_all, i
    print("All tasks:")
    rows_all = get_all_tasks()

    for i in range(rows.__len__()):
        print(f"{i + 1}. {rows_all[i].task}. {rows_all[i].deadline.strftime('%-d %b')}")
    print()


def get_all_tasks() -> list[Any]:
    return session.query(Table).order_by(Table.deadline).all()


def missed_tasks():
    global i
    print("Missed tasks:")
    rows_missed = session.query(Table).filter(Table.deadline < datetime.today()).order_by(Table.deadline).all()

    if rows_missed.__len__() == 0:
        print("All tasks have been completed!")
        print()
        return
    else:
        for i in range(rows_missed.__len__()):
            print(f"{i + 1}. {rows_missed[i].task}. {rows_missed[i].deadline.strftime('%-d %b')}")
    print()


def add_task():
    print("Enter a task")
    task_description = input()
    print("Enter a deadline")
    deadline = input()
    task_deadline = datetime.strptime(deadline, '%Y-%m-%d')
    new_row = Table(task=task_description, deadline=task_deadline.date())
    session.add(new_row)
    session.commit()
    print("The task has been added!")
    print()


def delete_task():
    rows_all = get_all_tasks()
    if rows_all.__len__() == 0:
        print("Nothing to delete")
        print()
        return
    else:
        print("Choose the number of the task you want to delete:")
        for i in range(rows_all.__len__()):
            print(f"{i + 1}. {rows_all[i].task}. {rows_all[i].deadline.strftime('%-d %b')}")

        task_number = int(input())
        rows_all = get_all_tasks()
        session.delete(rows_all[task_number - 1])
        session.commit()
        print("The task has been deleted!")
        print()


def exit_app():
    print("Bye!")
    exit()


while True:
    print("1) Today's tasks")
    print("2) Week's tasks")
    print("3) All tasks")
    print("4) Missed tasks")
    print("5) Add a task")
    print("6) Delete a task")
    print("0) Exit")

    n = int(input())
    print()
    rows = session.query(Table).all()

    if n == 0:
        exit_app()

    elif n == 1:
        today_tasks()

    elif n == 2:
        week_tasks()

    elif n == 3:
        all_tasks()

    elif n == 4:
        missed_tasks()

    elif n == 5:
        add_task()

    elif n == 6:  # delete a task
        delete_task()
