## <p align='center'>拼写纠错</p>

### 原理介绍

拼写纠错的原理就是对一个特定的词w，找出他最可能的正确形式。（这里存在一个问题就是如何判断这个词是错误的，为了简单起见，就将没有出现在词典中的词看作是错误的。）因此拼写纠错的任务就是从所有的候选集中找出概率最大的正确形式，记为c。使用数学的方式表示为：
$$
\operatorname{arg\max}_{c\in \text {candidates}} \mathrm{P(c|w)}
$$
使用贝叶斯公式可以将上式转化为：
$$
\operatorname{arg\max}_{c\in \text {candidates}} \mathrm{P(c)}\mathrm{P(w|c)}/\mathrm{P(w)}
$$
因为对于候选集中的元素来说，$\mathrm{P(w)}$是相同的，因此可以忽略，故最后要求的目标为：
$$
\operatorname{arg\max}_{c\in \text {candidates}} \mathrm{P(c)}\mathrm{P(w|c)}
$$
这个表达式包含了四个部分：

- Selection Mechanism：argmax，即选择能使得该组合概率最大的candidate
- Candidate Model：$c \in candidates$，明确哪些是需要考虑的
- Language Model：P(c)。这里使用语言模型是为了使得纠正之后的词语c更符合语境
- Error Model：P(w|c)，表示正确的词语c被写作w的概率。如P(teh|the)的概率明显会大于P(theeexyz|the)的概率

对于这个表达式的直观理解就是对于一个写错的w，要综合考虑可能是要打哪个c和这个c是否符合当前上下文语境。

### 具体实现

接着是对这四个部分的具体实现。

#### Selection Mechanism

选择机制只需要使用python的内置函数argmax即可

#### Candidate Model

Candidate Model是指错误的w真是想要表达的c，因此c是又w通过

- deletion：删除一个字符
- transposition：交换两个相邻的字符
- replacement：替换一个字符
- insertion：在字符中间添加一个字符

得到的，通常使用**编辑距离(edit distance)**来衡量这几种操作。

在这里我们通过已知的w来通过若干次变换得到c。基本函数为：

```python
def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)
```

得到的结果再调用一次edits1即可得到两次变化后的集合(也有可能变换为原始集合)。

这里需要注意的地方是最后返回的是一个**set而不是list**，set在某些情况下可以加速查找速度。list的查找是线性的，而set的查找在某些情况下是log(N)的。

这并没有完成我们所需要的编辑结果，这里需要对返回的结果进行过滤，因为在上文中我们假设错误的单词是词典中没有的单词，因此在这里我们将得到的集合中字典没有出现过的单词过滤出去，这样会大大减少原来的集合。

#### Language Model



#### Error Model





### 进一步的改进





#### 





### 参考

[编辑距离算法实现](https://www.geeksforgeeks.org/edit-distance-dp-5/)

[拼写纠错简单实现](https://norvig.com/spell-correct.html)

[paper1](http://static.googleusercontent.com/media/research.google.com/en/us/pubs/archive/36180.pdf)

[paper2](http://citeseerx.ist.psu.edu/viewdoc/download;jsessionid=52A3B869596656C9DA285DCE83A0339F?doi=10.1.1.146.4390&rep=rep1&type=pdf)

