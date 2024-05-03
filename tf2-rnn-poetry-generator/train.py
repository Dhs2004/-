import tensorflow as tf
from dataset import PoetryDataGenerator, poetry, tokenizer
from model import model
import settings
import utils
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import jieba
import matplotlib.font_manager as fm


class Evaluate(tf.keras.callbacks.Callback):
    """
    在每个epoch训练完成后，保留最优权重，并随机生成settings.SHOW_NUM首古诗展示
    """

    def __init__(self):
        super().__init__()
        # 给loss赋一个较大的初始值
        self.lowest = 1e10

    def on_epoch_end(self, epoch, logs=None):
        # 在每个epoch训练完成后调用
        # 如果当前loss更低，就保存当前模型参数
        if logs['loss'] <= self.lowest:
            self.lowest = logs['loss']
            model.save(settings.BEST_MODEL_PATH)
        # 随机生成几首古体诗测试，查看训练效果
        for i in range(settings.SHOW_NUM):
            generated_poetry = utils.generate_random_poetry(tokenizer, model)
            print(generated_poetry)
            generate_word_cloud(generated_poetry)


def generate_word_cloud(poetry):
    # 生成词云图
    text = " ".join(jieba.cut(poetry))
    font_path = fm.findfont(fm.FontProperties(family="SimHei"))  # 查找中文字体文件路径
    wordcloud = WordCloud(font_path=font_path, background_color='white').generate(text)

    plt.figure(figsize=(8, 8), dpi=80)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()


# 创建数据集
data_generator = PoetryDataGenerator(poetry, random=True)
# 开始训练
model.fit_generator(data_generator.for_fit(), steps_per_epoch=data_generator.steps, epochs=settings.TRAIN_EPOCHS,
                    callbacks=[Evaluate()])