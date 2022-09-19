## 一、修改spark-env.sh
```
cd /export/server/spark/conf
vim /export/server/spark/conf/spark-env.sh
```

```
# 添加以下内容
HADOOP_CONF_DIR=/export/server/hadoop-3.3.0/etc/hadoop/
YARN_CONF_DIR=/export/server/hadoop-3.3.0/etc/hadoop/
```

```
# 将spark-env.sh拷贝到另外2台机器
cd /export/server/spark/conf
scp -r spark-env.sh node2:$PWD
scp -r spark-env.sh node3:$PWD
```

## 二、修改hadoop的yarn-site.xml
```
cd /export/server/hadoop-3.3.0/etc/hadoop/
vim /export/server/hadoop-3.3.0/etc/hadoop/yarn-site.xml
```

```
# 要修改的内容
<?xml version="1.0"?>

<!-- 新增加的代码 -->
<configuration>

<!-- Site specific YARN configuration properties -->

<!-- Site specific YARN configuration properties -->
<!-- 设置YARN集群主角色运行机器位置 -->
<property>
        <name>yarn.resourcemanager.hostname</name>
        <value>node1</value>
</property>

<property>
    <name>yarn.nodemanager.aux-services</name>
    <value>mapreduce_shuffle</value>
</property>


    <!-- 设置yarn集群的内存分配方案 -->
    <property>
        <name>yarn.nodemanager.resource.memory-mb</name>
        <value>20480</value>
    </property>
    <property>
        <name>yarn.scheduler.minimum-allocation-mb</name>
        <value>2048</value>
    </property>
    <property>
        <name>yarn.nodemanager.vmem-pmem-ratio</name>
        <value>2.1</value>
    </property>


<!-- 是否将对容器实施物理内存限制 -->
<property>
    <name>yarn.nodemanager.pmem-check-enabled</name>
    <value>false</value>
</property>

<!-- 是否将对容器实施虚拟内存限制。 -->
<property>
    <name>yarn.nodemanager.vmem-check-enabled</name>
    <value>false</value>
</property>

<!-- 开启日志聚集 -->
<property>
  <name>yarn.log-aggregation-enable</name>
  <value>true</value>
</property>

<!-- 设置yarn历史服务器地址 -->
<property>
    <name>yarn.log.server.url</name>
    <value>http://node1:19888/jobhistory/logs</value>
</property>

<!-- 保存的时间7天 -->
<property>
  <name>yarn.log-aggregation.retain-seconds</name>
  <value>604800</value>
</property>
</configuration>
```
```
# 将yarn-site.xml拷贝到另2台机器
cd /export/server/hadoop-3.3.0/etc/hadoop
scp -r yarn-site.xml node2:$PWD
scp -r yarn-site.xml node3:$PWD
```

### 三、Spark设置历史服务地址
```
cd /export/server/spark/conf
cp spark-defaults.conf.template spark-defaults.conf
vim spark-defaults.conf
```
```
# 添加以下内容:
spark.eventLog.enabled                  true
spark.eventLog.dir                      hdfs://node1:8020/sparklog/
spark.eventLog.compress                 true
spark.yarn.historyServer.address        node1:18080
```
```
cd /export/server/spark/conf
cp log4j.properties.template log4j.properties
vim log4j.properties
```
```
# 修改为以下内容
log4j.rootCategory=WARN, console
```
```
# 将spark-defaults.conf log4j.properties拷贝到另2台机器
cd /export/server/spark/conf
scp -r spark-defaults.conf log4j.properties node2:$PWD
scp -r spark-defaults.conf log4j.properties node3:$PWD
```

### 四、配置依赖spark jar包
```
hadoop fs -mkdir -p /spark/jars/
hadoop fs -put /export/server/spark/jars/* /spark/jars/
```

```
cd /export/server/spark/conf
vim spark-defaults.conf
```

```
# 添加以下内容:
spark.yarn.jars  hdfs://node1:8020/spark/jars/*
```

```
cd /export/server/spark/conf
scp -r spark-defaults.conf root@node2:$PWD
scp -r spark-defaults.conf root@node3:$PWD
```

### 五、启动服务
```
start-dfs.sh
start-yarn.sh
mr-jobhistory-daemon.sh start historyserver
/export/server/spark/sbin/start-history-server.sh
```

### Configuring Logging
>Spark uses log4j for logging. You can configure it by adding a log4j2.properties file in the conf directory. One way to start is to copy the existing log4j2.properties.template located there.


### Overriding configuration directory
>To specify a different configuration directory other than the default “SPARK_HOME/conf”, you can set SPARK_CONF_DIR. Spark will use the configuration files (spark-defaults.conf, spark-env.sh, log4j2.properties, etc) from this directory.
---
### Inheriting Hadoop Cluster Configuration

If you plan to read and write from HDFS using Spark, there are two Hadoop configuration files that should be included on Spark’s classpath:

* hdfs-site.xml, which provides default behaviors for the HDFS client.
* core-site.xml, which sets the default filesystem name.

The location of these configuration files varies across Hadoop versions, but a common location is inside of /etc/hadoop/conf. Some tools create configurations on-the-fly, but offer a mechanism to download copies of them.

To make these files visible to Spark, set HADOOP_CONF_DIR in $SPARK_HOME/conf/spark-env.sh to a location containing the configuration files.

---
### Custom Hadoop/Hive Configuration
If your Spark application is interacting with Hadoop, Hive, or both, there are probably Hadoop/Hive configuration files in Spark’s classpath.

Multiple running applications might require different Hadoop/Hive client side configurations. You can copy and modify hdfs-site.xml, core-site.xml, yarn-site.xml, hive-site.xml in Spark’s classpath for each application. In a Spark cluster running on YARN, these configuration files are set cluster-wide, and cannot safely be changed by the application.

The better choice is to use spark hadoop properties in the form of spark.hadoop.*, and use spark hive properties in the form of spark.hive.*. For example, adding configuration “spark.hadoop.abc.def=xyz” represents adding hadoop property “abc.def=xyz”, and adding configuration “spark.hive.abc=xyz” represents adding hive property “hive.abc=xyz”. They can be considered as same as normal spark properties which can be set in $SPARK_HOME/conf/spark-defaults.conf

In some cases, you may want to avoid hard-coding certain configurations in a SparkConf. For instance, Spark allows you to simply create an empty conf and set spark/spark hadoop/spark hive properties.

```
val conf = new SparkConf().set("spark.hadoop.abc.def", "xyz")
val sc = new SparkContext(conf)
```
Also, you can modify or add configurations at runtime:

```
./bin/spark-submit \ 
  --name "My app" \ 
  --master local[4] \  
  --conf spark.eventLog.enabled=false \ 
  --conf "spark.executor.extraJavaOptions=-XX:+PrintGCDetails -XX:+PrintGCTimeStamps" \ 
  --conf spark.hadoop.abc.def=xyz \
  --conf spark.hive.abc=xyz
  myApp.jar

```