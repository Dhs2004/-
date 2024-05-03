import tkinter as tk
import pyttsx3
from PIL import ImageTk, Image
import tensorflow as tf
from dataset import tokenizer
import settings
import utils


def generate_poetry():
    # 加载训练好的模型
    model = tf.keras.models.load_model("./best_model.h5")

    # 清空输出文本框
    output_text.delete("1.0", tk.END)

    # 获取生成类型的选择
    selected_option = option_var.get()

    if selected_option == 1:  # 生成藏头诗
        acrostic_head = input_entry.get()
        generated_poetry = utils.generate_acrostic(tokenizer, model, head=acrostic_head)
    elif selected_option == 2:  # 以输入为开头生成诗词
        input_text = input_entry.get()
        generated_poetry = utils.generate_random_poetry(tokenizer, model, s=input_text)
    else:  # 随机生成诗词
        generated_poetry = utils.generate_random_poetry(tokenizer, model)

    # 在输出文本框中显示生成的诗词
    output_text.insert(tk.END, generated_poetry)

    # 使用pyttsx3库将生成的诗词读出来
    engine = pyttsx3.init()
    engine.say(generated_poetry)
    engine.runAndWait()


def close_window():
    window.destroy()


# 创建主窗口
window = tk.Tk()
window.title("诗歌生成器")

# 设置背景图片
background_image = ImageTk.PhotoImage(Image.open("backgroud_image.png"))
background_label = tk.Label(window, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# 创建输入框和标签用于输入诗词或藏头诗头部
input_label = tk.Label(window, text="请输入诗词或藏头诗头部：", bg='white')
input_label.pack()
input_entry = tk.Entry(window, highlightbackground='white')
input_entry.pack()

# 创建生成类型的选择框
option_var = tk.IntVar()
option_random = tk.Radiobutton(window, text="随机生成", variable=option_var, value=0)
option_acrostic = tk.Radiobutton(window, text="生成藏头诗", variable=option_var, value=1)
option_input = tk.Radiobutton(window, text="以输入为开头生成诗词", variable=option_var, value=2)
option_random.pack()
option_acrostic.pack()
option_input.pack()

# 创建生成按钮
generate_button = tk.Button(window, text="生成", command=generate_poetry)
generate_button.pack()

# 创建文本框用于显示生成的诗歌
output_text = tk.Text(window, bg='white', bd=0, highlightthickness=0, highlightbackground='white', height=2, width=50)
output_text.pack()

# 将文本框背景设置为透明
output_text.configure(inactiveselectbackground=output_text.cget("background"))

# 创建关闭按钮
close_button = tk.Button(window, text="关闭", command=close_window)
close_button.pack()

# 运行主循环
window.mainloop()