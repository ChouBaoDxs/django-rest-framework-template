import logging
import os
import sys
from importlib import import_module
from typing import Union

import django

from utils.strings import hump2underline

project_root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drf_template.settings')
django.setup()

logger = logging.getLogger('default.scripts.generate_crud_code')

current_dir = os.path.dirname(os.path.abspath(__file__))

from django.db import models
from django.template import Template, Context


class CrudCodeGenerator:
    logger = logger
    temp_dir = os.path.join(current_dir, 'generate_crud_code')
    template_dir = os.path.join(current_dir, 'generate_crud_code_template')
    serializers_tpl_file_path = os.path.join(template_dir, 'serializers.tpl')
    schemas_tpl_file_path = os.path.join(template_dir, 'schemas.tpl')
    filters_tpl_file_path = os.path.join(template_dir, 'filters.tpl')
    views_tpl_file_path = os.path.join(template_dir, 'views.tpl')

    def __init__(self, model_path):
        self.logger.info(f'初始化代码生成器，model_path: {model_path}')
        self.model_path = model_path
        # model_path = 'user.models.UserProfile'
        model_path_split = model_path.split('.')
        self.model_module_path = '.'.join(model_path_split[:-1])  # user.models
        self.model_name = model_path_split[-1]  # UserProfile
        self.model_name_lower = hump2underline(self.model_name)  # user_profile
        self.model_module = import_module(self.model_module_path)
        self.model = getattr(self.model_module, self.model_name)

    @classmethod
    def make_dir(cls, dir_path: Union[str, list]):
        if isinstance(dir_path, str):
            dir_path = [dir_path]
        for e in dir_path:
            if not os.path.exists(e):
                os.mkdir(e)

    @classmethod
    def read_file(cls, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    @classmethod
    def write_file(cls, file_path, content):
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def load_template(self):
        self.serializers_template = Template(self.read_file(self.serializers_tpl_file_path))
        self.schemas_template = Template(self.read_file(self.schemas_tpl_file_path))
        self.filters_template = Template(self.read_file(self.filters_tpl_file_path))
        self.views_template = Template(self.read_file(self.views_tpl_file_path))

    def generate_serializers_code(self):
        fields = self.model._meta.fields
        ser_fields = []
        ignore_field_set = {'deleted_at'}
        default_ser_special_field_code = ''
        default_ser_create_method_code = ''
        text_field_set = set()
        uneditable_field_set = set()
        for field in fields:
            if field.name in ignore_field_set:
                continue

            if field.name == 'creator':
                default_ser_create_method_code += f'''def create(self, validated_data):
        validated_data['creator_id'] = self.context['request'].user.id
        return super().create(validated_data)\n
'''

            if isinstance(field, models.ForeignKey):
                if field.editable:
                    default_ser_special_field_code += f'''{field.attname} = serializers.PrimaryKeyRelatedField(
        help_text='{field.verbose_name}',
        queryset={field.related_model._meta.object_name}.objects.all(),
        source='{field.name}',
        required={not field.null},
        allow_null={field.null},
    )
'''
            elif isinstance(field, models.TextField):
                text_field_set.add(field.attname)

            ser_fields.append(field.attname)

            if field.editable is False:
                uneditable_field_set.add(field.attname)

        default_ser_fields = ser_fields
        retrieve_ser_fields = ser_fields.copy()
        list_ser_fields = ser_fields.copy()
        for field in text_field_set:  # models.TextField 一般不方便出现在 list 接口中
            list_ser_fields.remove(field)
        for field in uneditable_field_set:
            default_ser_fields.remove(field)

        context = {
            'model_module_path': self.model_module_path,
            'model_name': self.model_name,
            'default_ser_special_field_code': default_ser_special_field_code,
            'default_ser_create_method_code': default_ser_create_method_code,
            'default_ser_fields': default_ser_fields,
            'retrieve_ser_fields': retrieve_ser_fields,
            'list_ser_fields': list_ser_fields,
        }
        serializers_code = self.serializers_template.render(context=Context(context))
        return serializers_code

    def generate_filters_code(self):
        context = {
            'model_module_path': self.model_module_path,
            'model_name': self.model_name,
            'special_filter_field_code': '',
        }
        filters_code = self.filters_template.render(context=Context(context))
        return filters_code

    def generate_schemas_code(self):
        context = {
            'model_name': self.model_name,
            'model_verbose_name': self.model._meta.verbose_name,
        }
        schemas_code = self.schemas_template.render(context=Context(context))
        return schemas_code

    def generate_views_code(self):
        filter_module_path = f'{self.apis_dir_module_path}.filters.{self.model_name_lower}'
        schema_module_path = f'{self.apis_dir_module_path}.schemas.{self.model_name_lower}'
        serializer_module_path = f'{self.apis_dir_module_path}.serializers.{self.model_name_lower}'

        context = {
            'model_module_path': self.model_module_path,
            'model_name': self.model_name,
            'filter_module_path': filter_module_path,
            'schema_module_path': schema_module_path,
            'serializer_module_path': serializer_module_path,
            'model_verbose_name': self.model._meta.verbose_name,
        }
        views_code = self.views_template.render(context=Context(context))
        return views_code

    def generate_all_code(self, is_regenerate):

        self.load_template()

        serializers_dir = os.path.join(self.target_apis_dir_path, 'serializers')
        filters_dir = os.path.join(self.target_apis_dir_path, 'filters')
        schemas_dir = os.path.join(self.target_apis_dir_path, 'schemas')
        views_dir = os.path.join(self.target_apis_dir_path, 'views')
        self.make_dir([
            serializers_dir,
            filters_dir,
            schemas_dir,
            views_dir,
        ])

        serializers_file_path = os.path.join(serializers_dir, self.model_name_lower) + '.py'
        if os.path.isfile(serializers_file_path) and not is_regenerate:
            self.logger.info(f"{self.model_path} 已经生成过")
            return
        serializers_code = self.generate_serializers_code()
        self.write_file(serializers_file_path, serializers_code)

        filters_file_path = os.path.join(filters_dir, self.model_name_lower) + '.py'
        filters_code = self.generate_filters_code()
        self.write_file(filters_file_path, filters_code)

        schemas_file_path = os.path.join(schemas_dir, self.model_name_lower) + '.py'
        schemas_code = self.generate_schemas_code()
        self.write_file(schemas_file_path, schemas_code)

        views_file_path = os.path.join(views_dir, self.model_name_lower) + '.py'
        views_code = self.generate_views_code()
        self.write_file(views_file_path, views_code)

    def generate_to_temp_dir(self, is_regenerate=False):
        self.make_dir(self.temp_dir)
        self.target_apis_dir_path = os.path.join(self.temp_dir, 'apis')
        self.make_dir(self.target_apis_dir_path)
        self.apis_dir_module_path = '.'
        self.logger.info(f'开始生成 {self.model_path} 的 CRUD 代码到临时目录：{self.target_apis_dir_path}')

        self.generate_all_code(is_regenerate)

        self.logger.info(f'{self.model_path} 的 CRUD 代码生成到临时目录完成！')

    def generate_to_target_apis_dir(self, target_apis_dir_path, apis_dir_module_path, is_regenerate=False):
        self.target_apis_dir_path = target_apis_dir_path  # 绝对路径
        self.apis_dir_module_path = apis_dir_module_path  # 'apps.user.apis'
        self.make_dir(self.target_apis_dir_path)
        self.logger.info(f'开始生成 {self.model_path} 的 CRUD 代码到指定目录：{target_apis_dir_path}，apis 模块路径：{apis_dir_module_path}')

        self.generate_all_code(is_regenerate)

        self.logger.info(f'{self.model_path} 的 CRUD 代码生成到指定目录完成！')


def run(*args):
    if len(args) > 0:
        model_path = args[0]
    else:
        model_path = 'generate_crud_code_example.models.Book'

    code_generator = CrudCodeGenerator(model_path)
    # 生成代码到临时目录
    # code_generator.generate_to_temp_dir()

    # 生成代码到指定目录
    code_generator.generate_to_target_apis_dir(
        os.path.join(project_root_dir, 'apps/generate_crud_code_example/apis'),
        'apps.generate_crud_code_example.apis',
        is_regenerate=True,
    )


if __name__ == '__main__':
    run()
