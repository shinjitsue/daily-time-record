import datetime
from datetime import timedelta

# Define the daily logs (arrival/departure times)
logs = {
    1: [("8:00 am", "12:00 pm"), ("1:00 pm", "5:00 pm")],
    2: [],  
    3: [],  
    4: [("8:00 am", "12:00 pm"), ("1:00 pm", "5:00 pm")],
    5: [("8:10 am", "12:00 pm"), ("1:00 pm", "5:00 pm")],
    6: [("8:00 am", "12:00 pm"), ("1:00 pm", "7:00 pm")],
    7: [("8:20 am", "12:00 pm"), ("1:00 pm", "5:00 pm")],
    8: [],  
    9: [],  
    10: [],  
    11: [("8:15 am", "12:00 pm"), ("1:00 pm", "5:00 pm")],
    12: [("8:05 am", "12:00 pm"), ("1:00 pm", "5:00 pm")],
    13: [("8:00 am", "12:00 pm"), ("1:00 pm", "5:00 pm")],
    14: [("8:38 am", "12:00 pm"), ("1:00 pm", "5:00 pm")],
    15: [("8:25 am", "12:00 pm"), ("1:00 pm", "5:00 pm")],
    16: [],  
    17: [],  
    18: [("8:25 am", "12:00 pm"), ("1:00 pm", "3:00 pm")],
    19: [],  
    20: [("8:20 am", "12:00 pm"), ("1:00 pm", "5:00 pm")],
    21: [],  
    22: [],  
    23: [],  
    24: [],  
    25: [],  
    26: [("8:32 am", "12:00 pm"), ("1:00 pm", "5:00 pm")],
    27: [("8:33 am", "12:00 pm"), ("1:00 pm", "4:36 pm")],
    28: [("8:18 am", "12:00 pm"), ("1:00 pm", "5:00 pm")],
    29: [("8:10 am", "12:00 pm"), ("1:00 pm", "5:00 pm")],
    30: [],  
    31: [],  
}

def parse_time(t):
    """Parse time strings in 12-hour format."""
    return datetime.datetime.strptime(t, "%I:%M %p")

def calculate_hours():
    """Calculate total hours worked and generate daily breakdown."""
    total_minutes = 0
    daily_hours = {}
    
    for day in range(1, 32):
        day_minutes = 0
        if day in logs and logs[day]:
            for start, end in logs[day]:
                start_dt = parse_time(start)
                end_dt = parse_time(end)
                diff = end_dt - start_dt
                minutes = diff.total_seconds() / 60
                day_minutes += minutes
            
            daily_hours[day] = round(day_minutes / 60, 2)
            total_minutes += day_minutes
        else:
            daily_hours[day] = 0
    
    total_hours = round(total_minutes / 60, 2)
    return total_hours, daily_hours

def generate_report():
    """Generate a summary report of worked hours."""
    total_hours, daily_hours = calculate_hours()
    
    print(f"Daily Time Record Summary")
    print(f"========================")
    
    for day in range(1, 32):
        if daily_hours[day] > 0:
            day_sessions = []
            for start, end in logs[day]:
                day_sessions.append(f"{start} - {end}")
            sessions_str = ", ".join(day_sessions)
            print(f"Day {day}: {daily_hours[day]} hours ({sessions_str})")
    
    print(f"========================")
    print(f"Total hours worked: {total_hours}")
    
    return total_hours

if __name__ == "__main__":
    total_hours = generate_report()
    print(f"x hours: {total_hours}")