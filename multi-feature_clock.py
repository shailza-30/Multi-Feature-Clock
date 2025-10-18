import tkinter as tk
from tkinter import ttk, messagebox
import time
import pytz
from datetime import datetime
 
class ClockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-Feature Clock")
        self.root.geometry("500x400")
        self.root.configure(bg="#121212")  # Dark background
 
        self.style = ttk.Style()
        self.style.theme_use('clam')
 
        # Configure styles for ttk widgets to match dark theme
        self.style.configure('TNotebook', background="#121212")
        self.style.configure('TNotebook.Tab', background="#282828", foreground="white", font=('Helvetica', 12, 'bold'))
        self.style.map('TNotebook.Tab', background=[('selected', '#4caf50')])
        self.style.configure('TFrame', background="#121212")
        self.style.configure('TLabel', background="#121212", foreground="cyan", font=('Digital-7', 24))
        self.style.configure('TButton', background="#4caf50", foreground="white", font=('Helvetica', 10, 'bold'))
 
        # --- Tabs ---
        self.tabs = ttk.Notebook(root)
        self.tabs.pack(expand=True, fill='both', pady=10)
 
        # Digital Clock Tab
        self.digital_frame = ttk.Frame(self.tabs)
        self.tabs.add(self.digital_frame, text='Digital Clock')
 
        self.digital_clock_label = tk.Label(
            self.digital_frame, text="", font=('Digital-7', 60), fg="#00ff00", bg="#121212"
        )
        self.digital_clock_label.pack(expand=True)
 
        # World Clock Tab
        self.world_frame = ttk.Frame(self.tabs)
        self.tabs.add(self.world_frame, text='World Clock')
 
        self.timezones = ['UTC', 'US/Eastern', 'Europe/London', 'Asia/Kolkata', 'Asia/Tokyo', 'Australia/Sydney']
        self.timezone_var = tk.StringVar(value=self.timezones[0])
 
        ttk.Label(self.world_frame, text="Select Timezone:", font=('Helvetica', 14, 'bold'), foreground="white").pack(pady=10)
        self.timezone_combo = ttk.Combobox(self.world_frame, values=self.timezones, textvariable=self.timezone_var, state='readonly', font=('Helvetica', 12))
        self.timezone_combo.pack()
 
        self.world_clock_label = tk.Label(
            self.world_frame, text="", font=('Digital-7', 50), fg="#00ffff", bg="#121212"
        )
        self.world_clock_label.pack(expand=True, pady=20)
 
        # Stopwatch Tab
        self.stopwatch_frame = ttk.Frame(self.tabs)
        self.tabs.add(self.stopwatch_frame, text='Stopwatch')
 
        self.stopwatch_label = tk.Label(
            self.stopwatch_frame, text="00:00:00.0", font=('Digital-7', 50), fg="#ff4081", bg="#121212"
        )
        self.stopwatch_label.pack(pady=20)
 
        self.stopwatch_running = False
        self.stopwatch_start_time = None
        self.stopwatch_elapsed = 0
 
        self.stopwatch_buttons_frame = ttk.Frame(self.stopwatch_frame)
        self.stopwatch_buttons_frame.pack()
 
        self.start_stopwatch_btn = ttk.Button(self.stopwatch_buttons_frame, text="Start", command=self.start_stopwatch)
        self.start_stopwatch_btn.grid(row=0, column=0, padx=10)
 
        self.stop_stopwatch_btn = ttk.Button(self.stopwatch_buttons_frame, text="Stop", command=self.stop_stopwatch, state='disabled')
        self.stop_stopwatch_btn.grid(row=0, column=1, padx=10)
 
        self.reset_stopwatch_btn = ttk.Button(self.stopwatch_buttons_frame, text="Reset", command=self.reset_stopwatch)
        self.reset_stopwatch_btn.grid(row=0, column=2, padx=10)
 
        # Timer Tab
        self.timer_frame = ttk.Frame(self.tabs)
        self.tabs.add(self.timer_frame, text='Timer')
 
        self.timer_label = tk.Label(
            self.timer_frame, text="00:00:00", font=('Digital-7', 50), fg="#ffeb3b", bg="#121212"
        )
        self.timer_label.pack(pady=20)
 
        self.timer_running = False
        self.timer_seconds_left = 0
 
        self.timer_entry_frame = ttk.Frame(self.timer_frame)
        self.timer_entry_frame.pack(pady=10)
 
        ttk.Label(self.timer_entry_frame, text="Hours:", foreground="white").grid(row=0, column=0)
        ttk.Label(self.timer_entry_frame, text="Minutes:", foreground="white").grid(row=0, column=2)
        ttk.Label(self.timer_entry_frame, text="Seconds:", foreground="white").grid(row=0, column=4)
 
        self.hours_var = tk.StringVar(value="0")
        self.minutes_var = tk.StringVar(value="0")
        self.seconds_var = tk.StringVar(value="0")
 
        self.hours_entry = ttk.Entry(self.timer_entry_frame, width=3, textvariable=self.hours_var, font=('Helvetica', 12))
        self.hours_entry.grid(row=0, column=1, padx=5)
 
        self.minutes_entry = ttk.Entry(self.timer_entry_frame, width=3, textvariable=self.minutes_var, font=('Helvetica', 12))
        self.minutes_entry.grid(row=0, column=3, padx=5)
 
        self.seconds_entry = ttk.Entry(self.timer_entry_frame, width=3, textvariable=self.seconds_var, font=('Helvetica', 12))
        self.seconds_entry.grid(row=0, column=5, padx=5)
 
        self.timer_buttons_frame = ttk.Frame(self.timer_frame)
        self.timer_buttons_frame.pack(pady=10)
 
        self.start_timer_btn = ttk.Button(self.timer_buttons_frame, text="Start", command=self.start_timer)
        self.start_timer_btn.grid(row=0, column=0, padx=10)
 
        self.stop_timer_btn = ttk.Button(self.timer_buttons_frame, text="Stop", command=self.stop_timer, state='disabled')
        self.stop_timer_btn.grid(row=0, column=1, padx=10)
 
        self.reset_timer_btn = ttk.Button(self.timer_buttons_frame, text="Reset", command=self.reset_timer)
        self.reset_timer_btn.grid(row=0, column=2, padx=10)
 
        # Start updating clocks
        self.update_digital_clock()
        self.update_world_clock()
 
    # Digital Clock Update with AM/PM
    def update_digital_clock(self):
        current_time = time.strftime('%I:%M:%S %p')  # 12-hour format with AM/PM
        self.digital_clock_label.config(text=current_time)
        self.root.after(1000, self.update_digital_clock)
 
    # World Clock Update with AM/PM
    def update_world_clock(self):
        tz_name = self.timezone_var.get()
        try:
            tz = pytz.timezone(tz_name)
            now = datetime.now(tz)
            time_str = now.strftime('%Y-%m-%d %I:%M:%S %p')  # 12-hour + AM/PM
        except Exception:
            time_str = "Invalid Timezone"
 
        self.world_clock_label.config(text=time_str)
        self.root.after(1000, self.update_world_clock)
 
    # Stopwatch Functions (showing tenths of seconds)
    def update_stopwatch(self):
        if self.stopwatch_running:
            now = time.time()
            elapsed = self.stopwatch_elapsed + (now - self.stopwatch_start_time)
            h, rem = divmod(elapsed, 3600)
            m, s = divmod(rem, 60)
            self.stopwatch_label.config(text=f"{int(h):02d}:{int(m):02d}:{s:04.1f}")
            self.root.after(100, self.update_stopwatch)
 
    def start_stopwatch(self):
        if not self.stopwatch_running:
            self.stopwatch_start_time = time.time()
            self.stopwatch_running = True
            self.update_stopwatch()
            self.start_stopwatch_btn.config(state='disabled')
            self.stop_stopwatch_btn.config(state='normal')
 
    def stop_stopwatch(self):
        if self.stopwatch_running:
            now = time.time()
            self.stopwatch_elapsed += now - self.stopwatch_start_time
            self.stopwatch_running = False
            self.start_stopwatch_btn.config(state='normal')
            self.stop_stopwatch_btn.config(state='disabled')
 
    def reset_stopwatch(self):
        self.stop_stopwatch()
        self.stopwatch_elapsed = 0
        self.stopwatch_label.config(text="00:00:00.0")
 
    # Timer Functions
    def update_timer(self):
        if self.timer_running:
            if self.timer_seconds_left > 0:
                self.timer_seconds_left -= 1
                h, rem = divmod(self.timer_seconds_left, 3600)
                m, s = divmod(rem, 60)
                self.timer_label.config(text=f"{int(h):02d}:{int(m):02d}:{int(s):02d}")
                self.root.after(1000, self.update_timer)
            else:
                self.timer_label.config(text="Time's Up!")
                messagebox.showinfo("Timer", "Time's Up!")
                self.stop_timer()
 
    def start_timer(self):
        if self.timer_running:
            return
 
        try:
            h = int(self.hours_var.get())
            m = int(self.minutes_var.get())
            s = int(self.seconds_var.get())
            total_seconds = h*3600 + m*60 + s
            if total_seconds <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid positive integer values for hours, minutes, and seconds.")
            return
 
        self.timer_seconds_left = total_seconds
        self.timer_running = True
        self.update_timer()
        self.start_timer_btn.config(state='disabled')
        self.stop_timer_btn.config(state='normal')
 
    def stop_timer(self):
        if self.timer_running:
            self.timer_running = False
            self.start_timer_btn.config(state='normal')
            self.stop_timer_btn.config(state='disabled')
 
    def reset_timer(self):
        self.stop_timer()
        self.timer_seconds_left = 0
        self.timer_label.config(text="00:00:00")
        self.hours_var.set("0")
        self.minutes_var.set("0")
        self.seconds_var.set("0")
 
 
if __name__ == "__main__":
    import tkinter.font as tkFont
 
    root = tk.Tk()
    available_fonts = tkFont.families()
    if 'Digital-7' not in available_fonts:
        # You can install the font for best effect or skip
        pass
 
    app = ClockApp(root)
    root.mainloop()