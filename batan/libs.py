from scrapy.utils.project import get_project_settings
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join
import yaml
import os
from batan.items import BatanItem


class BatanItemLoader(ItemLoader):
    default_output_processor = TakeFirst()

    # content_out = Join()
    # labels_out = Join(separator='#|#')

    def __init__(self, item=None, selector=None, response=None, parent=None, **context):
        item = item or BatanItem()
        super(BatanItemLoader, self).__init__(item, selector, response, parent, **context)


def parse_config(name):
    settings = get_project_settings().copy()
    config_file = os.path.join(settings['CONFIGS_DIR'], '{name}'.format(name=name))
    if os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf8') as f:
            try:
                return yaml.load(f.read(), Loader=yaml.FullLoader)
            except Exception as e:
                raise ValueError('{name} 配置文件错误请检查：\n{error}'.format(name=name, error=str(e)))
    else:
        raise FileNotFoundError('{name} 配置文件不存在请检查'.format(name=name))


if __name__ == '__main__':
    config = parse_config('CnblogSpider')
    print(config)
