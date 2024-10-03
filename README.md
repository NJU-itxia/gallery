## 启动指南

1. 首先需要ruby环境
2. 安装jekyll, jekyll-paginate, jekyll-seo-tag

```
gem install jekyll
gem install jekyll-paginate
gem install jekyll-seo-tag
```

3. 执行`jekyll serve`运行
4. 根据提示访问目标端口，可用于本地调试
5. push到master分支即可更新

## 图库更新指南

1. 在box的gallery资料库中添加图片，文件名格式为"标题_日期_分类.XXX"。
2. 执行 `python build.py SEAFILE_TOKEN`。
3. git追踪新增图片和`_data/photos.yml`，提交修改。

建议在box里的图片做适当压缩。
