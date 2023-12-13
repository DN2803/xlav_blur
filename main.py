import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
from blur import *
from tkinter import messagebox

def validate_entry(text):
    try:
        int_value = int(text)
        if int_value % 2 != 0:
            return True
        else:
            return False
    except ValueError:
        return False
# use to valid kernel size
def on_validate(P, entry_value):
    if validate_entry(entry_value):
        return True
    else:
        root.bell()  # Phát âm thanh khi có giá trị không hợp lệ
        return False

class ImageProcessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processing App")

        self.image_path = None
        self.original_image = None        
        self.noisy_image = None
        self.processed_image = None

        # UI components
        # load image 
        frame_dislay_image = tk.Frame()
        frame_dislay_image.pack(side="top")

        self.original_image_label = tk.Label(frame_dislay_image, text="Ảnh gốc")
        self.original_image_label.grid(row=0, column=0)

        self.original_image_display = tk.Label(frame_dislay_image)
        self.original_image_display.grid(row =1, column=0)

        self.noisy_image_label = tk.Label(frame_dislay_image, text="Ảnh nhiễu")
        self.noisy_image_label.grid(row=0, column=1)

        self.noisy_image_display = tk.Label(frame_dislay_image)
        self.noisy_image_display.grid(row=1, column=1)

        self.processed_image_label = tk.Label(frame_dislay_image, text="Ảnh kết quả")
        self.processed_image_label.grid(row=0, column=2)

        self.processed_image_display = tk.Label(frame_dislay_image)
        self.processed_image_display.grid(row=1, column=2)

        self.browse_button = tk.Button(self.root, text="Chọn ảnh", command=self.browse_image)
        self.browse_button.pack(pady=5)

        self.add_noise_button = tk.Button(self.root, text="Tạo ảnh nhiễu", command=self.add_noise)
        self.add_noise_button.pack(pady=5)
        self.stddev_label = tk.Label(self.root, text="Độ nhiễu:")
        self.stddev_label.pack(pady=5)
        self.stddev_entry = tk.Entry(self.root)
        self.stddev_entry.insert(0, "20")
        self.stddev_entry.pack(pady=5)

        self.kernel_size_label = tk.Label(self.root, text="Kích thước kernel:")
        self.kernel_size_label.pack(pady= 5)
        self.kernel_size_entry = tk.Entry(self.root)
        self.kernel_size_entry.insert(0, "3")
        self.kernel_size_entry.pack(pady=5)
        self.sigma_label = tk.Label(self.root, text="Giá trị Sigma:")
        self.sigma_label.pack(pady= 5)
        self.sigma_entry = tk.Entry(self.root)
        self.sigma_entry.insert(0, "1")
        self.sigma_entry.pack(pady=5)

        self.blur_method_label = tk.Label(self.root, text="Phương pháp làm trơn:")
        self.blur_method_label.pack()
        self.blur_method_var = tk.StringVar()
        self.blur_method_var.set("BLUR")
        self.blur_method_menu = tk.OptionMenu(self.root, self.blur_method_var, "BLUR_AVERANGE", "BLUR_GAUSSIAN", "BLUR_MEDIAN", 
                                              "CV2_AVERANGE","CV2_GAUSSIAN", "CV2_MEDIAN")
        self.blur_method_menu.pack(pady=5)

        self.use_noisy_image = tk.IntVar()
        self.use_noisy_image_checkbutton = tk.Checkbutton(self.root, text = "Sử dụng ảnh nhiễu", variable=self.use_noisy_image)
        self.use_noisy_image_checkbutton.pack(pady=5)

        self.process_button = tk.Button(self.root, text="Xử lý ảnh", command=self.process_image)
        self.process_button.pack(pady=5)

        self.save_button = tk.Button(self.root, text="Xuất ảnh", command=self.save_image)
        self.save_button.pack(pady=5)

    def browse_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
        if file_path:
            self.image_path = file_path
            self.original_image = cv2.imread(self.image_path)
            self.original_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)
            self.noisy_image = None
            self.processed_image = None
            self.update_image_display(self.original_image, self.original_image_display)
            self.update_image_display(self.noisy_image, self.noisy_image_display)
            self.update_image_display(self.processed_image, self.processed_image_display)

    def update_image_display(self, image, image_display):
        max_width = 400
        max_height = 300
        _image_display = image

        if image is not None:
            height, width, _ = _image_display.shape

            # Giới hạn kích thước ảnh
            if width > max_width or height > max_height:
                scale = min(max_width / width, max_height / height)
                new_width = int(width * scale)
                new_height = int(height * scale)

                _image_display = cv2.resize(image, (new_width, new_height))

            image_tk = ImageTk.PhotoImage(Image.fromarray(_image_display))
            image_display.config(image=image_tk)
            image_display.image = image_tk
       

    def add_noise(self):
        if self.original_image is not None:
            stddev = int(self.stddev_entry.get())
            self.noisy_image = GaussianNoise(self.original_image, stddev)
            self.update_image_display(self.noisy_image, self.noisy_image_display)

    def process_image_implementation(self, image):
        kernel_size = int(self.kernel_size_entry.get())
        entered_value = self.kernel_size_entry.get()

        if not validate_entry(entered_value):
            messagebox.showerror("Lỗi", "Vui lòng nhập số lẻ.")
            return

        blur_method = self.blur_method_var.get()
        sigma = float(self.sigma_entry.get())
        if blur_method == "CV2_AVERANGE":
            self.processed_image = cv2.blur(image, (kernel_size, kernel_size))
        elif blur_method == "CV2_MEDIAN":
            self.processed_image = cv2.medianBlur(image, kernel_size)
        elif blur_method == "CV2_GAUSSIAN":
            self.processed_image = cv2.GaussianBlur(image, (kernel_size, kernel_size), sigma)
        elif blur_method == "BLUR_AVERANGE":
            self.processed_image = blur_avarage(image,  (kernel_size, kernel_size))
        elif blur_method == "BLUR_GAUSSIAN": 
            self.processed_image = blur_Gaussian(image, (kernel_size, kernel_size), sigma)
        elif blur_method == "BLUR_MEDIAN": 
            self.processed_image = blur_Median(image, (kernel_size, kernel_size))

    def process_image(self):
        if self.use_noisy_image.get(): 
            if self.noisy_image is not None:
                self.process_image_implementation(self.noisy_image)
                
        elif self.original_image is not None:
            self.process_image_implementation(self.original_image)

        self.update_image_display(self.processed_image, self.processed_image_display)

    def save_image(self):
        if self.processed_image is not None:
            save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if save_path:
                cv2.imwrite(save_path, cv2.cvtColor(self.processed_image, cv2.COLOR_RGB2BGR))

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessingApp(root)
    root.mainloop()
