import tkinter as tk
import random

def draw_random_lines():
    canvas.delete("all")
    for _ in range(15):
        x1 = random.randint(0, int(canvas.cget('width')))
        y1 = random.randint(0, int(canvas.cget('height')))
        x2 = random.randint(0, int(canvas.cget('width')))
        y2 = random.randint(0, int(canvas.cget('height')))
        line_id = canvas.create_line(x1, y1, x2, y2, fill='black', width=4, tags="line")
        lines[line_id] = (x1, y1, x2, y2)

def line_intersects_box(x1, y1, x2, y2, x1f, y1f, x2f, y2f):
    if (x1f <= x1 <= x2f and y1f <= y1 <= y2f) or (x1f <= x2 <= x2f and y1f <= y2 <= y2f):
        return True

    def intersects_vertical(x3, y3, x4, y4, x):
        if x3 == x4:
            return False
        y = y3 + (y4 - y3) * (x - x3) / (x4 - x3)
        return y1f <= y <= y2f and min(x3, x4) <= x <= max(x3, x4)

    def intersects_horizontal(x3, y3, x4, y4, y):
        if y3 == y4:
            return False
        x = x3 + (x4 - x3) * (y - y3) / (y4 - y3)
        return x1f <= x <= x2f and min(y3, y4) <= y <= max(y3, y4)

    return (intersects_vertical(x1, y1, x2, y2, x1f) or
            intersects_vertical(x1, y1, x2, y2, x2f) or
            intersects_horizontal(x1, y1, x2, y2, y1f) or
            intersects_horizontal(x1, y1, x2, y2, y2f))

def check_lines_in_frame():
    frame_coords = canvas.coords("frame")
    if frame_coords:
        x1f, y1f, x2f, y2f = frame_coords
        for line_id, coords in lines.items():
            x1, y1, x2, y2 = coords
            if line_intersects_box(x1, y1, x2, y2, x1f, y1f, x2f, y2f):
                canvas.itemconfig(line_id, fill='blue')
            else:
                canvas.itemconfig(line_id, fill='black')

def on_mouse_move(event):
    canvas.delete("frame")
    x1, y1 = event.x - 100, event.y - 100
    x2, y2 = event.x + 100, event.y + 100
    canvas.create_rectangle(x1, y1, x2, y2, outline="red", width=2, tags="frame")
    check_lines_in_frame()

def setup_gui():
    root = tk.Tk()
    root.title("Выявление видимых отрезков")

    root.geometry(f"+50+50")

    global canvas, lines
    lines = {}
    canvas = tk.Canvas(root, width=1200, height=900)
    canvas.pack()

    button = tk.Button(root, text="сгенерировать отрезки", command=draw_random_lines)
    button.pack()

    canvas.bind("<Motion>", on_mouse_move)

    root.mainloop()

setup_gui()
