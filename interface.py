from tkinter import (
    Tk, Frame, Label, OptionMenu, Spinbox, Checkbutton, StringVar, IntVar
)

VALUES: tuple = (
    'First',
    'Second',
    'Third',
    '. . .'
)


class Root:
    def __init__(self):
        self.root = Tk()

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.title('Soccer statistics parser')

        main = Frame(
            self.root
        )
        main.grid()

        for i in range(4):
            main.columnconfigure(i, weight=1)
        for i in range(6):
            main.rowconfigure(i, weight=1)

        Label(
            main,
            text='Лига',
            justify='left'
        ).grid(column=1, row=1, sticky='w')

        league = StringVar()
        m = OptionMenu(
            main,
            league,
            *VALUES
        )
        m.grid(column=2, row=1, sticky='e')
        m["width"] = max(len(i) for i in VALUES)

        Label(
            main,
            text='Команда',
            justify='left'
        ).grid(column=1, row=2, sticky='w')

        team = StringVar()
        m = OptionMenu(
            main,
            team,
            *VALUES
        )
        m.grid(column=2, row=2, sticky='e')
        m["width"] = max(len(i) for i in VALUES)

        Label(
            main,
            text='Год'
        ).grid(column=1, row=3, sticky='w')

        year = IntVar()
        Spinbox(
            main,
            textvariable=year,
            width=4,
            from_=2000,
            to=2022,
            increment=1
        ).grid(column=2, row=3, sticky='e')

        Label(
            main,
            text='Количество матчей',
            justify='left'
        ).grid(column=1, row=4, sticky='w')

        amount = IntVar()
        Spinbox(
            main,
            textvariable=amount,
            width=3,
            from_=1,
            to=100,
            increment=1
        ).grid(column=2, row=4, sticky='e')

        Label(
            main,
            text='Из текущего сезона',
            justify='left'
        ).grid(column=1, row=5, sticky='w')

        current_season = IntVar()
        Checkbutton(
            main,
            variable=current_season
        ).grid(column=2, row=5, sticky='e')


Root().root.mainloop()
