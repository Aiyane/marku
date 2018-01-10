

# 认识与入门 Markdown

> [Markdown](http://zh.wikipedia.org/wiki/Markdown)是一种轻量级的【标记语言】，它的优点很多，目前也被越来越多的写作爱好者，撰稿者广泛使用。看到这里请不要被【标记】、语言所迷惑，Markdown的语法十分简单。常用的标记符号也不超过十个，这种相对于更为复杂的HTML标记语言来说，Markdown可谓是十分轻量级的，学习成本也不需要太多，且一旦熟悉这种语法规则，会有一劳永逸的效果。


## 认识 Markdown 

在刚才的导语里提到的，Markdown是一种用来写作的轻量级\[ 标记语言\] ，它用简洁的语法代替排版，而不是一般我们用的字处理软件_word_或*Pages*有大量的排版、字体设置。它使我们专心于码字，用\[标记\]语法,来代替常见的排版格式。例如此文从内容到格式，甚至插图，键盘就可以统统搞定了。目前来看，支持Markdown语法的编译器有很多，包括很多网站（例如[简书](http://www.jianshu.com/)）也支持了Markdown的文字录入，Markdown从写法到完成，导出格式随心所欲，你可以导出HTML格式的文件用来网站发布，也可以十分方便的导出PDF格式，这种格式写出来的简历更能得到HR的好感。甚至可以利用[CloudApp](https://www.getcloudapp.com/)这种云服务器工具直接上传至网页用来分享你的文章，全球最大的轻博客平台Tumblr，也支持使用Mou这类Markdown工具进行编辑并直接上传。

### Markdown 官方文档 ##

> 这里可以看到官方的Markdown语法规则文档，当然，后文我也会用自己的方式，阐述这些语法在实际使用中的用法。

* [创始人John Gruber 的Markdown语法说明](http://daringfireball.net/projects/markdown/syntax)
* [Markdown 中文版语法说明](http://wowubuntu.com/markdown/#list)

### 使用Markdown的优点

* 专注你的文字内容而不是排版样式。
* 轻松的导出HTML、PDF和本身的.md文件。
* 纯文本内容，兼容所有的文本编辑器与文字处理软件。
* 可读，直观。适合所有人的写作语言。

### 我该用什么工具？

![Mou icon](https://cdn.sspai.com/attachment/origin/2014/04/15/69488.png)

#### Mac 平台

* 在Mac OS X 上，我强烈建议你用[Mou](http://25.io/mou/)这款免费且十分好用的Markdown编译器，它支持实时预览，既左边是你编辑Markdown语言，右边会实时的生成预览效果，笔者文章就是Mou这款应用写出来的。

![ ](https://cdn.sspai.com/attachment/origin/2014/04/15/69489.jpg)

其实还有很多同类选择。如果你是一个编辑作者，我强烈建议你购买 [Ulysses Ⅲ](https://ulyssesapp.com/) ,这款应用入围了苹果去年Mac App Store的*The Best of 2013*，相比Mou它支持更多的写作格式、多文档的支持。Mou、iA Writer这些应用都是基于单文档的管理方式，而Ulysses Ⅲ支持 Folder、Filter的管理，一个Folder里面可以创建多个Sheet、Sheet之间还可以进行Combine处理。

![ ](https://cdn.sspai.com/attachment/origin/2014/04/15/69490.jpg)

#### windows、ios、Web平台

* 笔者并未使用过Windows下的Markdown工具，但经朋友介绍，有两款还算不错，一款叫[MarkdownPad](http://www.markdownpad.com/),另一款叫[MarkPad](http://code52.org/DownmarkerWPF/)。
* iOS端已有相当多的app支持Markdown语法编辑，例如Drafts、Day One、iA Writer等。
* Web端上，我强烈推荐[简书](http://jianshu.io/)这款产品，上面有无数热爱文字的人在不停的创造、分享。在Web端使用Markdown没有比简书更舒服的地方了，它同样支持左右左右两栏的实时预览，字体优雅、简洁。

![ ](https://cdn.sspai.com/attachment/origin/2014/04/15/69491.jpg)

* 同样是Web端，Draftin这款在线MD编辑器也近乎完美。

## Markdown 语法的简要规则

### 标题

![ ](https://cdn.sspai.com/attachment/origin/2014/04/15/69492.jpg)

标题是每篇文章都需要也是最常用的格式，在Markdown中，如果一段文字被定义为标题，只要在文字前加`#`号即可。

`# 一级标题`

`## 二级标题`

`### 三级标题`

以此类推，总共六级标题，建议在并号后加一个空格，这是最标准的Markdown语法。

### 列表

熟悉HTML的同学肯定知道有序列表与无序列表的区别，在Markdown下，列表的现实需要在文字前加上`-`或`*`即可变为无序列表，有序列表则直接在文字前加`1.` `2.` `3.`符号要和文字之间加上一个字符的空格。

![ ](https://cdn.sspai.com/attachment/origin/2014/04/15/69493.jpg)

### 引用

如果你需要引用一小段别处的句子，那么就要用引用的格式。

`>例如这样`

只需要在文本前加入	`>` 这种尖括号（大于号）即可

![ ](https://cdn.sspai.com/attachment/origin/2014/04/15/69494.jpg)

### 图片与链接

插入链接与插入图片的语法很像， 区别在一个 `!` 号
插入图片的地址需要图床，这里推荐[CloudApp](http://www.getcloudapp.com/)的服务，生成URL地址即可。

![ ](https://cdn.sspai.com/attachment/origin/2014/04/15/69495.jpg)

### 粗体与斜体

Markdown的粗体和斜体也非常简单，用两个 `*` 包含一段文本就是粗体的语法，用一个 `*` 包含一段文本就是斜体的语法。

例如：**这里是粗体***这里是斜体*

### 表单

表格是我觉得Markdown比较累人的地方，例子如下：

```
	|Tables |Are  |Cool |
 
	|-------|:----:|----:|
 
	|col 3 is|right-aligned|$1600|

	|col 2 is|centered |$12|

	|zebra stripes|are neat |$1 |
```

这种语法生成的表格如下：

|Tables        | Are           | Cool   |
|:------------:|:-------------:|:------:|
|col 3 is      | right-aligned | $1600  |
|col 2 is      | centered      |   $12  |
|zebra atripes | are neat      |  $1    |

### 代码框

如果你是个程序员，需要在文章里优雅的引用代码框，在Markdown下实现也非常简单，只需要用两个```把中间的代码包裹起来，如 `code` 。图例：

![ ](https://cdn.sspai.com/attachment/origin/2014/04/15/69496.jpg)

使用 `tab` 键即可缩进。

### 分割线

分割线的语法只需要另起一行，连续输入三个 `***` 即可。

### 小结

到这里，Markdown的基本语法在日常的使用中基本就没有什么大问题了，只要多加练习，配合好用的工具，写起东西来肯定会行云流水。更多的语法规则，其实Mou的Help文档例子很好，当你第一次使用Mou时，就会显示该文档，其次，你也可以在撰写的过程中，使用 `CMD+R` 快捷键来快速打开文档，以便随时查阅和学习语法。

![ ](https://cdn.sspai.com/attachment/origin/2014/04/15/69497.jpg)

**本篇文章为转载，请勿打赏!**
