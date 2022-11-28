# WYYMusicSentimentClassificationPublic

### 使用方式

#### 以下项目均需先安装依赖环境、数据库
**MongoDB数据安装：**

参考连接（Mac：https://blog.csdn.net/weixin_45406712/article/details/121235190
centos：https://juejin.cn/post/6844903828811153421；）

**python依赖安装：**

① 查看Dockerfile所需的python版本 ② 安装依赖库：pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

**vue依赖安装**

@vue/cli 4.5.15、node@v16.13.2、npm@8.1.2、vue@2.6.10
命令行执行：npm install
启动：npm run serve

> 1. WWYScrapy：① 修改setting.py数据库配置。② 修改配置GROUP_IDS、spiders文件夹下py文件的数据过滤（可选）
> 2. WYYDataAnalysis：① 修改dataBase/mongodb.py的数据库配置
> 3. WYYFastAPI：① 修改.env.dev的数据库配置
> 4. WYYVueFront：① 修改src/api/request.js中baseURL（即后端接口地址） ②vue.config.js解决跨域问题

### 部署
可参考Jenkinsfile、Dockerfile

### 项目实现
主要步骤：数据爬虫-> 数据清洗及统计分析 -> 后端接口 -> 前端展示 -> 页面交互（提供数据手动标注功能） -> 模型训练

### 主要技术
```text
爬虫：Scrapy MongoDB
数据分析：jieba pandas
后端：FastApi
前端：Vue Echarts ElementUI
部署：docker jenkins
情感二分类：Python Bert
```

### 参考资料
> 爬虫：https://github.com/sujiujiu/WYYScrapy
> 
> 后端：https://github.com/Youngestdev/fastapi-mongo
> 
> 前端：https://github.com/lin-xin/vue-manage-system/tree/V4.2.0

### 项目预览
地址：http://120.25.163.240:8002/