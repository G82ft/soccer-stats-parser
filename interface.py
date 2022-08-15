from threading import Thread
from time import sleep
from tkinter import (
    Tk, Frame, Label, OptionMenu, Spinbox, Checkbutton, Button,
    StringVar, IntVar
)
from tkinter.messagebox import showerror, showinfo

from main import get_leagues, dump_table

VALUES: tuple = (
    'First',
    'Second',
    'Third',
    '. . .'
)


def flash(element):
    def _flash(element):
        default_color = element["bg"]
        for _ in range(3):
            element["bg"] = 'pink'
            sleep(0.25)
            element["bg"] = default_color
            sleep(0.25)

    Thread(target=_flash, args=(element,))


class Root:
    def __init__(self):
        self.root = Tk()

        self.root.title('Soccer statistics parser')
        self.root.geometry('500x250')

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        main = Frame(
            self.root
        )
        main.grid(sticky='nesw')

        for i in range(4):
            main.columnconfigure(i, weight=1)
        for i in range(7):
            main.rowconfigure(i, weight=1)

        self.objects: dict[Label: OptionMenu | Label | Spinbox | Checkbutton] = {}
        self.variables: dict = {}

        self._setup_leagues(main)

        k = Label(
            main,
            text='Количество матчей',
            justify='left'
        )

        self.amount = IntVar()
        v = Spinbox(
            main,
            textvariable=self.amount,
            width=3,
            from_=1,
            to=100,
            increment=1
        )

        self.objects[k] = v

        k = Label(
            main,
            text='Из текущего сезона',
            justify='left'
        )

        self.current_season = IntVar()
        v = Checkbutton(
            main,
            variable=self.current_season,
            onvalue=True,
            offvalue=False
        )

        self.objects[k] = v

        for i, (k, v) in enumerate(self.objects.items()):
            k.grid(column=1, row=i + 1, sticky='w')
            v.grid(column=2, row=i + 1, sticky='e')

        Button(
            main,
            text='Ok',
            command=self.ok
        ).grid(column=2, row=5, sticky='e')

    def _setup_leagues(self, main: Frame):
        leagues = []

        k = Label(
            main,
            text='Лига',
            justify='left'
        )

        for i, league in enumerate(get_leagues()):
            leagues.append(league)

        self.leagues: dict = dict(leagues)

        self.league = StringVar()
        v = OptionMenu(
            main,
            self.league,
            *self.leagues
        )
        v["width"] = max(len(i) for i in self.leagues)

        self.objects[k] = v

    def ok(self):
        if not self.league.get():
            flash(tuple(self.objects.values())[0])
            return

        showinfo('Process', 'Пожалуйста, дожитесь конца парсинга.')

        try:
            for i in dump_table(
                    self.leagues[self.league.get()],
                    self.amount.get(),
                    bool(self.current_season.get())
            ):
                if isinstance(i, float):
                    showinfo('Process', f'Заполнение листа {int(i)}...')
        except Exception as e:
            showerror('Process', f'Произошла ошибка!\n{e}')
        else:
            showinfo('Process', 'Парсинг окончен.')


Root().root.mainloop()
