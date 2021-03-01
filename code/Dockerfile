FROM YourBaseDockerImage:last

COPY . /opt/projects/drf_template

WORKDIR /opt/projects/drf_template

RUN pip3 install -r requirements.txt --timeout=300 -i https://pypi.tuna.tsinghua.edu.cn/simple

EXPOSE 8000 8001

CMD ["sh", "./entrypoint.sh"]
