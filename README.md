# syosetu_downloader
## 简介
一个用于批量下载小说网站“syosetu”内容的命令行工具，支持下载与导出翻译任务、导入翻译，方便离线阅读。

## License
![GNU AGPL Version 3 Logo](https://www.gnu.org/graphics/agplv3-with-text-162x68.png)

syosetu_downloader 是自由软件，遵循`Affero GNU 通用公共许可证第 3 版或任何后续版本`。你可以自由地使用、修改和分发该软件，但不提供任何明示或暗示的担保。有关详细信息，请参见 [Affero GNU 通用公共许可证](https://www.gnu.org/licenses/agpl-3.0.html)。

## 安装依赖
```bash
pip install -r requirements.txt
```

## 使用示例
```bash
# 这里演示的是大致流程，实际可能需要调整，不过一般照着这个来就行了
# 下载章节
python3 download.py n2267be --proxy socks5h://127.0.0.1:1080 # 中国大陆特供代理（注意，这里是`socks5h`，按照经验，不要少了个`h`）

# 导出章节为翻译任务
python3 export_chapters.py

# 翻译（人工翻译，或者用tktransl翻译）
...

# 导入翻译
# 复制翻译结果到`translated`文件夹
cp -r /path/to/translated ./translated

# 将翻译结果应用到原文
python3 apply_translation.py

# 然后，翻译后的结果就储存在`results`文件夹了
```

## 注意事项
- 如果你不需要翻译，就只看下载章节那步就好了
- 建议搭配和[tktransl](https://2git.xyz/thiliapr/tktransl)一起使用。

## 文档
文档是不可能写的，这辈子都不可能写的。经验表明，写了文档只会变成“代码一天一天改，文档一年不会动”的局面，反而误导人。

所以我真心推荐：有什么事直接看代码（代码的注释和函数的文档还是会更新的），或者复制代码问ai去吧（记得带上下文）。

## 贡献与开发
欢迎提出问题、改进或贡献代码。如果有任何问题或建议，您可以在 GitHub 上提 Issues，或者直接通过电子邮件联系开发者。

## 联系信息
如有任何问题或建议，请联系项目维护者 thiliapr。
- Email: thiliapr@tutanota.com

# 无关软件本身的广告
## Join the Blue Ribbon Online Free Speech Campaign!
![Blue Ribbon Campaign Logo](https://www.eff.org/files/brstrip.gif)

支持[Blue Ribbon Online 言论自由运动](https://www.eff.org/pages/blue-ribbon-campaign)！  
你可以通过向其[捐款](https://supporters.eff.org/donate)以表示支持。

## 支持自由软件运动
为什么要自由软件: [GNU 宣言](https://www.gnu.org/gnu/manifesto.html)

你可以通过以下方式支持自由软件运动:
- 向非自由程序或在线敌服务说不，哪怕只有一次，也会帮助自由软件。不和其他人使用它们会帮助更大。进一步，如果你告诉人们这是在捍卫自己的自由，那么帮助就更显著了。
- [帮助 GNU 工程和自由软件运动](https://www.gnu.org/help/help.html)
- [向 FSF 捐款](https://www.fsf.org/about/ways-to-donate/)
