import datetime
import calendar
from datetime import timedelta
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class DTR:
    def __init__(self, month=None, year=None):
        # Set default to current month and year if not provided
        today = datetime.datetime.now()
        self.month = month if month else today.month
        self.year = year if year else today.year
        
        self.data_file = f"dtr_data_{self.year}.json"
        self.logs = self.load_data()
    
    def load_data(self):
        """Load time records from JSON file or create empty structure"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                # Convert string keys back to integers for the month we're viewing
                month_key = str(self.month)
                if month_key in data:
                    return {int(day): value for day, value in data[month_key].items()}
                return {}
        else:
            return {}
    
    def save_data(self):
        """Save time records to JSON file"""
        # Load existing data first to avoid overwriting other months
        all_data = {}
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                all_data = json.load(f)
        
        # Convert int keys to strings for JSON compatibility
        month_key = str(self.month)
        all_data[month_key] = {str(day): entries for day, entries in self.logs.items()}
        
        with open(self.data_file, 'w') as f:
            json.dump(all_data, f, indent=2)
    
    def parse_time(self, t):
        """Parse time strings in 12-hour format."""
        try:
            return datetime.datetime.strptime(t, "%I:%M %p")
        except ValueError:
            return None

    def validate_time_entry(self, start, end):
        """Validate time entries to ensure they make logical sense"""
        start_dt = self.parse_time(start)
        end_dt = self.parse_time(end)
        
        if not start_dt or not end_dt:
            return False, "Invalid time format. Use '12:00 am/pm' format."
        
        if end_dt <= start_dt:
            return False, "End time must be after start time."
            
        return True, ""

    def add_time_entry(self, day, start_time, end_time):
        """Add a time entry for a specific day with validation"""
        # Ensure day is within valid range for the month
        days_in_month = calendar.monthrange(self.year, self.month)[1]
        if not 1 <= day <= days_in_month:
            return False, f"Invalid day. Must be between 1 and {days_in_month}."
        
        valid, message = self.validate_time_entry(start_time, end_time)
        if not valid:
            return False, message
        
        # Initialize the day entry if it doesn't exist
        if day not in self.logs:
            self.logs[day] = []
        
        self.logs[day].append((start_time, end_time))
        self.save_data()
        return True, "Entry added successfully."

    def delete_time_entry(self, day, index):
        """Delete a specific time entry"""
        if day in self.logs and 0 <= index < len(self.logs[day]):
            self.logs[day].pop(index)
            self.save_data()
            return True, "Entry deleted successfully."
        return False, "Entry not found."

    def calculate_hours(self):
        """Calculate total hours worked and generate daily breakdown."""
        total_minutes = 0
        daily_hours = {}
        
        days_in_month = calendar.monthrange(self.year, self.month)[1]
        for day in range(1, days_in_month + 1):
            day_minutes = 0
            if day in self.logs and self.logs[day]:
                for start, end in self.logs[day]:
                    start_dt = self.parse_time(start)
                    end_dt = self.parse_time(end)
                    if start_dt and end_dt and end_dt > start_dt:
                        diff = end_dt - start_dt
                        minutes = diff.total_seconds() / 60
                        day_minutes += minutes
                
                daily_hours[day] = round(day_minutes / 60, 2)
                total_minutes += day_minutes
            else:
                daily_hours[day] = 0
        
        total_hours = round(total_minutes / 60, 2)
        return total_hours, daily_hours

    def load_all_data(self):
        """Load all available data across all months for the year"""
        all_data = {}
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                all_data = json.load(f)
        return all_data
    
    def calculate_all_hours(self):
        """Calculate total hours across all months for the year"""
        all_data = self.load_all_data()
        total_minutes = 0
        months_data = {}
        
        for month_key, month_data in all_data.items():
            month_minutes = 0
            month_num = int(month_key)
            
            for day_key, entries in month_data.items():
                day_minutes = 0
                
                for start, end in entries:
                    start_dt = self.parse_time(start)
                    end_dt = self.parse_time(end)
                    if start_dt and end_dt and end_dt > start_dt:
                        diff = end_dt - start_dt
                        minutes = diff.total_seconds() / 60
                        day_minutes += minutes
                
                month_minutes += day_minutes
            
            months_data[month_num] = round(month_minutes / 60, 2)
            total_minutes += month_minutes
        
        total_hours = total_minutes / 60
        hours = int(total_hours)
        minutes = int((total_hours - hours) * 60)
        
        return hours, minutes, months_data

    def generate_report(self):
        """Generate a summary report of worked hours."""
        total_hours, daily_hours = self.calculate_hours()
        month_name = calendar.month_name[self.month]
        days_in_month = calendar.monthrange(self.year, self.month)[1]
        
        report = []
        report.append(f"Daily Time Record Summary for {month_name} {self.year}")
        report.append(f"================================================")
        
        for day in range(1, days_in_month + 1):
            if day in self.logs and self.logs[day]:
                day_sessions = []
                for start, end in self.logs[day]:
                    day_sessions.append(f"{start} - {end}")
                sessions_str = ", ".join(day_sessions)
                report.append(f"Day {day}: {daily_hours[day]} hours ({sessions_str})")
        
        report.append(f"================================================")
        report.append(f"Total hours worked: {total_hours}")
        
        return report, total_hours


class DTRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Daily Time Record Manager")
        self.root.geometry("900x650")
            
        # Set a theme for a more modern look
        style = ttk.Style()
        if 'clam' in style.theme_names():  # Check if 'clam' theme is available
            style.theme_use('clam')
        
        # Configure some styles
        style.configure('TButton', font=('Segoe UI', 10))
        style.configure('TLabel', font=('Segoe UI', 10))
        style.configure('TFrame', background='#f5f5f5')
        style.configure('Header.TLabel', font=('Segoe UI', 12, 'bold'))
        style.configure('Stats.TLabel', font=('Segoe UI', 11), foreground='#0066cc')
        
        # Default to current month and year
        today = datetime.datetime.now()
        self.current_month = today.month
        self.current_year = today.year
        
        self.dtr = DTR(self.current_month, self.current_year)
        
        self.setup_ui()
    
    def setup_ui(self):
        # Main frame with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create a frame for the header/control panel with modern styling
        header_frame = ttk.Frame(main_frame, padding="10", style='TFrame')
        header_frame.pack(fill=tk.X)
        
        # Title
        title_label = ttk.Label(header_frame, text="Daily Time Record Manager", style='Header.TLabel')
        title_label.grid(row=0, column=0, columnspan=5, pady=(0, 10))
        
        # Month and Year selectors
        ttk.Label(header_frame, text="Month:").grid(row=1, column=0, padx=5)
        self.month_var = tk.StringVar(value=calendar.month_name[self.current_month])
        month_combo = ttk.Combobox(header_frame, textvariable=self.month_var, 
                                   values=[calendar.month_name[i] for i in range(1, 13)],
                                   width=12)
        month_combo.grid(row=1, column=1, padx=5)
        month_combo.bind("<<ComboboxSelected>>", self.update_month)
        
        ttk.Label(header_frame, text="Year:").grid(row=1, column=2, padx=5)
        self.year_var = tk.StringVar(value=str(self.current_year))
        year_combo = ttk.Combobox(header_frame, textvariable=self.year_var,
                                 values=[str(y) for y in range(2020, 2030)],
                                 width=6)
        year_combo.grid(row=1, column=3, padx=5)
        year_combo.bind("<<ComboboxSelected>>", self.update_year)
        
        # Generate report and total hours buttons
        button_frame = ttk.Frame(header_frame)
        button_frame.grid(row=1, column=4, padx=15)
        
        ttk.Button(button_frame, text="Generate Report", 
                  command=self.show_report).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Total Hours", 
                  command=self.show_total_hours).pack(side=tk.LEFT, padx=5)
        
        # Add a notebook/tab control for different views
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(expand=True, fill=tk.BOTH, padx=5, pady=10)
        
        # Create tabs
        self.data_entry_tab = ttk.Frame(self.notebook)
        self.report_tab = ttk.Frame(self.notebook)
        self.total_hours_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.data_entry_tab, text="Data Entry")
        self.notebook.add(self.report_tab, text="Monthly Report")
        self.notebook.add(self.total_hours_tab, text="Total Hours")
        
        # Set up the data entry tab
        self.setup_data_entry_tab()
        
        # Set up the report tab
        self.setup_report_tab()
        
        # Set up the total hours tab
        self.setup_total_hours_tab()
    
    def setup_data_entry_tab(self):
        # Create a frame for entry fields
        entry_frame = ttk.LabelFrame(self.data_entry_tab, text="Add Time Entry", padding="10")
        entry_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Day entry
        ttk.Label(entry_frame, text="Day:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.day_var = tk.StringVar()
        ttk.Entry(entry_frame, textvariable=self.day_var, width=5).grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Time entries
        ttk.Label(entry_frame, text="Start Time:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.start_var = tk.StringVar(value="8:00 am")  # Set default value
        ttk.Entry(entry_frame, textvariable=self.start_var, width=15).grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(entry_frame, text="Format: 8:00 am").grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(entry_frame, text="End Time:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.end_var = tk.StringVar(value="12:00 pm")  # Set default value
        ttk.Entry(entry_frame, textvariable=self.end_var, width=15).grid(row=2, column=1, padx=5, pady=5)
        ttk.Label(entry_frame, text="Format: 12:00 pm").grid(row=2, column=2, padx=5, pady=5, sticky=tk.W)
        
        # Buttons
        button_frame = ttk.Frame(entry_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=10)
        
        ttk.Button(button_frame, text="Add Entry", command=self.add_entry).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_entry_fields).pack(side=tk.LEFT, padx=5)
        
        # Display current entries
        display_frame = ttk.LabelFrame(self.data_entry_tab, text="Current Entries", padding="10")
        display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Treeview for displaying entries
        columns = ("day", "start_time", "end_time", "duration")
        self.tree = ttk.Treeview(display_frame, columns=columns, show="headings")
        
        self.tree.heading("day", text="Day")
        self.tree.heading("start_time", text="Start Time")
        self.tree.heading("end_time", text="End Time")
        self.tree.heading("duration", text="Duration (hrs)")
        
        self.tree.column("day", width=50)
        self.tree.column("start_time", width=150)
        self.tree.column("end_time", width=150)
        self.tree.column("duration", width=100)
        
        # Add a scrollbar
        scrollbar = ttk.Scrollbar(display_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        # Pack the tree and scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Button to delete selected entry
        button_frame = ttk.Frame(display_frame)
        button_frame.pack(fill=tk.X, pady=5)
        ttk.Button(button_frame, text="Delete Selected", 
                  command=self.delete_selected_entry).pack(side=tk.LEFT, padx=5)
        
        # Populate the tree with existing entries
        self.update_entries_display()
    
    def setup_report_tab(self):
        # Create a frame for the report
        report_frame = ttk.Frame(self.report_tab, padding="10")
        report_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create a text widget to display the report
        self.report_text = tk.Text(report_frame, wrap=tk.WORD, padx=10, pady=10, font=("Segoe UI", 10))
        self.report_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Add a scrollbar
        scrollbar = ttk.Scrollbar(report_frame, orient=tk.VERTICAL, command=self.report_text.yview)
        self.report_text.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def setup_total_hours_tab(self):
        # Create a frame for total hours
        total_frame = ttk.Frame(self.total_hours_tab, padding="10")
        total_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_label = ttk.Label(total_frame, text="Total Hours Worked", style='Header.TLabel')
        header_label.pack(pady=(0, 15))
        
        # Create a frame for the total hours summary
        summary_frame = ttk.LabelFrame(total_frame, text="Summary", padding="10")
        summary_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Labels for displaying total hours and minutes
        self.total_hours_label = ttk.Label(summary_frame, text="", style='Stats.TLabel')
        self.total_hours_label.pack(pady=5)
        
        # Create a frame for monthly breakdown
        monthly_frame = ttk.LabelFrame(total_frame, text="Monthly Breakdown", padding="10")
        monthly_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Treeview for displaying monthly breakdown
        columns = ("month", "hours", "percent")
        self.months_tree = ttk.Treeview(monthly_frame, columns=columns, show="headings", height=12)
        
        self.months_tree.heading("month", text="Month")
        self.months_tree.heading("hours", text="Hours")
        self.months_tree.heading("percent", text="% of Total")
        
        self.months_tree.column("month", width=150)
        self.months_tree.column("hours", width=100)
        self.months_tree.column("percent", width=100)
        
        # Add a scrollbar
        scrollbar = ttk.Scrollbar(monthly_frame, orient=tk.VERTICAL, command=self.months_tree.yview)
        self.months_tree.configure(yscroll=scrollbar.set)
        
        # Pack the tree and scrollbar
        self.months_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def update_entries_display(self):
        # Clear current entries
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add entries from the DTR object
        for day, entries in sorted(self.dtr.logs.items()):
            for i, (start, end) in enumerate(entries):
                start_dt = self.dtr.parse_time(start)
                end_dt = self.dtr.parse_time(end)
                
                if start_dt and end_dt:
                    diff = end_dt - start_dt
                    duration_hrs = round(diff.total_seconds() / 3600, 2)
                    self.tree.insert("", tk.END, values=(day, start, end, duration_hrs),
                                   tags=(f"{day}_{i}",))
    
    def update_total_hours_display(self):
        # Calculate total hours across all months
        hours, minutes, months_data = self.dtr.calculate_all_hours()
        
        # Update the summary label
        self.total_hours_label.config(text=f"Total Hours: {hours} hours and {minutes} minutes")
        
        # Clear current entries
        for item in self.months_tree.get_children():
            self.months_tree.delete(item)
        
        # Calculate total hours for percentage calculation
        total_hours = sum(months_data.values())
        
        # Add monthly data to the tree
        for month_num, hours in sorted(months_data.items()):
            month_name = calendar.month_name[month_num]
            percentage = (hours / total_hours * 100) if total_hours > 0 else 0
            self.months_tree.insert("", tk.END, values=(month_name, f"{hours:.2f}", f"{percentage:.1f}%"))
    
    def add_entry(self):
        try:
            day = int(self.day_var.get())
            start_time = self.start_var.get()
            end_time = self.end_var.get()
            
            success, message = self.dtr.add_time_entry(day, start_time, end_time)
            
            if success:
                self.update_entries_display()
                self.clear_entry_fields()
            else:
                messagebox.showerror("Error", message)
                
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid day number.")
    
    def delete_selected_entry(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Info", "No entry selected")
            return
        
        for item in selected:
            values = self.tree.item(item, "values")
            day = int(values[0])
            
            # Find the index based on start and end times
            for i, (start, end) in enumerate(self.dtr.logs.get(day, [])):
                if start == values[1] and end == values[2]:
                    success, message = self.dtr.delete_time_entry(day, i)
                    if success:
                        break
        
        self.update_entries_display()
    
    def clear_entry_fields(self):
        self.day_var.set("")
        self.start_var.set("8:00 am")
        self.end_var.set("12:00 pm")  
    
    def update_month(self, event):
        month_name = self.month_var.get()
        for i in range(1, 13):
            if calendar.month_name[i] == month_name:
                self.current_month = i
                break
        
        self.dtr = DTR(self.current_month, self.current_year)
        self.update_entries_display()
    
    def update_year(self, event):
        try:
            self.current_year = int(self.year_var.get())
            self.dtr = DTR(self.current_month, self.current_year)
            self.update_entries_display()
        except ValueError:
            messagebox.showerror("Error", "Invalid year format")
    
    def show_report(self):
        report, _ = self.dtr.generate_report()
        
        # Clear and update the report text
        self.report_text.delete(1.0, tk.END)
        self.report_text.insert(tk.END, "\n".join(report))
        
        # Switch to the report tab
        self.notebook.select(self.report_tab)
    
    def show_total_hours(self):
        # Update the total hours display
        self.update_total_hours_display()
        
        # Switch to the total hours tab
        self.notebook.select(self.total_hours_tab)

def main():
    root = tk.Tk()
    root.configure(bg="#f5f5f5")
    app = DTRApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()