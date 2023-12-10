import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
from blur import *
class ImageProcessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processing App")

        self.image_path = None
        self.original_image = None
        self.processed_image = None

        # UI components
        # load image 
        frame_dislay_image = tk.Frame()
        frame_dislay_image.pack(side="top")

        self.original_image_label = tk.Label(frame_dislay_image, text="Ảnh gốc")
        self.original_image_label.grid(row=0, column=0)

        self.original_image_display = tk.Label(frame_dislay_image)
        self.original_image_display.grid(row =1, column=0)

        self.processed_image_label = tk.Label(frame_dislay_image, text="Ảnh kết quả")
        self.processed_image_label.grid(row=0, column=1)

        self.processed_image_display = tk.Label(frame_dislay_image)
        self.processed_image_display.grid(row=1, column=1)


        self.browse_button = tk.Button(self.root, text="Chọn ảnh", command=self.browse_image)
        self.browse_button.pack(pady=5)

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

        self.blur_method_label = tk.Label(self.root, text="Phương pháp làm mờ:")
        self.blur_method_label.pack()
        self.blur_method_var = tk.StringVar()
        self.blur_method_var.set("BLUR")
        self.blur_method_menu = tk.OptionMenu(self.root, self.blur_method_var, "BLUR_AVERANGE", "BLUR_GAUSSIAN", "BLUR_MEDIAN", 
                                              "CV2_AVERANGE","CV2_GAUSSIAN", "CV2_MEDIAN")
        self.blur_method_menu.pack(pady=5)

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
            self.processed_image = None
            self.update_image_display()

    def update_image_display(self):
        max_width = 400
        max_height = 300
        

        _original_image_display = None
        _processed_image_display = None

        
        
        if self.original_image is not None:
            height_src, width_src, _ = self.original_image.shape
        
            # Giới hạn kích thước ảnh
            if width_src > max_width or height_src > max_height:
                scale = min(max_width / width_src, max_height / height_src)
                new_width = int(width_src * scale)
                new_height = int(height_src * scale)

                _original_image_display = cv2.resize(self.original_image, (new_width, new_height))
            
            original_image_tk = ImageTk.PhotoImage(Image.fromarray(_original_image_display))
            self.original_image_display.config(image=original_image_tk)
            self.original_image_display.image = original_image_tk

        if self.processed_image is not None:
            height_dst, width_dst, _ = self.processed_image.shape
            if width_dst > max_width or height_dst > max_height:
                scale = min(max_width / width_dst, max_height / height_dst)
                new_width = int(width_dst * scale)
                new_height = int(height_dst * scale)

                _processed_image_display = cv2.resize(self.processed_image, (new_width, new_height))

            processed_image_tk = ImageTk.PhotoImage(Image.fromarray(_processed_image_display))
            self.processed_image_display.config(image=processed_image_tk)
            self.processed_image_display.image = processed_image_tk

    def process_image(self):
        if self.original_image is not None:
            kernel_size = int(self.kernel_size_entry.get())
            blur_method = self.blur_method_var.get()
            sigma = float(self.sigma_entry.get())
            if blur_method == "CV2_AVERANGE":
                self.processed_image = cv2.blur(self.original_image, (kernel_size, kernel_size))
            elif blur_method == "CV2_MEDIAN":
                self.processed_image = cv2.medianBlur(self.original_image, kernel_size)
            elif blur_method == "CV2_GAUSSIAN":
                self.processed_image = cv2.GaussianBlur(self.original_image, (kernel_size, kernel_size), sigma)
            elif blur_method == "BLUR_AVERANGE":
                self.processed_image = blur_avarage(self.original_image,  (kernel_size, kernel_size))
            elif blur_method == "BLUR_GAUSSIAN": 
                self.processed_image = blur_Gaussian(self.original_image, (kernel_size, kernel_size), sigma)
            elif blur_method == "BLUR_MEDIAN": 
                self.processed_image = blur_Median(self.original_image, (kernel_size, kernel_size))
            self.update_image_display()

    def save_image(self):
        if self.processed_image is not None:
            save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if save_path:
                cv2.imwrite(save_path, cv2.cvtColor(self.processed_image, cv2.COLOR_RGB2BGR))

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessingApp(root)
    root.mainloop()
