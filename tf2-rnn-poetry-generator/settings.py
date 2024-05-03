import tkinter as tk
from tkinter import messagebox

DISALLOWED_WORDS = ['（', '）', '(', ')', '__', '《', '》', '【', '】', '[', ']']
# 创新点自己手动输入禁词
'''
print('您可以选择输入一些禁用词，这些词将被忽略，请选择输入禁词的个数：')
NUM_DIS = input()
CINDISABLE_WORDS = []
for i in range(int(NUM_DIS)):
    print('请输入第{}个禁词：'.format(i + 1))
    a = input()
    CINDISABLE_WORDS.append(a)
DISALLOWED_WORDS = DISALLOWED_WORDS + CINDISABLE_WORDS
'''

MAX_LEN = 64
MIN_WORD_FREQUENCY = 8
BATCH_SIZE = 16
DATASET_PATH = './poetry.txt'
SHOW_NUM = 5
TRAIN_EPOCHS = 20
BEST_MODEL_PATH = './best_model.h4'


class SettingsWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Settings")

        # 创建一个用于显示背景图片的Label
        self.background_image = tk.PhotoImage(file="content.jpg")
        self.background_label = tk.Label(root, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.disallowed_entry = tk.Entry(root)
        self.disallowed_entry.pack()
        self.add_button = tk.Button(root, text="Add Disallowed Word", command=self.add_disallowed_word)
        self.add_button.pack()

        self.save_button = tk.Button(root, text="Save", command=self.save_settings)
        self.save_button.pack()

    def add_disallowed_word(self):
        word = self.disallowed_entry.get()
        if word:
            DISALLOWED_WORDS.append(word)
            messagebox.showinfo("Info", "Disallowed word added.")
            self.disallowed_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Please enter a word.")

    def save_settings(self):
        messagebox.showinfo("Info", "Settings saved.")
        self.root.destroy()


root = tk.Tk()
settings_window = SettingsWindow(root)
root.mainloop()