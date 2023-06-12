from tkinter import *
from DataBase import DB

# обработчик нажатия на кнопку «Посмотреть всё»
def view_command():         
    # очищаем список в приложении
    list1.delete(0, END)    
    # проходим все записи в БД
    for row in db.view():   
        # и сразу добавляем их на экран
        list1.insert(END, row)

# обработчик нажатия на кнопку «Добавить»
def add_command():         
    # добавляем запись в БД
    db.insert(product_text.get(), price_text.get(), comment_text.get()) 
    # обновляем общий список в приложении
    view_command()
    
# заполняем поля ввода значениями выделенной позиции в общем списке
def get_selected_row(event): 
    # будем обращаться к глобальной переменной
    global selected_tuple
    # получаем позицию выделенной записи в списке
    index = list1.curselection() #this is the id of the selected tuple
    # получаем значение выделенной записи
    selected_tuple = list1.get(index) 
    # удаляем то, что было раньше в поле ввода
    e1.delete(0, END)                
    # и добавляем туда текущее значение названия покупки
    e1.insert(END, selected_tuple[1]) 
    # делаем то же самое с другими полями
    e2.delete(0, END)
    e2.insert(END, selected_tuple[2]) 
    e3.delete(0, END)
    e3.insert(END, selected_tuple[3]) 
    
# обработчик нажатия на кнопку «Поиск»
def search_command():       
    # очищаем список в приложении
    list1.delete(0, END)   
    # находим все записи по названию покупки
    for row in db.search(product_text.get()):
        # и добавляем их в список в приложение
        list1.insert(END, row) 

# обработчик нажатия на кнопку «Удалить»
def delete_command(): 
    # удаляем запись из базы данных по индексу выделенного элемента
    db.delete(selected_tuple[0]) 
    # обновляем общий список расходов в приложении
    view_command()

# обработчик нажатия на кнопку «Обновить»
def update_command():
    # обновляем данные в БД о выделенной записи
    db.update(selected_tuple[0], product_text.get(), price_text.get(), comment_text.get()) 
    # обновляем общий список расходов в приложении
    view_command()
    
def finish():
    window.destroy()  # ручное закрытие окна и всего приложения
    print("Закрытие приложения")
    
# обрабатываем закрытие окна
def on_closing(): 
    # показываем диалоговое окно с кнопкой
    if messagebox.askokcancel("", "Закрыть программу?"): 
        # удаляем окно и освобождаем память
        window.destroy()

print("Открытие приложения")

# создаём экземпляр базы данных на основе класса
db = DB()
window = Tk()
window.title("Бюджет v0.1")
window.attributes("-toolwindow", False)

# создаём надписи для полей ввода и размещаем их по сетке
l1 = Label(window, text="Название") 
l1.grid(row=0, column=0) 

l2 = Label(window, text="Стоимость")
l2.grid(row=0, column=2)

l3 = Label(window, text="Комментарий")
l3.grid(row=1, column=0)

# создаём поле ввода названия покупки, говорим, что это будут строковые переменные и размещаем их тоже по сетке
product_text = StringVar()
e1 = Entry(window, textvariable=product_text)
e1.grid(row=0, column=1)

# то же самое для комментариев и цен
price_text = StringVar() 
e2 = Entry(window, textvariable=price_text)
e2.grid(row=0, column=3)

comment_text = StringVar() 
e3 = Entry(window, textvariable=comment_text)
e3.grid(row=1, column=1)

# создаём список, где появятся наши покупки, и сразу определяем его размеры в окне
list1 = Listbox(window, height=25, width=80) 
list1.grid(row=2, column=0, rowspan=6, columnspan=2) 
# привязываем выбор любого элемента списка к запуску функции выбора
list1.bind('<<ListboxSelect>>', get_selected_row)

# на всякий случай добавим сбоку скролл, чтобы можно было быстро прокручивать длинные списки
sb1 = Scrollbar(window) 
sb1.grid(row=2, column=2, rowspan=6)

# привязываем скролл к списку
list1.configure(yscrollcommand=sb1.set) 
sb1.configure(command=list1.yview)

# создаём кнопки действий и привязываем их к своим функциям
# кнопки размещаем тоже по сетке
b1 = Button(window, text="Посмотреть все", width=12, command=view_command) 
b1.grid(row=2, column=3) #size of the button

b2 = Button(window, text="Поиск", width=12, command=search_command)
b2.grid(row=3, column=3)

b3 = Button(window, text="Добавить", width=12, command=add_command)
b3.grid(row=4, column=3)

b4 = Button(window, text="Обновить", width=12, command=update_command)
b4.grid(row=5, column=3)

b5 = Button(window, text="Удалить", width=12, command=delete_command)
b5.grid(row=6, column=3)

b6 = Button(window, text="Закрыть", width=12, command=on_closing)
b6.grid(row=7, column=3)

window.protocol("WM_DELETE_WINDOW", on_closing)

window.mainloop()
