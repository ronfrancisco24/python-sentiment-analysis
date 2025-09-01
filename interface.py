from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext
from bot import Cohere
from PIL import Image,ImageTk


# Objects

root = Tk()
bot = Cohere()

# Color Themes
style = ttk.Style()
root.call("source", "azure.tcl")
root.call("set_theme", "light")

# Methods
        
def change_theme():
    if root.tk.call("ttk::style", "theme", "use") == "azure-dark":
        root.tk.call("set_theme", "light")
        canvas.delete("all")  
        original_img = Image.open("images/light-mode.png")
        resized_img = original_img.resize((180, 180), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(resized_img)
        canvas.create_image(100, 40, image=img)
        canvas.image = img   
    else:
        # Set dark theme
        root.tk.call("set_theme", "dark")
        canvas.delete("all")  # Clear the canvas
        original_img = Image.open("images/dark-mode.png")
        resized_img = original_img.resize((180, 180), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(resized_img)
        canvas.create_image(100, 40, image=img)
        canvas.image = img   
        
        
def analyze_text():
    user_prompt = text_entry.get("1.0", "end-1c")
    analyzing_animation(step=0)
    bot.chat(user_prompt)
    bot.confidence_score(bot.emotion)
    
    
def analyzing_animation(step=0):
    global advice_string
    advice_text.config(state='normal')
    advice_text.delete('1.0', 'end')
    dots = '.' * (step % 4)
    advice_string = f'Analyzing{dots}'
    advice_text.insert('1.0', advice_string)
    if step < 4:
        root.after(300, analyzing_animation, step+1)   
    elif step == 4:
        display_advice()
    
    
def display_advice():
    global advice_string
    advice_string = f'{bot.advice}'
    advice_text.delete('1.0', 'end')
    root.after(2000, edit_details)
    
def edit_details():
    advice_text.delete('1.0', 'end')
    advice_text.insert('1.0', advice_string)
    advice_text.config(state='disabled')
    sentiment_text.config(text=f'{bot.emotion}')
    confidence_text.config(text=f'{bot.score}')
    
def reset():
    advice_text.delete('1.0', 'end')
    sentiment_text.config(text='')
    confidence_text.config(text='')
        

# UI

root.title('Sentiment Analyze')
root.config(padx=100, pady=50)
root.geometry('500x600')
root.resizable(width=False, height=False)

main_frame = ttk.Frame(root)
main_frame.pack()

title_frame = ttk.Frame(main_frame)
title_frame.grid(column=1, row=1, columnspan=2, pady=5)

canvas = Canvas(title_frame, width=200, height=80)
original_img = Image.open("images/light-mode.png")
resized_img = original_img.resize((180, 180), Image.Resampling.LANCZOS)  # Specify desired width, height
img = ImageTk.PhotoImage(resized_img)
canvas.create_image(100, 40, image=img)
canvas.pack()

themes_button = ttk.Button(title_frame, text='Change Theme', command=change_theme)
themes_button.pack(pady=10)

enter_label = ttk.Label(main_frame, text='Enter text', font=('Arial', 11, 'bold'))
enter_label.grid(column=1, row=2, sticky='ew')

text_entry = Text(main_frame, width=20, height=4)
text_entry.grid(column=1, row=3, columnspan=2, sticky='ew', pady=15)
text_entry.focus()

analyze_button = ttk.Button(main_frame, text='Analyze', command=analyze_text)
analyze_button.grid(column=1, row=4, sticky='ew', padx=10)

reset_button = ttk.Button(main_frame, text='Reset', command=reset)
reset_button.grid(column=2, row=4, sticky='ew', pady=10)

sentiment_frame = ttk.Frame(main_frame, padding=(10, 5))
sentiment_frame.grid(column=1, row=5, sticky='ew', columnspan=2)

sentiment_text = ttk.Label(sentiment_frame, text='')
sentiment_text.pack(side='right')

sentiment_label = ttk.Label(sentiment_frame, text='Sentiment:', font=('Arial', 11, 'bold'))
sentiment_label.pack(side='right')

confidence_label = ttk.Label(sentiment_frame, text='Confidence:', font=('Arial', 11, 'bold'))
confidence_label.pack(side='left')

confidence_text = ttk.Label(sentiment_frame, text='')
confidence_text.pack(side='left')

advice_frame = Frame(main_frame, width=300, height=100, relief='ridge', bd=2)
advice_frame.pack_propagate(False)
advice_frame.grid(column=1, row=7, columnspan=2, pady=10)

advice_text = scrolledtext.ScrolledText(advice_frame, wrap=WORD)

advice_string = 'This is an advice.'
advice_text.insert("1.0", advice_string)
advice_text.pack()

root.mainloop()




