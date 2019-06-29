# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
from urllib import request
from scrapy.pipelines.images import ImagesPipeline
from bmw import settings

class BmwPipeline(object):
    def __init__(self):
        # 获取当前文件路径，向上寻找两层即工程路径，join()拼接一个images路径
        self.path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'images')
        if not os.path.exists(self.path):
            os.mkdir(self.path)

    def process_item(self, item, spider):
        category = item['category'] #item中获取到
        urls = item['urls']

        #创建种类文件夹
        category_path = os.path.join(self.path,category)
        if not os.path.exists(category_path):
            os.mkdir(category_path)
        for url in urls:
            image_name = url.split("_")[-1] # 将最后一个字符串提取出来作为名字
            request.urlretrieve(url,os.path.join(category_path,image_name)) # request.urlretrieve下载的函数（链接，存储地址）
        return item

# 重写scrapy提供的ImagesPipeline
class BMWImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        #这个方法是在发送下载请求前调用
        #这个方法本身就是去发送下载请求的
        request_objs = super(BMWImagesPipeline, self).get_media_requests(item,info)
        for request_obj in request_objs:
            request_obj.item = item
        return request_objs

    #重写file_path，用它调用父类的file_path
    def file_path(self, request, response=None, info=None):
        path = super(BMWImagesPipeline, self).file_path(request,response,info)
        category = request.item.get('category')
        images_store = settings.IMAGES_STORE
        category_path = os.path.join(images_store,category)
        if not os.path.exists(category_path):
            os.mkdir(category_path)
        image_name = path.replace("full/","")
        image_path = os.path.join(category_path,image_name)
        return image_path