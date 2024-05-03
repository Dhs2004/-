import numpy as np
import settings


def generate_random_poetry(tokenizer, model, s=''):
    """
    随机生成一首诗
    :param tokenizer: 分词器
    :param model: 用于生成古诗的模型
    :param s: 用于生成古诗的起始字符串，默认为空串
    :return: 一个字符串，表示一首古诗
    """
    # 将初始字符串转成token
    token_ids = tokenizer.encode(s)
    # 去掉结束标记[SEP]
    token_ids = token_ids[:-1]
    while len(token_ids) < settings.MAX_LEN:
        # 进行预测，只保留第一个样例（我们输入的样例数只有1）的、最后一个token的预测的、不包含[PAD][UNK][CLS]的概率分布
        output = model(np.array([token_ids, ], dtype=np.int32))
        #0表示第一个样例（很明显，我们就只有一个样例），-1表示最后一个预测序列，3：表示取从第三个开始的元素（省去了0,1,2）
        #保留了对于结束标志的预测（SEP）
        _probas = output.numpy()[0, -1, 3:]
        del output
        #print(_probas)
        # 按照出现概率，对所有token倒序排列
        #通过argsort函数对_probas进行从小到大排序，使用[::-1]将排序结果翻转，得到的是从大到小排序的结果。取其前100个预测结果。
        #这里返回的是值从大到小的索引数组。
        """
        先进行索引根据概率大小进行排序，再进行概率的排序"""
        p_args = _probas.argsort()[::-1][:100]
        # 排列后的概率顺序
        #p =sorted(_probas,reverse=True)[:100]这样花费的时间较多
        p=_probas[p_args]
        # 先对概率归一
        p = p / sum(p)
        # 再按照预测出的概率，随机选择一个词作为预测结果
        target_index = np.random.choice(len(p), p=p)
        target = p_args[target_index] + 3
        # 保存
        token_ids.append(target)
        if target == 3:
            break
    return tokenizer.decode(token_ids)


def generate_acrostic(tokenizer, model, head):
    """
    随机生成一首藏头诗
    :param tokenizer: 分词器
    :param model: 用于生成古诗的模型
    :param head: 藏头诗的头
    :return: 一个字符串，表示一首古诗
    """
    # 使用空串初始化token_ids，加入[CLS]
    token_ids = tokenizer.encode('')
    token_ids = token_ids[:-1]
    # 标点符号，这里简单的只把逗号和句号作为标点
    punctuations = ['，', '。']
    punctuation_ids = {tokenizer.token_to_id(token) for token in punctuations}
    # 缓存生成的诗的list
    poetry = []
    # 对于藏头诗中的每一个字，都生成一个短句
    for ch in head:
        # 先记录下这个字
        poetry.append(ch)
        # 将藏头诗的字符转成token id
        token_id = tokenizer.token_to_id(ch)
        # 加入到列表中去
        token_ids.append(token_id)
        # 开始生成一个短句
        while True:
            # 进行预测，只保留第一个样例（我们输入的样例数只有1）的、最后一个token的预测的、不包含[PAD][UNK][CLS]的概率分布
            output = model(np.array([token_ids, ], dtype=np.int32))
            _probas = output.numpy()[0, -1, 3:]
            del output
            # 按照出现概率，对所有token倒序排列
            p_args = _probas.argsort()[::-1][:100]
            # 排列后的概率顺序
            p = _probas[p_args]
            # 先对概率归一
            p = p / sum(p)
            # 再按照预测出的概率，随机选择一个词作为预测结果
            target_index = np.random.choice(len(p), p=p)
            target = p_args[target_index] + 3
            # 保存
            token_ids.append(target)
            # 只有不是特殊字符时，才保存到poetry里面去
            if target > 3:
                poetry.append(tokenizer.id_to_token(target))
            if target in punctuation_ids:
                break

    return ''.join(poetry)