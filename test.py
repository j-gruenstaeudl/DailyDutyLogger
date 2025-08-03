import customtkinter as ctk
from collections import defaultdict
import json
import tkinter as tk
from tkinter import filedialog

# Set the appearance mode and default color theme
ctk.set_appearance_mode("System")  # Modes: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue", "dark-blue", "green"

class ActivityLogApp(ctk.CTk):
    """
    A CustomTkinter application for logging daily activities.

    This application provides a tab-based interface for each day of the week,
    allowing users to input total hours, kilometers, and a list of activities.
    Each activity has a type, start time, end time, and an optional note.
    The UI for activities is dynamic, allowing users to add or remove entries.
    It now includes a feature to calculate total working hours, excluding breaks,
    both for a single day and for the entire week.
    The UI has been translated to German.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Tägliches Aktivitäten-Protokoll")
        self.geometry("1100x750")

        # Configure grid for the main window
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # German day names mapping
        self.days_of_week_en = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        self.days_of_week_de = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']
        self.day_mapping = dict(zip(self.days_of_week_en, self.days_of_week_de))
        
        # Create a reverse mapping for easy lookup
        self.reverse_day_mapping = {v: k for k, v in self.day_mapping.items()}
        self.current_day_de = "Montag"

        # Dictionaries to hold widget references for each day
        self.day_widgets = defaultdict(dict)
        self.activity_widgets = defaultdict(list)
        
        # TabView for different days
        self.day_tabs = ctk.CTkTabview(self, width=1000, height=600)
        self.day_tabs.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Create tabs for each day of the week with German names
        for day_en, day_de in self.day_mapping.items():
            self.day_tabs.add(day_de)
            self.day_tabs.tab(day_de).grid_columnconfigure(0, weight=1)
            self.create_day_tab_content(self.day_tabs.tab(day_de), day_en)

        # Set the default tab to 'Montag'
        self.day_tabs.set(self.current_day_de)

        # Add buttons and output labels to the bottom of the main window
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.button_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # New button to load from a JSON file
        self.load_json_button = ctk.CTkButton(self.button_frame, text="Daten aus JSON laden", command=self.load_from_json)
        self.load_json_button.grid(row=0, column=0, padx=10, pady=10)

        self.save_button = ctk.CTkButton(self.button_frame, text="Daten speichern und ausgeben", command=self.save_and_print_data)
        self.save_button.grid(row=0, column=1, padx=10, pady=10)
        
        self.save_json_button = ctk.CTkButton(self.button_frame, text="In JSON-Datei speichern", command=self.save_to_json)
        self.save_json_button.grid(row=0, column=2, padx=10, pady=10)

        self.clear_button = ctk.CTkButton(self.button_frame, text="Alle Daten löschen", command=self.clear_all_data)
        self.clear_button.grid(row=0, column=3, padx=10, pady=10)

        # Button for calculating total working hours for the week
        self.calculate_week_button = ctk.CTkButton(self.button_frame, text="Wochen-Arbeitsstunden berechnen", command=self.calculate_all_working_hours)
        self.calculate_week_button.grid(row=0, column=4, padx=10, pady=10)
        
        self.total_hours_label = ctk.CTkLabel(self.button_frame, text="Gesamte Arbeitsstunden: 0.0", font=ctk.CTkFont(size=16, weight="bold"))
        self.total_hours_label.grid(row=1, column=0, columnspan=5, padx=10, pady=(0, 10))

    def create_day_tab_content(self, parent_frame, day_en):
        """
        Populates a single day's tab with input widgets.
        
        Args:
            parent_frame (ctk.CTkFrame): The parent frame (the tab).
            day_en (str): The English day of the week (used for data keys).
        """
        # Get the German day name from the mapping
        day_de = self.day_mapping.get(day_en, day_en)

        # Create a scrollable frame for activities
        scrollable_frame = ctk.CTkScrollableFrame(parent_frame)
        scrollable_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=(10, 0), sticky="nsew")
        scrollable_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        self.activity_widgets[day_en] = {'frame': scrollable_frame, 'entries': []}

        # Header for the inputs
        ctk.CTkLabel(parent_frame, text=f"{day_de} Protokolleintrag", font=ctk.CTkFont(size=20, weight="bold")).grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")
        
        # Frame for total hours and km
        info_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
        info_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        info_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        ctk.CTkLabel(info_frame, text="Gesamtstunden:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        total_hours_entry = ctk.CTkEntry(info_frame)
        total_hours_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        # Bind the update function to the FocusOut event for live updates
        total_hours_entry.bind("<FocusOut>", lambda event, d=day_en: self.calculate_day_working_hours(d))
        self.day_widgets[day_en]['total_hours_entry'] = total_hours_entry

        ctk.CTkLabel(info_frame, text="Kilometer:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        km_entry = ctk.CTkEntry(info_frame)
        km_entry.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        self.day_widgets[day_en]['km_entry'] = km_entry
        
        # New button to manually calculate hours for the current day
        calculate_day_button = ctk.CTkButton(info_frame, text="Tagessumme berechnen", command=lambda d=day_en: self.calculate_day_working_hours(d))
        calculate_day_button.grid(row=0, column=4, padx=5, pady=5, sticky="ew")
        
        # Add a button to add a new activity
        add_button = ctk.CTkButton(parent_frame, text="Aktivität hinzufügen", command=lambda: self.add_activity_row(day_en))
        add_button.grid(row=3, column=0, padx=10, pady=(5, 10))

    def add_activity_row(self, day_en, activity_data=None):
        """
        Adds a new row of activity input widgets for the specified day.
        
        Args:
            day_en (str): The English day of the week (used for data keys).
            activity_data (dict, optional): Initial data for the activity.
        """
        container = self.activity_widgets[day_en]['frame']
        row_count = len(self.activity_widgets[day_en]['entries'])

        # Frame for a single activity row
        activity_frame = ctk.CTkFrame(container, fg_color="transparent")
        activity_frame.grid(row=row_count, column=0, columnspan=5, padx=5, pady=5, sticky="ew")
        activity_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Type dropdown
        type_options = ['F', 'A', 'P']
        type_dropdown = ctk.CTkOptionMenu(activity_frame, values=type_options, command=lambda value, d=day_en: self.calculate_day_working_hours(d))
        type_dropdown.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        # Start time entry
        start_entry = ctk.CTkEntry(activity_frame, placeholder_text="Startzeit")
        start_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        start_entry.bind("<FocusOut>", lambda event, d=day_en: self.calculate_day_working_hours(d))
        
        # End time entry
        end_entry = ctk.CTkEntry(activity_frame, placeholder_text="Endzeit")
        end_entry.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        end_entry.bind("<FocusOut>", lambda event, d=day_en: self.calculate_day_working_hours(d))
        
        # Note entry
        note_entry = ctk.CTkEntry(activity_frame, placeholder_text="Notiz")
        note_entry.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        
        # Remove button
        remove_button = ctk.CTkButton(activity_frame, text="X", width=30, command=lambda: self.remove_activity_row(day_en, activity_frame))
        remove_button.grid(row=0, column=4, padx=5, pady=5)

        # Populate with data if provided
        if activity_data:
            type_dropdown.set(activity_data.get('type', type_options[0]))
            start_entry.insert(0, str(activity_data.get('start', '')))
            end_entry.insert(0, str(activity_data.get('end', '')))
            note_entry.insert(0, activity_data.get('note', ''))
        
        # Store all widgets for this activity row
        activity_widgets = {
            'frame': activity_frame,
            'type': type_dropdown,
            'start': start_entry,
            'end': end_entry,
            'note': note_entry
        }
        self.activity_widgets[day_en]['entries'].append(activity_widgets)

        # Scroll to the bottom of the frame after adding a new row
        container.update_idletasks()
        
        # Recalculate total hours for the day and the week
        self.calculate_day_working_hours(day_en)

    def remove_activity_row(self, day_en, activity_frame):
        """
        Removes an activity row and its associated widgets.
        """
        for i, activity_data in enumerate(self.activity_widgets[day_en]['entries']):
            if activity_data['frame'] == activity_frame:
                # Destroy all widgets in the row
                activity_frame.destroy()
                # Remove the entry from the list
                del self.activity_widgets[day_en]['entries'][i]
                break
        
        # Recalculate total hours for the day and the week
        self.calculate_day_working_hours(day_en)

    def calculate_day_working_hours(self, day_en):
        """
        Calculates the total working hours for a specific day and updates the entry box.
        This calculation excludes break activities ('P').
        It also triggers a recalculation of the total weekly hours.
        """
        total_hours = 0.0
        for activity_entry_set in self.activity_widgets[day_en]['entries']:
            if activity_entry_set['type'].get() != 'P':
                try:
                    start = float(activity_entry_set['start'].get())
                    end = float(activity_entry_set['end'].get())
                    if end > start:
                        total_hours += (end - start)
                except ValueError:
                    continue
        
        # Get the German tab name from the English key
        day_de = self.day_mapping.get(day_en)
        current_tab_name = self.day_tabs.get()

        # Only update the 'Gesamtstunden' entry for the currently active tab
        if day_de == current_tab_name:
            total_hours_entry = self.day_widgets[day_en].get('total_hours_entry')
            if total_hours_entry:
                total_hours_entry.delete(0, ctk.END)
                total_hours_entry.insert(0, f"{total_hours:.2f}")

        # Recalculate total weekly hours after any daily change
        self.calculate_all_working_hours()
    
    def clear_all_data(self):
        """
        Clears all data from the GUI and the internal data structure.
        """
        for day_en in self.days_of_week_en:
            # Clear total hours and km entries
            total_hours_entry = self.day_widgets[day_en].get('total_hours_entry')
            km_entry = self.day_widgets[day_en].get('km_entry')
            
            if total_hours_entry:
                total_hours_entry.delete(0, ctk.END)
            if km_entry:
                km_entry.delete(0, ctk.END)
            
            # Remove all activity rows
            for activity_data in list(self.activity_widgets[day_en]['entries']):
                self.remove_activity_row(day_en, activity_data['frame'])

        # Reset the total hours label
        self.total_hours_label.configure(text="Gesamte Arbeitsstunden: 0.0")

    def load_from_json(self):
        """
        Opens a file dialog to let the user select a JSON file and loads its data into the app.
        """
        file_path = filedialog.askopenfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All Files", "*.*")],
            title="Wählen Sie eine JSON-Datei"
        )
        if not file_path:
            return  # User canceled the dialog

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                loaded_data = json.load(f)
            
            self.clear_all_data() # Clear existing data first

            for day_en in self.days_of_week_en:
                if day_en in loaded_data:
                    data = loaded_data[day_en]

                    # Update the total hours and km entries for the day
                    total_hours_entry = self.day_widgets[day_en]['total_hours_entry']
                    km_entry = self.day_widgets[day_en]['km_entry']
                    
                    total_hours_entry.delete(0, ctk.END)
                    total_hours_entry.insert(0, str(data.get('total_hours', 0)))
                    
                    km_entry.delete(0, ctk.END)
                    km_entry.insert(0, str(data.get('km', 0)))

                    # Populate activities
                    for activity in data.get('activities', []):
                        self.add_activity_row(day_en, activity)
            
            # After loading, recalculate the total hours for the entire week
            self.calculate_all_working_hours()
            print(f"Daten erfolgreich aus {file_path} geladen.")

        except (IOError, json.JSONDecodeError) as e:
            print(f"Fehler beim Laden der Datei: {e}")

    def collect_data(self):
        """
        Collects all data from the GUI and returns it in the desired dictionary format.
        
        Returns:
            dict: The final dictionary with all the collected data.
        """
        final_data = {}
        for day_en in self.days_of_week_en:
            day_data = {}
            
            # Get total hours and km from the day_widgets dictionary
            total_hours_entry = self.day_widgets[day_en].get('total_hours_entry')
            km_entry = self.day_widgets[day_en].get('km_entry')
            
            try:
                day_data['total_hours'] = float(total_hours_entry.get())
            except (ValueError, AttributeError):
                day_data['total_hours'] = 0.0 # Default to 0 if input is not a number or widget not found
            
            try:
                day_data['km'] = float(km_entry.get())
            except (ValueError, AttributeError):
                day_data['km'] = 0.0 # Default to 0 if input is not a number or widget not found

            # Collect activity data
            activities = []
            for activity_entry_set in self.activity_widgets[day_en]['entries']:
                try:
                    activity = {
                        'type': activity_entry_set['type'].get(),
                        'start': float(activity_entry_set['start'].get()),
                        'end': float(activity_entry_set['end'].get()),
                        'note': activity_entry_set['note'].get()
                    }
                    activities.append(activity)
                except ValueError:
                    # Skip entries with invalid numerical data
                    print(f"Skipping an activity for {day_en} due to invalid numerical input.")
            
            day_data['activities'] = activities
            final_data[day_en] = day_data
            
        return final_data

    def save_and_print_data(self):
        """
        Collects the data, recalculates the weekly hours, and prints it to the console in a nicely formatted way.
        """
        self.calculate_all_working_hours() # Ensure the latest total is calculated
        collected_data = self.collect_data()
        print("--- Gesammelte Daten ---")
        print(json.dumps(collected_data, indent=4))
        print("----------------------")
        
    def save_to_json(self):
        """
        Collects the data, recalculates the weekly hours, and saves it to a JSON file chosen by the user.
        """
        self.calculate_all_working_hours() # Ensure the latest total is calculated
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All Files", "*.*")],
            title="Daten als JSON speichern"
        )
        if file_path:
            collected_data = self.collect_data()
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(collected_data, f, indent=4, ensure_ascii=False)
                print(f"Daten erfolgreich in {file_path} gespeichert.")
            except IOError as e:
                print(f"Fehler beim Speichern der Datei: {e}")

    def calculate_all_working_hours(self):
        """
        Calculates the total working hours from all activities, excluding breaks ('P'),
        for the entire week and updates the label at the bottom of the window.
        """
        collected_data = self.collect_data()
        total_working_hours = 0.0
        
        for day_en, data in collected_data.items():
            for activity in data.get('activities', []):
                # Check if the activity is not a 'break'
                if activity.get('type') != 'P':
                    start_time = activity.get('start')
                    end_time = activity.get('end')
                    # Ensure start and end times are valid numbers before calculating
                    if isinstance(start_time, (int, float)) and isinstance(end_time, (int, float)):
                        duration = end_time - start_time
                        if duration > 0:
                            total_working_hours += duration

        # Update the label with the new total
        self.total_hours_label.configure(text=f"Gesamte Arbeitsstunden: {total_working_hours:.2f}")
        print(f"Gesamte Arbeitsstunden (ohne Pausen): {total_working_hours:.2f}")


if __name__ == "__main__":
    app = ActivityLogApp()
    app.mainloop()

