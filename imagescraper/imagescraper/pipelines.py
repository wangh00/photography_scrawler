# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline


# class ImagescraperPipeline:
#     def process_item(self, item, spider):
#         return item



class CustomImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, item=None):
        # 使用item中的image_name作为文件名
        return f"/{item['image_name']}" if item and 'image_name' in item else super().file_path(request, response=response, info=info, item=item)

    def item_completed(self, results, item, info):
        # 打印已下载图片的文件路径
        for success, file_info in results:
            if success:
                file_path = file_info['path']
                print(f"已下载图片：{file_path}")
        return item