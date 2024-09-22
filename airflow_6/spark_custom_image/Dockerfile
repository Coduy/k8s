FROM bitnami/spark:3.5.0

# Install required Python packages
RUN pip install numpy==1.24.3
RUN pip install pyspark prophet scikit-learn 
RUN pip install fsspec pyarrow requests

ENV SPARK_HOME=/opt/bitnami/spark
ENV PATH=$SPARK_HOME/bin:$PATH

EXPOSE 7077 8080

# Start Spark master
CMD ["/opt/bitnami/scripts/spark/run.sh"]
