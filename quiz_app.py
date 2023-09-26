"""
Paradigms Of Programming:Coursework
Author: Radoslav Gadzhovski
Date started: 09/11/2021
Purposes:
    - Create a quiz application with GUI using tkinter
Version:1.4
"""

# importing libraries
from tkinter import *
from tkinter import messagebox, ttk
import csv
import sqlite3
import os

cor_wron = []
# empty dictionary to store the quiz name as key and the score as it's value 
quiz_score = {}
# score count
score = 0


# database function that creates and connects to the database and creates the user table
def database_conn():
    global conn, cursor
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `user` (user_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, firstname TEXT, surname TEXT, username TEXT, password TEXT)")


# login function
def login():
    database_conn()
    # check if username, password are not empty else showing error
    if username.get() == "" or password.get() == "":
        messagebox.showerror("Empty Fields", "Please enter both username and password!")
    # if entered
    else:
        # checking if username, password exists in database
        cursor.execute("SELECT * FROM `user` WHERE `username` = ? AND `password` = ?", (username.get(), password.get()))
        # if yes then going to main window
        if cursor.fetchone() is not None:
            home()
        # else showing error
        else:
            messagebox.showerror("Invalid User", "The Username or Password is incorrect. Try Again")
            username.delete(0, END)
            password.delete(0, END)
    cursor.close()
    conn.close()


def admin_log():
    def log_back():
        up.destroy()
        log.deiconify()
        username.delete(0, END)
        password.delete(0, END)

    admin_username = 'Admin'
    admin_pass = '1234'

    def signup_db():
        up.withdraw()

        global ques_e
        global quest
        global op_a_e
        global op_b_e
        global op_c_e
        global op_d_e
        global ans_e
        # string variables below used in the form
        ques_e = StringVar()
        quest = StringVar()
        op_a_e = StringVar()
        op_b_e = StringVar()
        op_c_e = StringVar()
        op_d_e = StringVar()
        ans_e = StringVar()

        database_conn()
        # checking if a field is empty, show error
        if username1.get() == "" or password1.get() == "":
            messagebox.showerror("Empty Fields", "Please enter both username and password!")
        # else
        else:
            if username1.get() == admin_username and password1.get() == admin_pass:
                messagebox.showinfo("Logged In", "Successfully Logged In")

                def quiz_data(name):
                    adminportal = Tk()
                    # designing the window for admin portal
                    adminportal.geometry('1110x600')
                    adminportal.config(bg='white')

                    treev2 = ttk.Treeview(adminportal, selectmode='browse')
                    #  ------------ Calling pack method w.r.to treeview ------------
                    treev2.place(height=370, width=1110, x=00, y=30)

                    vsb = ttk.Scrollbar(adminportal, orient="vertical", command=treev2.yview)
                    vsb.place(x=1093, y=31, height=368)
                    treev2.configure(yscrollcommand=vsb.set)

                    vsb = ttk.Scrollbar(adminportal, orient="horizontal", command=treev2.xview)
                    vsb.place(x=1, y=379, width=1092, height=20)
                    treev2.configure(xscrollcommand=vsb.set)

                    #  ------------ Defining number of columns ------------
                    treev2["columns"] = ("1", "2", "3", "4", "5", "6", "7")
                    # Defining heading
                    treev2['show'] = 'headings'
                    treev2.column("1", width=100, anchor='c')
                    treev2.column("2", width=200, anchor='c')
                    treev2.column("3", width=100, anchor='c')
                    treev2.column("4", width=100, anchor='c')
                    treev2.column("5", width=100, anchor='c')
                    treev2.column("6", width=100, anchor='c')
                    treev2.column("7", width=120, anchor='c')

                    treev2.heading("1", text="Question No")
                    treev2.heading("2", text="Question")
                    treev2.heading("3", text="Option A")
                    treev2.heading("4", text="Option B")
                    treev2.heading("5", text="Option C")
                    treev2.heading("6", text="Option D")
                    treev2.heading("7", text="Answer")

                    mydb2 = sqlite3.connect("question_bank.db")
                    mycursor2 = mydb2.cursor()

                    # insert data into treeview
                    treev2.delete(*treev2.get_children())

                    mycursor2.execute(f"""SELECT *  FROM [{name}] LIMIT 100;""")
                    data_2 = mycursor2.fetchall()
                    # ---------- INSERT ALL VALUES INTO TREEVIEW FROM DATABASE -----------
                    indexer = 1
                    for value in data_2:
                        treev2.insert("", 'end', text="L" + str(indexer),
                                      values=(value[0], value[1], value[2], value[3], value[4], value[5], value[6]))
                        indexer += 1

                    def update_ques():

                        mycursor2.execute(f"""UPDATE [{name}] SET [Question] =?, [Option A] =?, [Option B] =?,
                                                        [Option C] =?, [Option D] =?, [Answer] =?
                                        WHERE [Question No.] =?""", (
                        quest.get(), op_a_e.get(), op_b_e.get(), op_c_e.get(), op_d_e.get(), ans_e.get(), q_no_e.get()))
                        mydb2.commit()

                        adminportal.withdraw()
                        adminportal.after(1, quiz_data(name))

                    def delete_ques():

                        mycursor2.execute(f"""DELETE FROM [{name}] WHERE [Question No.] ={q_no_e.get()}""")
                        mydb2.commit()

                        adminportal.withdraw()
                        adminportal.after(1, quiz_data(name))

                    def add_question():
                        new_win = Tk()
                        new_win.resizable(0, 0)
                        new_win.title('Add Question')

                        def submit_quest():

                            if question_e.get() == '' or option_a == '' or option_b == '' or option_c == '' or option_d == '' or answer_e == '':
                                messagebox.showerror('Error', 'Please enter the values')
                            else:
                                mycursor2.execute(f""" INSERT INTO [{name}] ([Question],[Option A],[Option B],[Option C],[Option D],[Answer])
                                                    VALUES(?,?,?,?,?,?) """, (
                                question_e.get(), option_a_e.get(), option_b_e.get(), option_c_e.get(),
                                option_d_e.get(), answer_e.get()))
                                mydb2.commit()
                                new_win.withdraw()
                                adminportal.withdraw()
                                adminportal.after(1, quiz_data(name))

                        question_head = Label(new_win, text='Add a Question', font=("ARIAL", 16))
                        question_head.grid(row=0, column=0, padx=10, pady=10)

                        question = Label(new_win, text='Question', font=("ARIAL", 16))
                        question.grid(row=1, column=0, padx=10, pady=10)

                        question_e = Entry(new_win, font=("ARIAL", 16))
                        question_e.grid(row=1, column=1)

                        option_a = Label(new_win, text='Option A', font=("ARIAL", 16))
                        option_a.grid(row=2, column=0, padx=10, pady=10)

                        option_a_e = Entry(new_win, font=("ARIAL", 16))
                        option_a_e.grid(row=2, column=1)

                        option_b = Label(new_win, text='Option B', font=("ARIAL", 16))
                        option_b.grid(row=3, column=0, padx=10, pady=10)

                        option_b_e = Entry(new_win, font=("ARIAL", 16))
                        option_b_e.grid(row=3, column=1)

                        option_c = Label(new_win, text='Option C', font=("ARIAL", 16))
                        option_c.grid(row=4, column=0, padx=10, pady=10)

                        option_c_e = Entry(new_win, font=("ARIAL", 16))
                        option_c_e.grid(row=4, column=1)

                        option_d = Label(new_win, text='Option D', font=("ARIAL", 16))
                        option_d.grid(row=5, column=0, padx=10, pady=10)

                        option_d_e = Entry(new_win, font=("ARIAL", 16))
                        option_d_e.grid(row=5, column=1)

                        answer = Label(new_win, text='Answer', font=("ARIAL", 16))
                        answer.grid(row=6, column=0, padx=10, pady=10)

                        answer_e = Entry(new_win, font=("ARIAL", 16))
                        answer_e.grid(row=6, column=1, padx=20)

                        submit = Button(new_win, text='Add Question', command=submit_quest)
                        submit.config(font=("ARIAL", 12))
                        submit.grid(row=7, column=1, pady=15)

                    ad_q = Button(adminportal, text='Add Question', command=add_question)
                    ad_q.config(bg='white', font=("ARIAL", 12))
                    ad_q.place(x=30, y=420)

                    ed_q = Button(adminportal, text='Update Question', command=update_ques)
                    ed_q.config(bg='white', font=("ARIAL", 12))
                    ed_q.place(x=280, y=420)

                    de_q = Button(adminportal, text='Delete Question', command=delete_ques)
                    de_q.config(bg='white', font=("ARIAL", 12))
                    de_q.place(x=510, y=420)

                    q_no = Label(adminportal, text='Question No.', state='disabled')

                    q_no.config(bg='white', font=("ARIAL", 12))
                    q_no.place(x=30, y=480)

                    q_no_e = Entry(adminportal, width=13)
                    q_no_e.config(bg='white', font=("ARIAL", 12))
                    q_no_e.place(x=130, y=480)

                    ques = Label(adminportal, text='Question')
                    ques.config(bg='white', font=("ARIAL", 12))
                    ques.place(x=280, y=480)

                    quest = Entry(adminportal, width=13)
                    quest.config(bg='white', font=("ARIAL", 12))
                    quest.place(x=360, y=480)

                    op_a = Label(adminportal, text='Option A')
                    op_a.config(bg='white', font=("ARIAL", 12))
                    op_a.place(x=490, y=480)

                    op_a_e = Entry(adminportal, width=13)
                    op_a_e.config(bg='white', font=("ARIAL", 12))
                    op_a_e.place(x=570, y=480)

                    op_b = Label(adminportal, text='Option B')
                    op_b.config(bg='white', font=("ARIAL", 12))
                    op_b.place(x=700, y=480)

                    op_b_e = Entry(adminportal, width=13)
                    op_b_e.config(bg='white', font=("ARIAL", 12))
                    op_b_e.place(x=780, y=480)

                    op_c = Label(adminportal, text='Option C')
                    op_c.config(bg='white', font=("ARIAL", 12))
                    op_c.place(x=280, y=530)

                    op_c_e = Entry(adminportal, width=13)
                    op_c_e.config(bg='white', font=("ARIAL", 12))
                    op_c_e.place(x=360, y=530)

                    op_d = Label(adminportal, text='Option D')
                    op_d.config(bg='white', font=("ARIAL", 12))
                    op_d.place(x=490, y=530)

                    op_d_e = Entry(adminportal, width=13)
                    op_d_e.config(bg='white', font=("ARIAL", 12))
                    op_d_e.place(x=570, y=530)

                    ans = Label(adminportal, text='Answer')
                    ans.config(bg='white', font=("ARIAL", 12))
                    ans.place(x=707, y=530)

                    ans_e = Entry(adminportal, width=13)
                    ans_e.config(bg='white', font=("ARIAL", 12))
                    ans_e.place(x=780, y=530)

                    def getrow(event):
                        q_no_e['state'] = 'normal'
                        q_no_e.delete(0, END)
                        q_no_e['state'] = 'disabled'
                        quest.delete(0, END)
                        op_a_e.delete(0, END)
                        op_b_e.delete(0, END)
                        op_c_e.delete(0, END)
                        op_c_e.delete(0, END)
                        op_d_e.delete(0, END)
                        ans_e.delete(0, END)

                        q_no_e['state'] = 'normal'
                        item = treev2.item(treev2.focus())
                        q_no_e.insert(END, item['values'][0])
                        q_no_e['state'] = 'disabled'
                        quest.insert(END, item['values'][1])
                        op_a_e.insert(END, item['values'][2])
                        op_b_e.insert(END, item['values'][3])
                        op_c_e.insert(END, item['values'][4])
                        op_d_e.insert(END, item['values'][5])
                        ans_e.insert(END, item['values'][6])

                    treev2.bind('<Double-Button-1>', getrow)
                    adminportal.mainloop()

                def view():
                    root2 = Toplevel()
                    root2.title('Quiz Subject')
                    root2.resizable(0, 0)

                    lbl = Label(root2, text='Pick a Subject', font=("HELVETICA", 15))
                    lbl.grid(row=0, column=0, columnspan=2, padx=40, pady=20)

                    con2 = sqlite3.connect("question_bank.db")
                    cursor2 = con2.cursor()

                    cursor2.execute("SELECT name FROM sqlite_master WHERE type='table';")

                    con2.commit()
                    # print()
                    aa = cursor2.fetchall()
                    bb = []
                    cc = []
                    for i in aa:
                        cc.append(list(i))

                    data2 = cc

                    for i in range(len(data2)):
                        data2[i][0] = str(data2[i][0])
                    # print(data2)
                    # for j in data2:
                    #     print(j[0].title())

                    x = 0

                    for i in range(len(data2)):
                        ll = Label(root2, text=f'{data2[i][0].title()}', font=("HELVETICA", 15))
                        ll.grid(row=x, column=0, columnspan=2, padx=40, pady=20)
                        x += 1

                    y = 0
                    for j in range(len(data2)):
                        lla = Button(root2, text='Edit', width=5, font=("HELVETICA", 14),
                                     command=lambda name=f'{data2[j][0]}': quiz_data(name))
                        lla.grid(row=y, column=3)
                        y += 1

                    def del_tab(name):
                        if messagebox.askyesno("Info", "Are you sure you want to delete this subject?"):
                            query = f"""DROP TABLE [{name}];"""
                            root2.withdraw()
                            con2.execute(query)

                            root2.after(1000, view())
                            root2.deiconify()

                    z = 0
                    for k in range(len(data2)):
                        llal = Button(root2, text='Delete', width=5, font=("HELVETICA", 14),
                                      command=lambda name=f'{data2[k][0].title()}': del_tab(name))
                        llal.grid(row=z, column=4, padx=50)
                        z += 1

                    def add_sub():
                        root2.withdraw()

                        def proceed():
                            query = f"""CREATE TABLE "{quiz.get()}" (
                                                    "Question No."	INTEGER,
                                                    "Question"	TEXT,
                                                    "Option A"	TEXT,
                                                    "Option B"	TEXT,
                                                    "Option C"	TEXT,
                                                    "Option D"	TEXT,
                                                    "Answer"	TEXT,
                                                    PRIMARY KEY("Question No.")
                    );"""
                            cursor2.execute(query)

                            add_quiz.withdraw()
                            # root2.update_idletasks()
                            root2.after(1000, view())
                            root2.deiconify()

                        add_quiz = Tk()
                        # designing the window for admin portal
                        add_quiz.geometry('410x300')
                        # add_quiz.config(bg='white')

                        quiz_label = Label(add_quiz, text="Add a Subject", font=("HELVETICA", 15))
                        # quiz_label.config(bg='white')
                        quiz_label.place(x=145, y=125)

                        quiz = Entry(add_quiz, width=30)
                        quiz.config(font=("ARIAL", 12))
                        quiz.place(x=70, y=175)

                        quiz_btn = Button(add_quiz, text='Proceed', width=10, font=("HELVETICA", 14),
                                          command=lambda: proceed())
                        quiz_btn.place(x=145, y=220)

                        add_quiz.mainloop()

                    llala = Button(root2, text='Add a Subject', width=20, font=("HELVETICA", 14),
                                   command=lambda: add_sub())
                    llala.grid(row=z + 2, column=1, pady=20)

                    root2.mainloop()

                view()
                quiz_data()


            # else inserting into the database
            else:
                messagebox.showerror("Error", "Incorrect username or password!")
                admin_log()

    # signup window gui
    log.withdraw()
    up = Toplevel()
    up.title('Sign Up')
    up.resizable(0, 0)

    # headings along with field names and entries and button that user will enter its info to be added into the database

    head = Label(up, text='PROJECT QUIZ', font=('HELVETICA', 21, 'bold'))
    head.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

    u_lbl = Label(up, text='Username', font=("ARIAL", 12))
    u_lbl.grid(row=3, column=0, padx=10, pady=10)

    username1 = Entry(up, width=20, font=("ARIAL", 12))
    username1.grid(row=3, column=1, pady=10, padx=(0, 40))

    pa_lbl = Label(up, text='Password', font=("ARIAL", 12))
    pa_lbl.grid(row=4, column=0, padx=10, pady=10)

    password1 = Entry(up, width=20, show='*', font=("ARIAL", 12))
    password1.grid(row=4, column=1, pady=10, padx=(0, 40))

    # button to call signup function to isert new user in database
    signup_btn = Button(up, text='Login', font=('HELVETICA', 16), width=12, bd=4, relief=RAISED, command=signup_db)
    signup_btn.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    dont = Label(up, text="Not an admin?", font=("HELVETICA", 12))
    dont.grid(row=6, column=0, columnspan=2, padx=(0, 100))

    # will go back to login window
    login_btn = Button(up, text='Login as user', bd=3, relief=RAISED, width=10, font=("HELVETICA", 12),
                       command=log_back)
    login_btn.grid(row=6, column=1, padx=(90, 0), pady=10)

    up.mainloop()


# signup function
def signup():
    def log_back():
        up.destroy()
        log.deiconify()
        username.delete(0, END)
        password.delete(0, END)

    def signup_db():

        database_conn()
        # checking if a field is empty, show error
        if fname.get() == "" or sname.get() == "" or username1.get() == "" or password1.get() == "":
            messagebox.showerror("Empty Fields", "Please enter both userneame and password!")
        # else
        else:
            # check if username already exists in the databse
            cursor.execute("SELECT * FROM `user` WHERE `username` = ?", (username1.get(),))
            # if yes then show error
            if cursor.fetchone() is not None:
                messagebox.showerror("User Exists", "A User with this Username Already exists.\nTry new username!")
                username.set("")
            # else inserting into the database
            else:
                cursor.execute("INSERT INTO `user` (firstname, surname, username, password) VALUES(?, ?, ?, ?)",
                               (fname.get(), sname.get(), username1.get(), password1.get()))
                conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo('Successful!', 'You are successfully registered!')
        up.destroy()
        log.deiconify()

    # signup window gui
    log.withdraw()
    up = Toplevel()
    up.title('Sign Up')
    up.resizable(0, 0)

    # headings along with field names and entries and button that user will enter its info to be added into the database

    head = Label(up, text='PROJECT QUIZ', font=('HELVETICA', 21, 'bold'))
    head.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

    f_lbl = Label(up, text='First Name', font=("HELVETICA", 12))
    f_lbl.grid(row=1, column=0, padx=10, pady=10)

    fname = Entry(up, width=20, font=("ARIAL", 12))
    fname.grid(row=1, column=1, pady=10, padx=(0, 40))

    s_lbl = Label(up, text='Surname', font=("HELVETICA", 12))
    s_lbl.grid(row=2, column=0, padx=10, pady=10)

    sname = Entry(up, width=20, font=("ARIAL", 12))
    sname.grid(row=2, column=1, pady=10, padx=(0, 40))

    u_lbl = Label(up, text='Username', font=("ARIAL", 12))
    u_lbl.grid(row=3, column=0, padx=10, pady=10)

    username1 = Entry(up, width=20, font=("ARIAL", 12))
    username1.grid(row=3, column=1, pady=10, padx=(0, 40))

    pa_lbl = Label(up, text='Password', font=("ARIAL", 12))
    pa_lbl.grid(row=4, column=0, padx=10, pady=10)

    password1 = Entry(up, width=20, show='*', font=("ARIAL", 12))
    password1.grid(row=4, column=1, pady=10, padx=(0, 40))

    # button to call signup function to isert new user in database
    signup_btn = Button(up, text='Sign Up', font=('HELVETICA', 16), width=12, bd=4, relief=RAISED, command=signup_db)
    signup_btn.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    dont = Label(up, text="Already have an account?", font=("HELVETICA", 12))
    dont.grid(row=6, column=0, columnspan=2, padx=(0, 100))

    # will go back to login window
    login_btn = Button(up, text='Login', bd=3, relief=RAISED, width=10, font=("HELVETICA", 12), command=log_back)
    login_btn.grid(row=6, column=1, padx=(90, 0), pady=10)

    up.mainloop()


# home window function
def home():
    # logout function
    def logout():
        home_w.destroy()
        log.deiconify()
        username.delete(0, END)
        password.delete(0, END)

    # grade book display function
    def grade():
        # grade book GUI
        grade = Toplevel()
        grade.title('Grade Book')
        grade.resizable(0, 0)

        heading = Label(grade, text=username.get().upper() + ' SCORES', font=("HELVETICA", 20))
        heading.pack(fill=BOTH, expand=YES, pady=10)

        # tree view that shows the scores of each quiz of only the current logged in student
        grade_score = ttk.Treeview(grade, columns=('Quiz Name', 'Score', 'Percentage'), show="headings")
        grade_score.heading('#1', text='Quiz Name', anchor=CENTER)
        grade_score.heading('#2', text='Score', anchor=CENTER)
        grade_score.heading('#3', text='Percentage', anchor=CENTER)

        # opening the user_score.csv file
        with open('user_score.csv') as f:
            # reading it line by line
            reader = csv.DictReader(f, delimiter=',')
            for row in reader:
                name = row['Student_Name']
                # read only the line which has the username of current user
                if username.get() == name:
                    head = reader.fieldnames
                    # looping to read quiz names and scores to display
                    for i in range(1, len(head)):
                        q_score = row[head[i]]
                        # checking if a score of a quiz is not empty means there is a score for that quiz
                        if q_score != '':
                            # calculating percentage
                            percent = (int(q_score) / 10) * 100
                            # 3 displaying the quiz name, score and percentage
                            grade_score.insert("", END, values=(head[i], q_score, str(percent) + '%'))
                        else:
                            # 3 displaying the quiz name, score and percentage
                            grade_score.insert("", END, values=(head[i], 0, '0%'))

        # scrollbar for the treeview
        scroll = Scrollbar(grade, command=grade_score.yview, orient='vertical')
        grade_score.configure(yscrollcommand=scroll.set)
        scroll.pack(side=RIGHT, fill=Y)
        grade_score.pack(fill=BOTH, expand=YES, pady=(0, 20), padx=10)

    # function to select the subject
    def main():

        # previous window function by pressing menu
        def back():
            root.destroy()
            home_w.deiconify()

        # function that allows to select the quiz number
        def show_quiz(name):

            # previous window function by pressing menu
            def back2():
                root2.destroy()
                home_w.deiconify()

            # quiz show function
            def start_quiz(f, quiz_num, head):
                # print(name)

                root2.withdraw()

                global counter
                counter = 0
                data = []

                # checking for correct answer function
                def check(b):
                    # getting global variables
                    global counter, score, all_files

                    # getting the text of the button that was pressed
                    answer = b.cget('text')
                    # print(answer)

                    # getting the correct answer number from the data list or from csv
                    correct_ans = data[counter][6][1]

                    # getting the correct answer from that number above
                    correct = data[counter][int(correct_ans) + 1]

                    # checking if user selected the correct answer
                    if str(correct) == str(answer):
                        # score added
                        score += 1
                        print('Your answer is correct')
                        cor_wron.append(f'Your answer is correct.')
                    # else wrong answer
                    else:
                        cor_wron.append(f'Your answer is wrong. The Correct answer is {str(correct)}')
                        print('Your answer is wrong')

                    try:
                        # if counter is less than 10, then it will update the questions and answers on gui, else if 10 questions are done, then window will close
                        if counter < 10:
                            counter += 1
                            num['text'] = 'Q' + data[counter][0]
                            quest['text'] = data[counter][1]
                            option1.configure(text=data[counter][2])
                            option2.configure(text=data[counter][3])
                            option3.configure(text=data[counter][4])
                            option4.configure(text=data[counter][5])

                    except:
                        # adding the score in the dictionary with the quiz name
                        try:
                            nn = str(name[0]).upper() + str(name[1]).upper() + str(name[2]).upper() + str(
                                name[3]).upper()
                            quiz_score[nn] = score
                        except:
                            nn = str(name[0]).upper() + str(name[1]).upper() + str(name[2]).upper()
                            quiz_score[nn] = score
                        # destroying the window
                        root3.destroy()
                        root2.deiconify()
                        # setting score to 0 again
                        score = 0

                        result = Toplevel()
                        result.title('Quiz')
                        result.resizable(0, 0)
                        # screen width and height

                        f_score = Label(result, text=f'Your Quiz Score is: {quiz_score[nn]} out of 5',
                                        font=("HELVETICA", 14, 'bold', 'underline'))
                        f_score.grid(row=1, column=1, padx=40, pady=20)

                        for i in range(len(cor_wron)):
                            ri_wro_label = Label(result, text=f'{i + 1}. {cor_wron[i]}',
                                                 font=("HELVETICA", 14))
                            ri_wro_label.grid(row=2 + i, column=1, padx=40, pady=20)

                        f = open('user_score.txt', 'a', encoding='UTF8', newline='')

                        # write in file

                        f.write(f'\n{username.get()}, {name.title()}, {quiz_score[nn]}, 5')


                        # close the file
                        f.close()

                        cor_wron.clear()

                        result.mainloop()

                        # converting dict to list
                        lst = list(quiz_score.items())[-1]
                        quiz_score.clear()

                import sqlite3

                conn = sqlite3.connect('question_bank.db')
                cursor = conn.cursor()

                cursor.execute(f"Select * from [{name.lower()}]")
                conn.commit()
                # print()
                a = cursor.fetchall()
                b = []
                c = []
                for i in a:
                    c.append(list(i))

                data = c

                for i in range(len(data)):
                    data[i][0] = str(data[i][0])
                # print(data)

                import random

                random.shuffle(data)

                if len(data) >= 5:
                    data = random.sample(data, 5)

                # print(data)

                # Quiz Window GUI that shows questions and answers to select
                root3 = Toplevel()
                root3.title('Quiz')
                root3.resizable(0, 0)
                # screen width and height
                h = root3.winfo_screenheight()
                w = root3.winfo_screenwidth()
                root3.geometry('{}x{}'.format(int(w) - 100, int(h / 2) - 50))

                answer = StringVar()

                # getting the question number, question, and 4 answers from the data list to print on GUI
                num = Label(root3, text='Q' + data[counter][0], font=("HELVETICA", 14))
                num.grid(row=0, column=0, padx=(0, 10), pady=10)

                quest = Label(root3, text=data[counter][1], font=("HELVETICA", 14))
                quest.grid(row=0, column=1, columnspan=2, padx=10, pady=10)

                # 4 buttons has 4 answers to select the right one. All different colors
                option1 = Button(root3, text=data[counter][2], bg='red', width=30, bd=3, relief=RAISED,
                                 font=("HELVETICA", 12), wraplength=250, justify=CENTER)
                option1.configure(command=lambda b=option1: check(b))
                option1.grid(row=1, column=1, padx=10, pady=(10, 5))

                option2 = Button(root3, text=data[counter][3], bg='lightblue', width=30, bd=3, relief=RAISED,
                                 font=("HELVETICA", 12), wraplength=250, justify=CENTER)
                option2.configure(command=lambda b=option2: check(b))
                option2.grid(row=1, column=2, padx=10, pady=(10, 5))

                option3 = Button(root3, text=data[counter][4], bg='orange', width=30, bd=3, relief=RAISED,
                                 font=("HELVETICA", 12), wraplength=250, justify=CENTER)
                option3.configure(command=lambda b=option3: check(b))
                option3.grid(row=2, column=1, padx=10, pady=(10, 5))

                option4 = Button(root3, text=data[counter][5], bg='pink', width=30, bd=3, relief=RAISED,
                                 font=("HELVETICA", 12), wraplength=250, justify=CENTER)
                option4.configure(command=lambda b=option4: check(b))
                option4.grid(row=2, column=2, padx=10, pady=(10, 5))

                root3.columnconfigure(3, weight=1)
                root3.rowconfigure(3, weight=1)
                root3.grid_columnconfigure(3, weight=1)
                root3.grid_rowconfigure(3, weight=1)

                root3.mainloop()

            # Quiz Window GUI.
            root.withdraw()
            root2 = Toplevel()
            root2.title('Quiz Select')
            root2.resizable(0, 0)

            lbl1 = Label(root2, text=name.upper(), font=("HELVETICA", 14))
            lbl1.grid(row=0, column=0, columnspan=2, padx=30, pady=20)

            select = Label(root2, text='Select a Quiz', font=("HELVETICA", 14))
            select.grid(row=1, column=0, padx=10, pady=5)

            global all_files
            all_files = [f for f in os.listdir('.') if '.db' in f]

            head = ['Student_Name']
            try:
                head.append(name[0].upper() + name[1].upper() + name[2].upper() + name[3].upper())
            except:
                head.append(name[0].upper() + name[1].upper() + name[2].upper())
            num_files1 = [f for f in os.listdir('.') if name.lower() in f]

            import sqlite3

            conn = sqlite3.connect('question_bank.db')
            cursor = conn.cursor()

            cursor.execute(f"Select * from [{name.lower()}]")
            conn.commit()
            a = cursor.fetchall()
            b = []
            c = []
            for i in a:
                c.append(list(i))

            data = c

            for i in range(len(data)):
                data[i][0] = str(data[i][0])

            # creating button based on the number of files found for that subject
            r = 1

            # for i in range(1):
            btn = Button(root2, text='Quiz', width=10, bd=3, relief=RAISED, font=("HELVETICA", 14),
                         command=lambda head='a', quiz_num=1, f=1: start_quiz(f, quiz_num, head))
            btn.grid(row=r, column=1, pady=5, padx=10)
            r += 1

            menu = Button(root2, text='Menu', width=5, font=("HELVETICA", 14), command=back2)
            menu.grid(row=r, column=0, padx=(0, 90), pady=(15, 0))

            root2.mainloop()


        # quiz window that will let user select the subject for quiz
        home_w.withdraw()
        root = Toplevel()
        root.title('Quiz Subject')
        root.resizable(0, 0)

        lbl = Label(root, text='Pick a Subject', font=("HELVETICA", 15))
        lbl.grid(row=0, column=0, columnspan=2, padx=40, pady=20)

        con3 = sqlite3.connect("question_bank.db")
        cursor3 = con3.cursor()

        cursor3.execute("SELECT name FROM sqlite_master WHERE type='table';")

        con3.commit()
        # print()
        aaa = cursor3.fetchall()
        bbb = []
        ccc = []
        for i in aaa:
            ccc.append(list(i))

        data2 = ccc

        for i in range(len(data2)):
            data2[i][0] = str(data2[i][0])

        # print(data2)

        new_row = 1
        for i in range(len(data2)):
            btn = Button(root, text=f'{data2[i][0].title()}', width=35, font=("HELVETICA", 14),
                         command=lambda name=f'{data2[i][0].title()}': show_quiz(name))
            btn.grid(row=new_row, column=0, columnspan=2, padx=40, pady=5)
            new_row += 1

        menu = Button(root, text='Menu', width=8, font=("HELVETICA", 14), command=back)
        menu.grid(row=new_row, column=0, padx=(0, 150), pady=(15, 0))

        root.mainloop()


    # home window GUI to let user select play or show grade book
    log.withdraw()
    home_w = Toplevel()
    home_w.resizable(0, 0)
    home_w.title('Home Page')

    logout_btn = Button(home_w, text='Logout', font=("ARIAL", 15), bd=3, relief=RAISED, command=logout)
    logout_btn.grid(row=0, column=1, padx=(30, 0), pady=(0, 10))

    head = Label(home_w, text='WELCOME TO\nPROJECT QUIZ', font=("HELVETICA", 20, 'bold'))
    head.grid(row=1, column=0, columnspan=2, padx=20, pady=20)

    # grade = Button(home_w,text='Grade Book',font=("ARIAL",15),bd=3,relief=RAISED,command=grade)
    # grade.grid(row=2,column=0,padx=(30,10),pady=(10,30))

    play_btn = Button(home_w, text='Play', font=("ARIAL", 15), bd=3, relief=RAISED, command=main)
    play_btn.grid(row=2, column=0, padx=(10, 30), pady=(10, 30))

    home_w.mainloop()


# login window GUI that lets user enter username and password
log = Tk()
log.resizable(0, 0)
log.title('Login Page')

heading = Label(log, text='PROJECT QUIZ', font=("HELVETICA", 20, 'bold'))
heading.grid(row=0, column=0, padx=90, pady=20)

username_lbl = Label(log, text='Username', font=("HELVETICA", 14))
username_lbl.grid(row=1, column=0, padx=45, pady=10)

username = Entry(log, width=20, font=("ARIAL", 12))
username.grid(row=2, column=0, padx=45, pady=(0, 10))

password_lbl = Label(log, text='Password', font=("HELVETICA", 14))
password_lbl.grid(row=3, column=0, padx=45, pady=10)

password = Entry(log, width=20, show="*", font=("ARIAL", 12))
password.grid(row=4, column=0, padx=45, pady=(0, 10))

# will go to login function if clicked
login_btn = Button(log, text='Login', bd=3, relief=RAISED, width=10, font=("HELVETICA", 14), command=login)
login_btn.grid(row=5, column=0, padx=10, pady=(20, 20))

dont = Label(log, text="Don't have an account?", font=("HELVETICA", 12))
dont.grid(row=6, column=0, padx=(0, 130))

# will go to signup function if clicked
signup_btn = Button(log, text='Signup', bd=3, relief=RAISED, width=10, font=("HELVETICA", 12), command=signup)
signup_btn.grid(row=6, column=0, padx=(150, 0), pady=10)

admin = Label(log, text="Are you an Admin?", font=("HELVETICA", 12))
admin.grid(row=7, column=0, padx=(0, 130))

admin_btn = Button(log, text='Admin Login', bd=3, relief=RAISED, width=10, font=("HELVETICA", 12), command=admin_log)
admin_btn.grid(row=7, column=0, padx=(150, 0), pady=10)

log.mainloop()
