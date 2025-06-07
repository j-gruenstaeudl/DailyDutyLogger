from customtkinter import *

app = CTk()
app.geometry("500x400")


set_appearance_mode("light")
count = 0

def btn_clicked():
    print(f"button clicked: {entry.get()}")
    global count
    count += 1
    label.configure(text=f"btn clicked {count} times")

frame = CTkFrame(master=app, fg_color="#8D6F3A", border_color="#FFCC70", border_width=2)
frame.pack(expand=True)
    
label = CTkLabel(master=frame, text="btn clicked 0 times")

entry = CTkEntry(master=frame, placeholder_text="Type something...", width=300)


btn = CTkButton(master=app, text="click me", corner_radius=32, command=btn_clicked)
btn.place(relx=0.5, rely=0.5, anchor="center")

label.pack(anchor="s", expand=True, pady=10)
entry.pack(anchor="s", pady=10, expand=True)
btn.pack(anchor="n", expand=True)


app.mainloop()