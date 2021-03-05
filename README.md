# django-rest-framework-template
久经考验的 django rest framework 项目模板

[TOC]

## 开发相关
### 常用基础 Model
- 代码位置：`code/utils/base_class.py`
- 比如附带逻辑删除以及创建时间、修改时间的 model：
```py
class LogicDeleteModel(models.Model):
    is_delete = models.BooleanField('删除标记', default=False, editable=False)

    class Meta:
        abstract = True

    # 注意，这个 delete 方法只针对单个 model 实例删除有效（比如 first_user.delete()）
    # 如果是 QuerySet 的删除，还是要使用 queryset.update(is_delete=True) 的写法
    def delete(self, using=None, keep_parents=False):
        self.is_delete = True
        self.save(update_fields=['is_delete'])

    class NotDeleteManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(is_delete=False)

    objects = NotDeleteManager()
    all_objects = models.Manager() # 需要查找被逻辑删除的数据时使用这个 all_objects
```
### 只返回查询结果的 id 集合
- 代码位置：`code/utils/database.py`
- 实际开发中会经常用到这种写法：目的是仅获取查询结果集的 id 集合
    ```py
    target_user_id_set = set(User.objects.all().values_list('id', flat=True))
    ```
    上面那个文件中简单封装了这种写法：
    ```py
    def values_list_ids(queryset: QuerySet) -> QuerySet:
        return queryset.values_list('id', flat=True)


    def values_list_ids_set(queryset: QuerySet) -> set:
        return set(values_list_ids(queryset))


    ids_set = values_list_ids_set
    ```
    此时一开始的代码就可以写成：
    ```py
    target_user_id_set = ids_set(User.objects.all())
    ```
### 字符串转 datetime 
- 代码位置：`code/utils/date_and_time.py`
- 支持年月日、年月日时分秒、秒级时间戳、毫秒级时间戳转datetime：
    ```py
    def str2datetime(s: str, format='%Y-%m-%d') -> Union[datetime, None]:
        """
        日期型字符转datetime
        """
        if isinstance(s, datetime):
            return s
        try:
            return datetime.strptime(s, format)
        except:
            pass
        try:
            return datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
        except:
            pass
        try:
            return datetime.fromtimestamp(int(s))
        except:
            pass
        try:
            return datetime.fromtimestamp(int(s) / 1000)
        except:
            pass
        return None
    ```
### 列表数据转 execl 的 BytesIO
- 代码位置：`code/utils/excel.py`，转为 BytesIO 后，可以选择保存为文件，或者作为接口响应返回
- 使用 xlwt 的方法：`generate_excel_io`，xlwt 支持保存为 xls、xlsx
- 使用 openpyxl 的方法：`generate_excel_io_by_openpyxl`，openpyxl 只支持保存为 xlsx

### 图片压缩和修改尺寸
- 代码位置：`code/utils/image.py`
- 修改图片尺寸：resize_image
- 压缩图片并修改尺寸：compress_and_resize_image
- 切图图片白边：crop_image_margin

### 中间件 middleware
- 代码位置：`code/utils/middlewares.py`
#### 前后端数据交互时驼峰和下划线参数互转
直接使用第三方库：`djangorestframework-camel-case`，配置一下在 settings 的 MIDDLEWARE，这个库只会对 body 中的参数进行转换，我写了一个对驼峰形式 get 参数转下划线的中间件：`GetParamsCamelCaseMiddleware`

#### 将 django 的响应改为 code、message、data 的形式
- `CodeMessageDataMiddleware`，这个中间件可能会影响某些第三方库的行为以及异常，比如 drf_extensions 的 cache 装饰器会报错，可以自行适配一下，我适配后的代码在 `code/utils/drf_extensions/cache/decorators.py`。
- 比起强行修改 ViewSet 的响应数据（比如封装一个自己的 ViewSet，实现 code message data 的响应），我更喜欢这种中间件可插拔形式的做法

### ViewSet 增强，以 Mixin 的形式支持多 Serializer 等功能
- 代码位置：`code/utils/mixins.py`
#### 支持多 Serializer 的优雅写法
```py
class SerializerMixin:
    def get_serializer_class(self):
        """
        让 ViewSet 支持以下写法，而不是serializer_class（这段代码来自 jumpserver 源码
        serializer_classes = {
            'default': serializers.AssetUserWriteSerializer,
            'list': serializers.AssetUserReadSerializer,
            'retrieve': serializers.AssetUserReadSerializer,
        }
        """
        serializer_class = None
        if hasattr(self, 'serializer_classes') and isinstance(self.serializer_classes, dict):
            serializer_class = self.serializer_classes.get(self.action, self.serializer_classes.get('default'))
        if serializer_class:
            return serializer_class
        return super().get_serializer_class()

    def get_request_serializer(self, *args, **kwargs):
        """
        校验请求数据并返回请求serializer
        """
        if 'data' not in kwargs:
            kwargs['data'] = self.request.data
        serializer = self.get_serializer(*args, **kwargs)
        serializer.is_valid(raise_exception=True)
        return serializer
```
然后常用的写法长这样：
```py
# user.apis.views.UserViewSet
class UserViewSet(SerializerMixin, PermissionMixin, viewsets.GenericViewSet):
    serializer_classes = {
        'default': UserMeSerializer,
        'me': UserMeSerializer,
        'create_or_update_profile': UserProfileCreateOrUpdateSerializer
    }

        @action(detail=False, methods=['POST'])
    def create_or_update_profile(self, request):
        req_serializer: UserProfileCreateOrUpdateSerializer = self.get_request_serializer()
        user_profile = req_serializer.save()
        res_serializer = UserProfileDisplaySerializer(user_profile).data
        return Response(res_serializer)
```
权限检查同理，也有一个 `PermissionMixin`

### 自定义分页器
- 代码位置：`code/utils/paginations.py`

### 获取客户端ip
- 代码位置：`code/utils/request.py`，这个函数需要 nginx 配合，否则会有漏洞（比如请求头的 X_FORWARDED_FOR 是可以客户端伪造的）
    ```
    # nginx.conf
    proxy_set_header Host $http_host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $remote_addr;
    ```

### 返回 excel 的 Response
- 代码位置：`code/utils/response.py`
- 使用的是 xlrd 库，返回了 xls 文件，这里存在优化空间，比如返回 xlsx，以及将 xlrd 换成 openpyxl。

### post 方法查询数据
- 代码位置：`utils.serializers.QuerySerializer`
- 因为 http 的 get 方法存在一些弊端，这里封装了一个 QuerySerializer，具体细节和用法可以读一下代码（个人觉得还不够完善）。

### 字符串工具方法
- 代码位置：`code/utils/strings.py`
- 字符串、float 类型转 Decimal：`str2decimal`
- 下划线转驼峰：`underline_2_hump`

### todo：添加其他用法说明

## 部署相关

### Dockerfile
- Dockerfile 文件位置：`code/Dockerfile`
- 为了提高镜像构建速度以及节约镜像层开销，建议自己构建一个基础镜像，替换 Dockerfile 中的 `YourBaseDockerImage:last`，基础镜像的写法可以参考我的另一个代码仓库：`https://github.com/ChouBaoDxs/PublicDockerfile/tree/zjkj/centos-py365`，这个 Dockerfile 使用的是 centos7 以及 python 3.6.5

### entrypoint.sh
为了让 Docker 镜像的使用更加灵活，支持部署 django、celery 以及 runscript，通过在 `entrypoint.sh` 中判断环境变量，决定镜像执行的命令。
```bash
#!/usr/bin/env bash

MODE=${MODE:-django}

cmd=""

if [ $MODE = 'django' ]; then
    mkdir -p /data/logs/uwsgi
    cmd="/usr/local/python3/bin/uwsgi --ini uwsgi.ini"
elif [ $MODE = 'celery_beat' ]; then
    cmd="/usr/local/python3/bin/celery beat -A drf_template -l info"
elif [ $MODE = 'celery_worker_queue_default' ]; then
    cmd="/usr/local/python3/bin/celery worker -A drf_template -l info -Q default"
elif [ $MODE = 'runscript' ]; then
    runscript_name=${runscript_name:-runscript_name}
    cmd="/usr/local/python3 manage.py runscript $runscript_name --traceback"
fi
```