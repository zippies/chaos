FROM centos:latest

RUN yum reinstall -y glibc-common && yum -y install openssh-clients python-setuptools \
    python-devel gcc zlib readline readline-devel readline-static openssl openssl-devel openssl-static sqlite-devel bzip2-devel bzip2-libs libffi libffi-devel zlib-devel libssl-dev&& \
    yum clean all

ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8

RUN easy_install -i http://mirrors.aliyun.com/pypi/simple/ pip

ENV JAVA_HOME /data/program/java
ENV PATH $JAVA_HOME/bin:$PATH

# notice: you should download java8.tar.gz file first,and put it under current file dir
ADD java8.tar.gz /data/program

RUN ln -sf /data/program/jdk1.8.0_171 /data/program/java

RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
  && echo 'Asia/Shanghai' > /etc/timezone

COPY . /data/program/chaos/

WORKDIR /data/program/chaos

# notice: if you have pip source of your own, replace the code below
RUN pip install -r requirements.txt -i http://pypi.douban.com/simple --trusted-host=pypi.douban.com --ignore-installed ipaddress

EXPOSE 8080

CMD ["./start.sh"]
