<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=default"></script>

## <p align='center'>NLP-文法与自动机</p>

### 乔姆斯基4型文法

文法（grammer）G一般使用一个四元组表示：
$$
G=(V,T,P,S)
$$
其中：

- V-变量（variable）的非空有穷集。
- T-终极符（terminal）的非空有穷集
- P-产生式（production）的非空有穷集
- S-S属于V，文法G的开始符号（start symbol）

**四种文法主要是通过production的左侧和右侧来进行区分**

- 0型文法（Phrase Structure Grammar，PSG）

  Production: $\alpha\rightarrow\beta$

  其中 $\alpha$ 为$(V+T)^*V(V+T)^ *$，*代表可以包含空字符串， $\beta$ 为$(V+T)^ *$。

  也就是说0型语法只要求production左边包含至少一个变量。对右边没有要求。

- 1型文法（Context Sensitive Grammar，CSG）

  Production: $\alpha\rightarrow\beta$

  首先1型文法都是0型文法，在0型文法的基础上增加约束$|\alpha|<=|\beta|$。其中||表示长度。

  对于 $\beta$ 没有限制。

- 2型文法（Context Free Grammar，CFG）

  Production: $\alpha\rightarrow\beta$

  首先2型文法都是1型文法，在1型文法的基础上满足条件$|\alpha|=1$。因为左边必须满足至少包含一个变量，因此2型文法的左边其实就是一个变量。

- 3型文法（Regular Grammar，RG）

  最后的3型文法则是在2型文法的基础上对右边进行限制。右边只能有两种形式：

  - $VT^ */T^*$（左线性文法）
  - $T^ */T^*V$（右线性文法）

  **左线型文法和右线型文法是等价的**

四种文法的关系

![](./pics/Chomsky.png)

### 有限自动机与正则文法



### 下推自动机与上下文无关文法



### 自动机的应用

