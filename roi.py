import tkinter as tk
from PIL import ImageGrab

class ROISelectionApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Seleziona regione")
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-alpha', 0.3)
        self.root.configure(bg='grey')

        self.canvas = tk.Canvas(self.root, cursor="cross", bg='grey', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.start_x = None
        self.start_y = None
        self.rect = None

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_button_move)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.root.bind("<Return>", self.on_enter_key)

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y

        if not self.rect:
            self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red")

    def on_button_move(self, event):
        cur_x, cur_y = event.x, event.y
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event):
        pass

    def on_enter_key(self, event):
        self.root.quit()

    def run(self):
        self.root.mainloop()
        bbox = self.canvas.coords(self.rect)
        x1, y1, x2, y2 = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
        return x1, y1, x2 - x1, y2 - y1

def main():
    app = ROISelectionApp()
    region = app.run()
    print("Regione selezionata:", region)

if __name__ == "__main__":
    main()

