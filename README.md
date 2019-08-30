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

1. **预处理**：建议图片压缩一下，**不要展示原图**:warning:，否则网页加载缓慢。
2. clone到本地，然后在`images`文件夹内添加图片。
3. 在`_data/photos.yml`文件内添加对应图片文件的描述、日期、主题色