import tkinter as tk, qrcode, os, random, string, win32gui, win32con
from tkinter import filedialog
from PIL import Image
from pyzbar.pyzbar import decode

class QRCodeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Creator and Reader")
        self.root.geometry("500x405")
        self.root.resizable(width=False, height=False)
        self.root.configure(bg="#333")
        self.create_qr_label = tk.Label(root, text="Create QR Code", font=("Helvetica", 16), bg="#333", fg="white")
        self.create_qr_label.pack(pady=10)
        self.text_entry = tk.Entry(root, font=("Helvetica", 14))
        self.text_entry.pack(pady=5)
        self.create_button = tk.Button(root, text="Create QR Code", command=self.create_qr, font=("Helvetica", 12))
        self.create_button.pack(pady=5)
        self.save_info_label = tk.Label(root, text="", font=("Helvetica", 12), bg="#333", fg="red")
        self.save_info_label.pack()
        self.scan_qr_label = tk.Label(root, text="Scan QR Code", font=("Helvetica", 16), bg="#333", fg="white")
        self.scan_qr_label.pack(pady=10)
        self.scan_button = tk.Button(root, text="Scan QR Code", command=self.scan_qr, font=("Helvetica", 12))
        self.scan_button.pack(pady=5)

    def create_qr(self):
        data = self.text_entry.get()
        if data:
            if len(data) > 1000:
                self.show_save_location("ERROR: Text is too long for QR code")
                return

            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")

            random_filename = self.generate_random_filename()
            current_directory = os.getcwd()
            qr_filename = os.path.join(current_directory, random_filename)
            img.save(qr_filename)

            self.show_save_location(qr_filename)

            self.create_button.config(text="QR Code Created and Saved")
            self.root.after(3000, self.reset_create_button_text)
        else:
            self.show_save_location("No text provided.")

    def show_save_location(self, filename):
        self.save_info_label.config(text=f"QR code saved at:\n{filename}")

    def reset_create_button_text(self):
        self.create_button.config(text="Create QR Code")

    def generate_random_filename(self):
        letters_and_digits = string.ascii_letters + string.digits
        return ''.join(random.choice(letters_and_digits) for _ in range(10)) + ".png"

    def scan_qr(self):
        try:
            file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")])

            if file_path:
                qr_image = Image.open(file_path)
                decoded_objects = decode(qr_image)

                if decoded_objects:
                    decoded_data = decoded_objects[0].data.decode('utf-8')
                    self.show_scanned_qr(decoded_data)
                else:
                    self.show_scanned_qr("No QR code found.")
            else:
                self.show_scanned_qr("No image selected.")
        except Exception as e:
            self.show_scanned_qr("Error: " + str(e))

    def show_scanned_qr(self, data):
        if hasattr(self, "scanned_frame"):
            self.scanned_frame.destroy()

        self.scanned_frame = tk.Frame(self.root, bg="#333")
        self.scanned_frame.pack()

        scanned_label = tk.Label(self.scanned_frame, text="Scanned QR Code:", font=("Helvetica", 14), bg="#333", fg="white")
        scanned_label.pack()

        self.scanned_data_text = tk.Text(self.scanned_frame, font=("Helvetica", 12), bg="#333", fg="white", height=3, width=30)
        self.scanned_data_text.insert("1.0", data)
        self.scanned_data_text.pack()

        self.scanned_data_text.config(state="disabled")

        copy_button = tk.Button(self.scanned_frame, text="Copy", command=lambda: self.copy_to_clipboard(data), font=("Helvetica", 12))
        copy_button.pack()

    def copy_to_clipboard(self, data):
        self.root.clipboard_clear()
        self.root.clipboard_append(data)
        self.root.update()

if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeApp(root)
    win32gui.ShowWindow(win32gui.GetForegroundWindow(), win32con.SW_HIDE)
    root.mainloop()
