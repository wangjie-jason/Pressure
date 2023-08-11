# Pressure

## 准备Python环境

- 安装Python>=3.10
- 安装依赖
    - pip3 install -r requirements.txt
- 安装vue环境(最好是不通过下方命令，自己手动安装，避免重复安装)
    - sh vue_requirements.sh

## 首次启动项目

- 初始化及打包前端项目(在前端项目v_pressure目录下执行下方命令)
- 注：如果该目录为空，需要在github上将前端v_pressure项目down下来后，将里面的内容复制到该目录下
    - 下载前端依赖
      ```
      npm install
      注：执行完后v_pressure目录下会新增node_modules目录，即代表成功
      ```

    - 打包前端项目
      ```
      npm run build
      注：执行完后v_pressure目录下会新增dist目录，即代表成功
      ```

- 初始化后端服务（在项目根目录下即Pressure目录下执行下方命令）
    - 启动后端服务
      ```
      python3 manage.py runserver
      ```
    - 创建后台数据库
      ```
      python manage.py migrate
      ```

    - 创建超级管理员
      ```
      manage.py createsuperuser
      ```

    - 启动消息队列中间件（不使用下面命令，手动执行下项目里面的task_mq.py也行）
      ```
      python3 /Users/wangjie/Pressure/MyApp/task_mq.py
      注：想用几个队列就启动几次（正常启动1个即可，可以理解为施压机，启动一个就代表所有的消息都在一个队列里处理，启动多个就代表多个队列同时处理消息）
      ```
- 首次启动项目后，后续再启动项目只需要执行"启动后端服务"和"启动消息队列中间件"的命令即可

## 项目结构

![img.png](img.png)