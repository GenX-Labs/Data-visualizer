from tkinter.ttk import Combobox, Treeview, Style
import pandas as pd
from tkinter import *
import tkinter.font as tkfont
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter.messagebox
from tkcalendar import DateEntry
from datetime import datetime

root = Tk()
root.title("Covid Data Visualizer (MAlAYSIA EDITION)")
covid_data = pd.read_csv("covid_cases.csv")
pd.set_option('display.max_rows', None)
root.geometry('1400x650')
root.resizable(False, False)

my_font = tkfont.Font(family="Microsoft JhengHei", size=12, weight="normal")

left_frame = Frame(root, width=300, height=650, borderwidth=1, relief="solid")
left_frame.place(x=0, y=0)
left_frame.pack_propagate(False)

right_frame = Frame(root, width=400, height=600, borderwidth=1, relief="solid")
right_frame.place( x=300, y=0)
right_frame.pack_propagate(False)

graph_frame = Frame(root, width=700, height=650, borderwidth=1, relief="solid")
graph_frame.place(x=700, y=0)
graph_frame.pack_propagate(False)

summary_frame = Frame(root, width=400, height=150, borderwidth=1, relief="solid")
summary_frame.place(x=300, y=500)
summary_frame.pack_propagate(False)

input_title = Label(left_frame, text="Choose a state:", font=my_font)
input_title.pack()

states = ["Johor", "Kelantan", "Melaka", "Negeri Sembilan", "Kedah", "Pahang",
          "Perak", "Perlis", "Pulau Pinang", "Sabah", "Sarawak", "Selangor", "Terengganu",
          "W.P. Kuala Lumpur", "W.P. Labuan", "W.P. Putrajaya"]
state_value = Combobox(left_frame, values=states)
state_value.pack(pady=(0, 20))
state_value.set("Malaysia")

# date settings
min_date = datetime(2020, 1, 25)
max_date = datetime(2025, 5, 31)

date_input1 = DateEntry(left_frame, mindate=min_date, maxdate=max_date)
date_input2 = DateEntry(left_frame, mindate=min_date, maxdate=max_date)

start_date = Label(left_frame, text="Select the Starting date:", font=my_font)
end_date = Label(left_frame, text="Select the ending date:", font=my_font)

start_date.pack()
date_input1.pack(pady=(0, 20))
end_date.pack()
date_input2.pack(pady=(0, 20))

y_data_qn = Label(left_frame, text="Choose Cases Type:", font=my_font)
y_data_qn.pack()

# determining the y data
# radio button for y_data type
y_choice = StringVar()
y_choice.set("new_cases")

new_cases_rb = Radiobutton(left_frame, text="new cases", variable=y_choice, value="new_cases")
recovered_cases_rb = Radiobutton(left_frame, text="recovered cases", variable=y_choice, value="recovered_cases")
active_cases_rb = Radiobutton(left_frame, text="active cases", variable=y_choice, value="active_cases")

new_cases_rb.pack()
recovered_cases_rb.pack()
active_cases_rb.pack()


# -----------Global Variables--------------------

def given_data():
    tree = Treeview(right_frame)
    tree.pack(ipady=224, ipadx=165)

    vsb = Scrollbar(tree, orient="vertical", command=tree.yview)
    vsb.pack(side='right', fill='y')
    tree.configure(yscrollcommand=vsb.set)

    # Add horizontal scrollbar
    hsb = Scrollbar(tree, orient="horizontal", command=tree.xview)
    hsb.pack(side='bottom', fill='x')
    tree.configure(xscrollcommand=hsb.set)

    # Add vertical scrollbar

    # set columns
    tree['columns'] = list(covid_data.columns)
    tree['show'] = 'headings'

    # style
    style = Style()
    style.configure("Treeview.Heading", font=('Arial', 12, 'bold'), background="gray")

    for col in covid_data.columns:
        tree.heading(col, text=col)
        tree.column(col, anchor='center')

    for index, row in covid_data.iterrows():
        (tree.insert("", "end", values=list(row)))


    tree.column('date', width=66)
    tree.column('state', width=100)
    tree.column('cases_new', width=100)
    tree.column('cases_import', width=120)
    tree.column('cases_recovered', width=150)
    tree.column('cases_active', width=120)
    tree.column('cases_cluster', width=130)

    # display summary
    country = "Malaysia"
    new_cases = covid_data.cases_new[(covid_data['state'] == country)]
    recovered_cases = covid_data.cases_recovered[(covid_data['state'] == country)]

    summary_title = Label(summary_frame, text="SUMMARY", font="15")
    summary_title.pack()

    total_cases = str(new_cases.sum())
    total_recovered_cases = str(recovered_cases.sum())

    total_c_text = "Total cases: " + total_cases
    total_r_c_text = "Total recovered cases: " + total_recovered_cases

    t_c = Label(summary_frame, text=total_c_text)
    t_r_c = Label(summary_frame, text=total_r_c_text)

    t_c.pack()
    t_r_c.pack()

    # plotting graph
    fig = Figure(figsize=(7, 6.5), dpi=100)
    ax = fig.add_subplot(111)

    covid_data['date'] = pd.to_datetime(covid_data['date'], format='%d/%m/%Y')

    # date,state,cases_new,cases_import,cases_recovered,cases_active,cases_cluster

    X_data = covid_data.date[(covid_data['state'] == country)]
    Y_data1 = covid_data.cases_new[(covid_data['state'] == country)]
    Y_data2 = covid_data.cases_active[(covid_data['state'] == country)]
    Y_data3 = covid_data.cases_recovered[(covid_data['state'] == country)]

    ax.plot(X_data, Y_data1, label="new cases")
    ax.plot(X_data, Y_data2, label="active cases")
    ax.plot(X_data, Y_data3, label="recovered cases")
    ax.set_title("Covid Data")
    ax.set_xlabel("Date")

    # dashboard
    ax.legend()

    # rotation
    ax.tick_params(axis='x', labelrotation=45)

    # display graph into the GUI
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()


# the whole process runs
given_data()

def user_data_function(specific_data):
    right_frame.pack_propagate(False)
    tree = Treeview(right_frame)
    tree.pack(ipady=224, ipadx=165)

    # Add vertical scrollbar
    vsb = Scrollbar(tree, orient="vertical", command=tree.yview)
    vsb.pack(side='right', fill='y')
    tree.configure(yscrollcommand=vsb.set)

    # Add horizontal scrollbar
    hsb = Scrollbar(tree, orient="horizontal", command=tree.xview)
    hsb.pack(side='bottom', fill='x')
    tree.configure(xscrollcommand=hsb.set)

    # set columns
    tree['columns'] = list(specific_data.columns)
    tree['show'] = 'headings'

    # style
    style = Style()
    style.configure("Treeview.Heading", font=('Arial', 12, 'bold'), background="gray")

    for col in specific_data.columns:
        tree.heading(col, text=col)
        tree.column(col, anchor='center')

    for index, row in specific_data.iterrows():
        (tree.insert("", "end", values=list(row)))

    tree.column('date', width=66)
    tree.column('state', width=100)
    tree.column('cases_new', width=100)
    tree.column('cases_import', width=120)
    tree.column('cases_recovered', width=150)
    tree.column('cases_active', width=120)
    tree.column('cases_cluster', width=130)

def data_selection():
    state_input = state_value.get()

    # date button function
    format_date1 = date_input1.get_date()
    format_date2 = date_input2.get_date()

    starting_date = format_date1.strftime('%d/%m/%Y')
    ending_date = format_date2.strftime('%d/%m/%Y')

    if format_date1 >= format_date2:
        tkinter.messagebox.showinfo("Error message", "The ending date is lower than starting date")
        right_frame.pack_propagate(False)
        given_data()

    else:

        covid_data['date'] = pd.to_datetime(covid_data['date'], format='%d/%m/%Y')
        specific_data = covid_data[(covid_data['date'] >= starting_date) & (covid_data['date'] <= ending_date)
                                   & (covid_data['state'] == state_input)]

        # display the data
        user_data_function(specific_data)

        y_information = y_choice.get()

        X_data = covid_data.date[(covid_data['date'] >= starting_date) & (covid_data['date'] <= ending_date) &
                                 (covid_data['state'] == state_input)]

        Y_data =""
        if y_information == "new_cases":
            Y_data = covid_data.cases_new[
                (covid_data['date'] >= starting_date) & (covid_data['date'] <= ending_date)
                & (covid_data['state'] == state_input)]

        elif y_information == "recovered_cases":
            Y_data = covid_data.cases_recovered[
                (covid_data['date'] >= starting_date) & (covid_data['date'] <= ending_date)
                & (covid_data['state'] == state_input)]

        elif y_information == "active_cases":
            Y_data = covid_data.cases_active[
                (covid_data['date'] >= starting_date) & (covid_data['date'] <= ending_date)
                & (covid_data['state'] == state_input)]

        # summary
        new_cases = covid_data.cases_new[(covid_data['date'] >= starting_date) & (covid_data['date'] <= ending_date)
                                         & (covid_data['state'] == state_input)]
        recovered_cases = covid_data.cases_recovered[
            (covid_data['date'] >= starting_date) & (covid_data['date'] <= ending_date)
            & (covid_data['state'] == state_input)]



        # display summary
        summary_title = Label(summary_frame, text="SUMMARY", font="15")
        summary_title.pack()

        total_cases = str(new_cases.sum())
        total_recovered_cases = str(recovered_cases.sum())

        total_c_text = "Total cases: " + total_cases
        total_r_c_text = "Total recovered cases: " + total_recovered_cases

        t_c = Label(summary_frame, text=total_c_text)
        t_r_c = Label(summary_frame, text=total_r_c_text)

        t_c.pack()
        t_r_c.pack()

        fig = Figure(figsize=(7, 6.5), dpi=100)
        ax = fig.add_subplot(111)

        ax.plot(X_data, Y_data)
        ax.set_title("Covid Data")
        ax.set_ylabel(y_information)
        ax.set_xlabel("Date")

        # rotation
        ax.tick_params(axis='x', labelrotation=45)

        # display graph into the GUI
        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()


def clear_frame():
    for widget in right_frame.winfo_children():
        widget.destroy()

    for widget in summary_frame.winfo_children():
        widget.destroy()

    for widget in graph_frame.winfo_children():
        widget.destroy()


def all_process():
    clear_frame()
    data_selection()
#-------------------------------------------------------------------------------


# confirm button
submit_btn = Button(left_frame, text="Filter", command=all_process)
submit_btn.pack()

root.mainloop()

