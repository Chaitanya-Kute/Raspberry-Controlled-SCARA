import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from serial.tools.list_ports import comports
import serial

class NumericKeypad:
    def __init__(self, master, entry_var):
        self.master = master
        self.master.title("Numeric Keypad")
        self.entry_var = entry_var

        for i in range(1, 10):
            ttk.Button(self.master, text=str(i), command=lambda digit=i: self.add_digit(digit)).grid(row=(i-1)//3, column=(i-1)%3, padx=5, pady=5)

        ttk.Button(self.master, text="0", command=lambda: self.add_digit(0)).grid(row=3, column=1, padx=5, pady=5)
        ttk.Button(self.master, text="Clear", command=self.clear).grid(row=3, column=0, padx=5, pady=5)
        ttk.Button(self.master, text="Backspace", command=self.backspace).grid(row=3, column=2, padx=5, pady=5)
        ttk.Button(self.master, text="OK", command=self.master.destroy).grid(row=4, column=0, columnspan=3, pady=5)

    def add_digit(self, digit):
        current_value = self.entry_var.get()
        self.entry_var.set(current_value + str(digit))

    def clear(self):
        self.entry_var.set("")

    def backspace(self):
        current_value = self.entry_var.get()
        self.entry_var.set(current_value[:-1])

class RobotController:
    def __init__(self, root):
        self.root = root
        self.root.title("Robot Controller")

        self.available_ports = [port.device for port in comports()]
        self.serial_port_var = tk.StringVar(value=self.available_ports[0] if self.available_ports else "")
        self.serial_baudrate = 9600
        self.ser = None

        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.style.configure('TButton.Save.TButton', font=('Helvetica', 12), foreground='black', background='#0D9276', padding=5)
        self.style.map('TButton.Save.TButton', background=[('pressed', '!disabled', '#0D9276'), ('active', '#0D9276')])
        self.style.configure('TButton.Send.TButton', font=('Helvetica', 12), foreground='white', background='#FC6736', padding=5)
        self.style.map('TButton.Send.TButton', background=[('pressed', '!disabled', '#FC6736'), ('active', '#FC6736')])
        self.style.configure('TButton.Play.TButton', font=('Helvetica', 12), foreground='white', background='#0B60B0', padding=5)
        self.style.map('TButton.Play.TButton', background=[('pressed', '!disabled', '#0B60B0'), ('active', '#0B60B0')])
        self.style.configure('TButton.Clear.TButton', font=('Helvetica', 12), foreground='black', background='#B5C0D0', padding=5)
        self.style.map('TButton.Clear.TButton', background=[('pressed', '!disabled', '#B5C0D0'), ('active', '#B5C0D0')])
        self.style.configure('TButton.Stop.TButton', font=('Helvetica', 12), foreground='white', background='#D32F2F', padding=5)
        self.style.map('TButton.Stop.TButton', background=[('pressed', '!disabled', '#D32F2F'), ('active', '#D32F2F')])
        self.style.configure('TEntry', font=('Helvetica', 12), background='#B5C0D0', foreground='black', padding=5)

        ttk.Label(root, text="Select COM Port:").grid(row=0, column=0, padx=10, pady=5)
        ttk.Combobox(root, textvariable=self.serial_port_var, values=self.available_ports, state="readonly").grid(row=0, column=1, padx=10, pady=5)

        self.entry_vars = [tk.StringVar() for _ in range(5)]
        for idx, axis in enumerate(['X', 'Y', 'Z', 'A', 'G']):
            ttk.Label(root, text=f"{axis} Axis:").grid(row=idx + 1, column=0, padx=10, pady=5)
            entry = ttk.Entry(root, textvariable=self.entry_vars[idx], style='TEntry')
            entry.grid(row=idx + 1, column=1, padx=10, pady=5)
            entry.bind("<Button-1>", lambda event, entry_var=self.entry_vars[idx]: self.show_numpad(entry_var))

        ttk.Button(root, text="Save", command=self.save_checkpoint, style='TButton.Save.TButton').grid(row=6, column=0, padx=5, pady=10)
        ttk.Button(root, text="Send", command=self.send_values, style='TButton.Send.TButton').grid(row=6, column=1, padx=5, pady=10)
        ttk.Button(root, text="Play", command=self.play_checkpoints, style='TButton.Play.TButton').grid(row=6, column=2, padx=5, pady=10)
        ttk.Button(root, text="Clear Last", command=self.clear_last_checkpoint, style='TButton.Clear.TButton').grid(row=7, column=0, padx=5, pady=10)
        ttk.Button(root, text="Stop", command=self.emergency_stop, style='TButton.Stop.TButton').grid(row=7, column=1, padx=5, pady=10)
        ttk.Button(root, text="Export", command=self.export_checkpoints).grid(row=8, column=0, padx=5, pady=10)
        ttk.Button(root, text="Import", command=self.import_checkpoints).grid(row=8, column=1, padx=5, pady=10)

        self.checkpoint_count_label = ttk.Label(root, text="Number of Checkpoints: 0", font=('Helvetica', 10))
        self.checkpoint_count_label.grid(row=8, column=2, padx=5, pady=10)

        self.checkpoints = []

    def save_checkpoint(self):
        values = [var.get() for var in self.entry_vars]
        self.checkpoints.append(values)
        for var in self.entry_vars:
            var.set("")
        self.update_checkpoint_count_label()
        messagebox.showinfo("Checkpoint Saved", "Current position saved as a checkpoint.")

    def clear_last_checkpoint(self):
        if self.checkpoints:
            self.checkpoints.pop()
        self.update_checkpoint_count_label()
        messagebox.showinfo("Clear Last", "The last checkpoint has been removed.")

    def emergency_stop(self):
        messagebox.showinfo("Emergency Stop", "Emergency Stop action performed.")

    def send_values(self):
        try:
            self.ser = serial.Serial(self.serial_port_var.get(), self.serial_baudrate, timeout=1)
            values = [var.get() for var in self.entry_vars]
            command = "{},{},{},{},{}\n".format(*values)
            self.ser.write(command.encode())
            self.ser.flush()
            self.ser.close()
            for var in self.entry_vars:
                var.set("")
            self.update_checkpoint_count_label()
            messagebox.showinfo("Values Sent", "Values sent successfully!")
        except serial.SerialException:
            messagebox.showerror("Error", "Failed to establish a serial connection.")

    def play_checkpoints(self):
        try:
            self.ser = serial.Serial(self.serial_port_var.get(), self.serial_baudrate, timeout=1)
            for checkpoint in self.checkpoints:
                command = "{},{},{},{},{}\n".format(*checkpoint)
                self.ser.write(command.encode())
                self.ser.flush()
            self.ser.close()
            messagebox.showinfo("Playback Complete", "Checkpoints played successfully!")
        except serial.SerialException:
            messagebox.showerror("Error", "Failed to establish a serial connection.")

    def export_checkpoints(self):
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if file_path:
                with open(file_path, 'w', newline='') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerows(self.checkpoints)
                messagebox.showinfo("Export Complete", f"Checkpoints exported to {file_path} successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export checkpoints: {str(e)}")

    def import_checkpoints(self):
        try:
            file_path = filedialog.askopenfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if file_path:
                with open(file_path, 'r') as csvfile:
                    csv_reader = csv.reader(csvfile)
                    self.checkpoints = [list(map(float, row)) for row in csv_reader]
                self.update_checkpoint_count_label()
                messagebox.showinfo("Import Complete", f"Checkpoints imported from {file_path} successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import checkpoints: {str(e)}")

    def update_checkpoint_count_label(self):
        count = len(self.checkpoints)
        self.checkpoint_count_label.config(text=f"Number of Checkpoints: {count}")

    def show_numpad(self, entry_var):
        numpad_window = tk.Toplevel(self.root)
        numpad = NumericKeypad(numpad_window, entry_var)

if __name__ == "__main__":
    root = tk.Tk()
    app = RobotController(root)
    root.mainloop()
