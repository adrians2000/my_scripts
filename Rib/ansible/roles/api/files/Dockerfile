FROM centos:6.8
COPY ./api.py /tmp/
RUN yum -y install epel-release && yum clean all
RUN yum -y install python-pip && yum clean all
RUN pip install flask
ENTRYPOINT ["python"]
CMD ["/tmp/api.py"]