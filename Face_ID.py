# импорт библиотек
import random
import face_recognition
from os import listdir as ld, getcwd
import tkinter as tk
from tkinter import filedialog, Tk
from PIL import Image, ImageTk
from face_recognition import load_image_file, face_encodings, face_distance

# создание окна для загрузки изображения
root = Tk()
window_width = 450
window_height = 450
x, y = 200, 200
image_path = ""

root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# функция открытия изображения
def open_image():
    global image_path
    image_path = filedialog.askopenfilename()

    image = Image.open(image_path)
    image.show()
    photo = ImageTk.PhotoImage(image)

    label = tk.Label(root, image=photo)
    label.image = photo
    label.pack()

button = tk.Button(root, text="Откройте изображение", width=100, height=100, command=open_image)
button.pack()

root.mainloop()


class FaceID:
    # заполнение словаря именами папок
    def __init__(self):
        self.names = {} # {'name1' : [], ' name2 ' : [], ...}
        for name in [x for x in ld(getcwd()) if not ('.' in x)]:
            if name != "venv":
                self.names.update({f'{name}': []})

    # загрузка и переведение в формат библиотеки изображения из папок
    def load(self):
        for name in self.names:
            print(f'Load photos from {name}')
            for photo in ld(f'{getcwd()}\\{name}'):
                self.names[name].append(face_encodings(load_image_file(f'{getcwd()}\\{name}\\{photo}'))[0])

    # поиск схожего лица
    def search(self):
        searched_photo = face_encodings(load_image_file(image_path))[0]
        answer = 'unknown'
        max_coef = 0
        for name in self.names:
            for photo in self.names[name]:
                # поиск коеффициента схожести
                coef = 1 - face_distance([searched_photo], photo)[0]

                if coef > max_coef:
                    answer = name
                    max_coef = coef

        if max_coef <= 0.3:
            print(f'Это неизвестный базе человек')
        else:
            print(f"This is {answer}")
        print(searched_photo)

        if answer != 'unknown':
            rand_photo = random.choice(ld(f'{getcwd()}\\{answer}'))
            image_ans = Image.open(f'{getcwd()}\\{answer}\\{rand_photo}')
            image_ans.show()



# запуск функций
if __name__ == '__main__':
    k = FaceID()
    k.load()
    k.search()
