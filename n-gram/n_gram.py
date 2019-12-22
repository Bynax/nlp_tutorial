# -*- coding: utf-8 -*-
# Created by bohuanshi on 2019/9/21

from nltk.corpus import reuters
import numpy as np


def edits1(word):
    """
    给定一个单词生成编辑距离为1的所有单词
    :param word:
    :return:
    """
    # insert时用到
    letters = 'abcdefghijklmnopqrstuvwxyz'

    word_length = len(word)
    splits = [(word[:i], word[i:]) for i in range(word_length + 1)]

    # insert
    inserts = [L + c + R for L, R in splits for c in letters]

    # delete
    deletes = [L + R[1:] for L, R in splits if R]

    # replace
    replacements = [L + c + R[1:] for L, R in splits if R for c in letters]

    # transposes
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    return set(inserts + deletes + transposes + replacements)


def edit2(word):
    """
    给定单词返回编辑距离为2的词
    :param word
    """
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))


def generate_candidates(word, vocab):
    """
    给定单词返回对应的候选集合
    即编辑距离为1且在词典中出现的词语集合
    :param word
    :param vocab 词典库
    """
    candidates = edits1(word)
    return [word for word in candidates if word in vocab]


def build_gram(corpus):
    """
    构建Language Model(Bigram)
    :param corpus 语料库
    """
    term_count = {}
    bigram_count = {}
    for doc in corpus:
        doc = ['<s>'] + doc
        doc_lenght = len(doc)
        for i in range(0, doc_lenght - 1):
            term = doc[i]
            bigram = ' '.join(doc[i:i + 2])

            if term in term_count:
                term_count[term] += 1
            else:
                term_count[term] = 1
            if bigram in bigram_count:
                bigram_count[bigram] += 1
            else:
                bigram_count[bigram] = 1
    return term_count, bigram_count


# sklearn有现成的包可以使用


def error_probability(spell_error_path):
    """
    构建Error Model
    :param spell_error_path 用户拼写错误文件所在的路径
    """
    error_prob = {}
    with open(spell_error_path, encoding='utf-8') as f:
        lines = f.readlines()
    for line in lines:
        items = line.split(':')
        correct = items[0].strip()
        mistakes = [item.strip() for item in items[1].strip().split(',')]
        error_prob[correct] = {}
        mistakes_len = len(mistakes)
        for mistake in mistakes:
            error_prob[correct][mistake] = 1.0 / mistakes_len
    return error_prob


if __name__ == "__main__":
    # 加载词典
    with open('vacab.txt', encoding='utf-8')as f:
        lines = f.readlines()
    vocab = set([line.rstrip() for line in lines])

    # 预计算error_prob
    error_prob = error_probability('spell-errors.txt')

    # 预计算Language Model
    categories = reuters.categories()
    corpus = reuters.sents(categories=categories)
    term_count, bigram_count = build_gram(corpus)

    with open('textdata.txt', 'r') as f:
        lines = f.readlines()

    for line in lines:
        items = line.rstrip().split('\t')
        line = items[2].split()
        # line = ['I','Like','Playing']
        for word in line:
            # 表示错误
            if word not in vocab:
                # 生成candidates
                candidates = generate_candidates(word, vocab)

                # 计算概率
                max_prob = 0
                max_idx = 0
                prob = 0
                for idx, candidate in enumerate(candidates):
                    # 计算Error Model的概率
                    if candidate in error_prob and word in error_prob[candidate]:
                        prob += np.log(error_prob[candidate][word])
                    else:
                        prob += np.log(0.00001)
                    # 计算Language Model的概率
                    # 在这里考虑Bigram，即一个词语的p(w|w-1)和p(w+1|w)
                    V = len(term_count.keys())
                    if items[2][idx - 1] in bigram_count and candidate in bigram_count[items[2][idx - 1]]:
                        prob += np.log(
                            (bigram_count[items[2][idx]][candidate] + 1) / (term_count[items[2][idx - 1]] + V))
                    else:
                        prob += np.log(1.0 / V)

                        """
                        idx = items[2].index(word)+1
                    if items[2][idx - 1] in bigram_count and candi in bigram_count[items[2][idx - 1]]:
                        prob += np.log((bigram_count[items[2][idx - 1]][candi] + 1.0) / (
                                term_count[bigram_count[items[2][idx - 1]]] + V))
                    # TODO: 也要考虑当前 [word, post_word]
                    #   prob += np.log(bigram概率)
    
                    else:
                        prob += np.log(1.0 / V)
    
                    probs.append(prob)
                        """
                        if prob > max_prob:
                            max_prob = prob
                        max_idx = idx
                        print(word, candidates[max_idx])
