Spark provides three locations to configure the system:

* Spark properties control most application parameters and can be set by using a SparkConf object, or through Java system properties.
* Environment variables can be used to set per-machine settings, such as the IP address, through the conf/spark-env.sh script on each node.
* Logging can be configured through log4j2.properties.

---

>Spark properties control most application settings and are configured separately for each application. These properties can be set directly on a SparkConf passed to your SparkContext. SparkConf allows you to configure some of the common properties (e.g. master URL and application name), as well as arbitrary key-value pairs through the set() method.

---
>In some cases, you may want to avoid hard-coding certain configurations in a SparkConf. For instance, if you’d like to run the same application with different masters or different amounts of memory. Spark allows you to simply create an empty conf:

```
val sc = new SparkContext(new SparkConf())
```
Then, you can supply configuration values at runtime:

```
./bin/spark-submit --name "My app" \
                   --master local[4] \
                   --conf spark.eventLog.enabled=false \
                    myApp.jar

```

---
> The Spark shell and spark-submit tool support two ways to load configurations dynamically. The first is command line options, such as --master, as shown above. spark-submit can accept any Spark property using the --conf/-c flag, but uses special flags for properties that play a part in launching the Spark application. Running ./bin/spark-submit --help will show the entire list of these options.

>bin/spark-submit will also read configuration options from conf/spark-defaults.conf, in which each line consists of a key and a value separated by whitespace. For example:

```
spark.master            spark://5.6.7.8:7077
spark.executor.memory   4g
spark.eventLog.enabled  true
spark.serializer        org.apache.spark.serializer.KryoSerializer
```

---
>Any values specified as flags or in the properties file will be passed on to the application and merged with those specified through SparkConf. Properties set directly on the SparkConf take highest precedence, then flags passed to spark-submit or spark-shell, then options in the spark-defaults.conf file. 

---
>Spark properties mainly can be divided into two kinds: one is related to deploy, like “spark.driver.memory”, “spark.executor.instances”, this kind of properties may not be affected when setting programmatically through SparkConf in runtime, or the behavior is depending on which cluster manager and deploy mode you choose, so it would be suggested to set through configuration file or spark-submit command line options; another is mainly related to Spark runtime control, like “spark.task.maxFailures”, this kind of properties can be set in either way.

### Viewing Spark Properties
>The application web UI at http://<driver>:4040 lists Spark properties in the “Environment” tab. This is a useful place to check to make sure that your properties have been set correctly. Note that only values explicitly specified through spark-defaults.conf, SparkConf, or the command line will appear. For all other configuration properties, you can assume the default value is used.

---

### Environment Variables

> Certain Spark settings can be configured through environment variables, which are read from the conf/spark-env.sh script in the directory where Spark is installed (or conf/spark-env.cmd on Windows).

>Note that conf/spark-env.sh does not exist by default when Spark is installed. However, you can copy conf/spark-env.sh.template to create it. Make sure you make the copy executable.


| Environment Variable	 | Meaning |
| :-----| :---- | 
| JAVA_HOME | Location where Java is installed (if it's not on your default PATH).
 | 
| PYSPARK_PYTHON | Python binary executable to use for PySpark in both driver and workers (default is python3 if available, otherwise python). Property spark.pyspark.python take precedence if it is set
 | 
 |PYSPARK_DRIVER_PYTHON|Python binary executable to use for PySpark in driver only (default is PYSPARK_PYTHON). Property spark.pyspark.driver.python take precedence if it is set
|
|SPARKR_DRIVER_R|R binary executable to use for SparkR shell (default is R). Property spark.r.shell.command take precedence if it is set
|
|SPARK_LOCAL_IP	|IP address of the machine to bind to.
|
|SPARK_PUBLIC_DNS	|Hostname your Spark program will advertise to other machines.
|

>Note: When running Spark on YARN in cluster mode, environment variables need to be set using the spark.yarn.appMasterEnv.[EnvironmentVariableName] property in your conf/spark-defaults.conf file. Environment variables that are set in spark-env.sh will not be reflected in the YARN Application Master process in cluster mode. See the YARN-related Spark Properties for more information.

