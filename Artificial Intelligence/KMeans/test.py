import tkinter as tk
from PIL import Image, ImageTk


def chrome(color):
    if color < (255 // 3):
        return 0
    elif color > (255 // 3 * 2):
        return 255
    else:
        return 127


def negate(c):
    return 255 - c


def main():
    window = tk.Tk()
    imagefile = "cute_dog.jpg"
    img = ImageTk.PhotoImage(Image.open(imagefile))
    tk.Label(window, image=img).pack()
    img2 = Image.open(imagefile)
    print(img2.size)  # a tuple of (# of rows, # of cols)
    pix = img2.load()
    print(pix[2, 5])  # a tuple of (r, g, b)
    for x in range(img2.size[0]):
        for y in range(img2.size[1]):
            r, g, b = pix[x, y]
            # pix[x, y] = (chrome(r), chrome(g), chrome(b))
            pix[x, y] = (negate(r), negate(g), negate(b))
        # img2.show()
    img3 = ImageTk.PhotoImage(img2)
    tk.Label(window, image=img3).pack()
    window.mainloop()


if __name__ == "__main__":
    main()
