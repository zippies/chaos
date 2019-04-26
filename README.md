#### start up

##### 文件结构


    chaos 
    ├── Dockerfile          -- [文件]构建docker镜像文件
    ├── README.md           -- [文件]使用说明文档
    ├── agent.py            -- [文件]jmeter进行分布式压测时，启动肉鸡的程序
    ├── app                 -- [目录]应用主目录
    │   ├── __init__.py
    │   ├── controllers     -- [目录]定义了所有对外接口(api)
    │   │   ├── __init__.py
    │   │   ├── agentController.py
    │   │   ├── analysisController.py
    │   │   ├── casController.py
    │   │   ├── localController.py
    │   │   ├── machineController.py
    │   │   ├── missionController.py
    │   │   ├── monitorController.py
    │   ├── models.py       -- 定义了所有数据库对象
    │   ├── services        -- [目录]定义了所有公共方法和内外部交互方法
    │   │   ├── __init__.py
    │   │   ├── agentService.py
    │   │   ├── commonService.py
    │   │   ├── horn
    │   │   │   ├── __init__.py
    │   │   │   ├── executor.py
    │   │   ├── missionService.py
    │   ├── static          -- [目录]存放所有静态资源文件和测试报告文件
    │   │   ├── debug_detail
    │   │   ├── imgs
    │   │   ├── js
    │   │   │   └── main.js
    │   │   ├── nmon_files
    │   │   └── reports
    │   └── templates       -- [目录]存放所有前端html模板文件
    │       ├── addMission.html
    │       ├── analyze.html
    │       ├── base.html
    │       ├── login.html
    │       ├── machines.html
    │       ├── missions.html
    ├── bin                 -- [目录]nmon执行程序
    │   ├── ksh
    │   ├── nmon
    │   └── nmonchart
    ├── code_templates      -- [目录]定义压测工具脚本模板
    │   ├── __init__.py
    ├── configer.py         -- [文件]配置类
    ├── chaos.cfg        -- [文件]主配置文件 -- 【重要】
    ├── db                  -- [目录]sqlite数据库存储目录
    ├── gatling2.2.4        -- [目录]gatling压测工具
    ├── gunicorn.py         -- [文件]gunicorn配置文件
    ├── lib                 -- [目录]非第三方本地函数库
    ├── logs                -- [目录]日志
    ├── manager.py          -- [文件]主启动程序
    ├── requirements.txt    -- [文件]pip依赖库列表
    ├── start.sh            -- [文件]主启动脚本
    ├── tasks.py            -- [文件]celery任务脚本
    └── update_image.sh     -- [文件]镜像构建脚本
    
#### 启动方式

##### 一、根据需要修改配置文件config.py


##### 二、单机模式

    执行启动脚本: ./start.sh 

##### 三、jmeter分布式模式

    1. 单机模式启动一个节点作为master节点

    2. agent机器上修改配置文件chaos.cfg中的agent_tag设置为任意字符串，注意:不同的agent需要设置不同的agent_tag值

    3. agent机器上执行启动脚本: ./start.sh

    agent机器启动后

    #### 调用 http://{agent_host}:8080/agent/start 启动agent
    #### 调用 http://{agent_host}:8080/agent/stop  停止slave
    #### 调用 http://{master_host}:8080/agent/list 查看活跃可用的agent列表

