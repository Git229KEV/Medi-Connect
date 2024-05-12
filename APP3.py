import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk
import sqlite3
import spacy
import speech_recognition as sr
import threading
import pyttsx3

# Load the English NLP model
nlp = spacy.load("en_core_web_sm")

class MedicineScheduleApp:
    def __init__(self):
        # Initialize SQLite database
        self.conn = sqlite3.connect('medicine_schedule.db')
        self.cursor = self.conn.cursor()
        
        # Create medicines table if not exists
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS medicines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                disease TEXT NOT NULL,
                medicine_name TEXT NOT NULL,
                morning TEXT,
                afternoon TEXT,
                night TEXT,
                duration_days INTEGER
            )
        ''')
        self.conn.commit()

    def add_medicine(self, disease, medicine_name, schedule, duration_days):
        self.cursor.execute('''
            INSERT INTO medicines (disease, medicine_name, morning, afternoon, night, duration_days)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (disease, medicine_name, schedule['morning'], schedule['afternoon'], schedule['night'], duration_days))
        self.conn.commit()

    def get_medicine_schedule(self, disease):
        self.cursor.execute('''
            SELECT medicine_name, morning, afternoon, night, duration_days
            FROM medicines
            WHERE disease = ?
        ''', (disease,))
        
        return self.cursor.fetchall()
    def suggest_medicine(self, symptoms, age, pre_medical_history):
        # Convert symptoms to lowercase and split into a list
        symptoms_list = symptoms.lower().split(',')

        # Convert pre_medical_history to lowercase and split into a list
        pre_medical_history_list = pre_medical_history.lower().split(',')

        # Initialize suggested medicine as None
        suggested_medicine = None

        # Rule-based medicine suggestion based on symptoms, age, and pre-medical history
        if 'headache' in symptoms_list:
            suggested_medicine = "Paracetamol"
        
        elif 'fever' in symptoms_list:
            suggested_medicine = "Ibuprofen"
        
        
        elif 'heart' in pre_medical_history_list and age < 60:
            suggested_medicine = "Aspirin"
        
        
        elif 'heart' in pre_medical_history_list and age >= 60:
            suggested_medicine = "Clopidogrel"
        
        
        elif 'diabetes' in pre_medical_history_list and age < 40:
             suggested_medicine = "Metformin"
        
       
        elif 'diabetes' in pre_medical_history_list and age >= 40:
            suggested_medicine = "Insulin"
        

        # You can add more conditions/rules based on the symptoms, age, and pre-medical history

        if suggested_medicine:
            return suggested_medicine
        else:
            return "No suggestions available"
        
    

    


def open_schedule_dialog():
    disease_name = simpledialog.askstring("Input", "Enter the name of the disease:")
    medicine_schedule = app.get_medicine_schedule(disease_name)

    if medicine_schedule:
        schedule_text = f"Medicine schedule for {disease_name}:\n"
        for med in medicine_schedule:
            schedule_text += f"Medicine: {med[0]}\n"
            schedule_text += f"Morning: {med[1]}\n"
            schedule_text += f"Afternoon: {med[2]}\n"
            schedule_text += f"Night: {med[3]}\n"
            schedule_text += f"Duration (days): {med[4]}\n\n"
        
        messagebox.showinfo("Medicine Schedule", schedule_text)
    else:
        messagebox.showinfo("Medicine Schedule", f"No medicine schedule found for {disease_name}.")

def open_suggest_medicine_dialog():
    symptoms = simpledialog.askstring("Input", "Enter the symptoms of the disease :")
    age = simpledialog.askinteger("Input", "Enter the age of the patient:")
    pre_medical_history = simpledialog.askstring("Input", "Enter the pre-medical history :")

    suggestion = app.suggest_medicine(symptoms, age, pre_medical_history)
    
    if suggestion == 'No suggestions available':
        messagebox.showinfo("Suggested Medicine", suggestion)
    else:
        messagebox.showinfo("Suggested Medicine", f"The medicine to be taken for the details entered is: {suggestion}")







def open_add_medicine_dialog():
    disease_name = simpledialog.askstring("Input", "Enter the name of the disease:")
    medicine_name = simpledialog.askstring("Input", "Enter the name of the medicine:")
    morning = simpledialog.askstring("Input", "Morning schedule:")
    afternoon = simpledialog.askstring("Input", "Afternoon schedule:")
    night = simpledialog.askstring("Input", "Night schedule:")
    duration_days = simpledialog.askinteger("Input", "Duration (days):")

    schedule = {'morning': morning, 'afternoon': afternoon, 'night': night}
    app.add_medicine(disease_name, medicine_name, schedule, duration_days)
    messagebox.showinfo("Add Medicine", "Medicine added successfully!")

def open_about_dialog():
    about_text = """
    MediConnect(beta) - Medicine Schedule App
    
    This app helps you manage and keep track of your medicine schedule based on different diseases.
    
    Features:
    - Add medicines with specific schedules for different diseases.
    - View medicine schedules.
    - Get suggested medicines based on common treatments.
    
    Developed by: KPKS.Copyright.All Rights reserved 2024
    Version: 1.0(beta)
    """
    messagebox.showinfo("About App", about_text)

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def voice_input(prompt):
    speak(prompt)
    
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
        
        try:
            text = recognizer.recognize_google(audio)
            return text.lower()
        except sr.UnknownValueError:
            messagebox.showinfo("Error", "Sorry, I could not understand your voice.")
            return None
        except sr.RequestError:
            messagebox.showinfo("Error", "Could not request results; please check your internet connection.")
            return None

def voice_assistant():
    threading.Thread(target=run_voice_assistant).start()

def run_voice_assistant():
    action = voice_input("Show medicine schedule, Suggest medicine or Exit?")
    
    if "show medicine" in action:
        # Existing code for showing medicine schedule
        pass
    
    elif "suggest medicine" in action:
        open_suggest_medicine_voice_dialog()
    elif "exit" in action:
        root.quit()
        
    else:
        messagebox.showinfo("Error", "Invalid command.")
        speak("Invalid command.")    
        
def open_suggest_medicine_voice_dialog():
    symptoms = voice_input("Please specify the symptoms of the disease.")
    age = voice_input("Please specify your age.")
    pre_medical_history = voice_input("Please specify your pre-medical history (if any).")
    
    suggested_medicine = app.suggest_medicine(symptoms, age, pre_medical_history)
    
    if suggested_medicine:
        messagebox.showinfo("Suggested Medicine", f"The medicine to be taken for the details entered is: {suggested_medicine}")
        speak(f"The medicine to be taken for the details entered is: {suggested_medicine}")
    else:
        messagebox.showinfo("Suggested Medicine", "No suggestions available")
        speak("Sorry, I couldn't suggest a medicine based on the provided information.")
app = MedicineScheduleApp()

root = tk.Tk()
root.title("MediConnect(beta)")
root.iconbitmap("C:\\Users\\Kevin\\Dropbox\\PC\\Downloads\\plus.ico")

# Add logo
logo_image = Image.open("C:\\Users\\Kevin\\Dropbox\\PC\\Downloads\\Livery and other assets\\New project.png")
logo_photo = ImageTk.PhotoImage(logo_image)
logo_label = tk.Label(root, image=logo_photo)
logo_label.pack(pady=20)

# Define button dimensions
button_width = 30
button_height = 2

font_style = ("Humnst777 Blk BT Black Italic", 15) 

btn_add_medicine = tk.Button(root, text="Add Medicine", command=open_add_medicine_dialog, width=button_width, height=button_height, font=font_style)
btn_add_medicine.pack(pady=10)


btn_show_schedule = tk.Button(root, text="Show Medicine Schedule", command=open_schedule_dialog, width=button_width, height=button_height, font=font_style)
btn_show_schedule.pack(pady=10)

btn_suggest_medicine = tk.Button(root, text="Suggest Medicine", command=open_suggest_medicine_dialog, width=button_width, height=button_height, font=font_style)
btn_suggest_medicine.pack(pady=10)



btn_about_app = tk.Button(root, text="About App", command=open_about_dialog, width=button_width, height=button_height, font=font_style)
btn_about_app.pack(pady=10)

btn_voice_assistant = tk.Button(root, text="🎙️", command=voice_assistant, width=5, height=2, font=font_style)
btn_voice_assistant.place(relx=1, rely=1, anchor='se', x=-10, y=-10)



root.mainloop()