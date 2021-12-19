FROM openjdk:8-jdk-alpine3.9
ENV KAFKA_HOME /usr/local/kafka
ADD ./start-kafka.sh /scripts/
RUN chmod u+x -R /scripts/
WORKDIR .
# install utils
RUN apk add wget --no-cache curl tar bash procps
# install kafka
RUN wget https://ftp.wayne.edu/apache/kafka/3.0.0/kafka_2.13-3.0.0.tgz && \
tar -xzf kafka_2.13-3.0.0.tgz && \
mv kafka_2.13-3.0.0 $KAFKA_HOME
 
EXPOSE 9092
ENTRYPOINT ["/scripts/start-kafka.sh"]