# -*- coding: utf-8 -*-
from urllib.parse import urljoin
import qiniu as QiniuClass
from django.conf import settings

class Qiniu(object):
    def __init__(self):
        self.init_app()

    def init_app(self):
        self._access_key = getattr(settings,'QINIU_ACCESS_KEY', '')
        self._secret_key = getattr(settings,'QINIU_SECRET_KEY', '') 
        self._bucket_name = getattr(settings,'QINIU_BUCKET_NAME', '')
        domain = getattr(settings,'QINIU_BUCKET_DOMAIN')
        if not domain:
            self._base_url = 'http://' + self._bucket_name + '.qiniudn.com'
        else:
            self._base_url = 'http://' + domain

    def save(self, data, filename=None):
        auth = QiniuClass.Auth(self._access_key, self._secret_key)
        token = auth.upload_token(self._bucket_name)
        ret, info = QiniuClass.put_data(token, filename, data)
        print(info)
        return urljoin(self._base_url, ret['key'])

    def delete(self, filename):
        auth = QiniuClass.Auth(self._access_key, self._secret_key)
        bucket = QiniuClass.BucketManager(auth)
        return bucket.delete(self._bucket_name, filename)

    def min_delete(self, filename):
        auth = QiniuClass.Auth(self._access_key, self._secret_key)
        bucket = QiniuClass.BucketManager(auth)
        return bucket.delete('min-img', filename)

    def url(self, filename):
        return urljoin(self._base_url, filename)

    def min_url(self, filename):
        q = QiniuClass.Auth(self._access_key, self._secret_key)
        #要缩略的文件所在的空间和文件名。
        from_bucket_name = 'user-img'
        to_bucket_name = 'min-img'
        from_key = filename 
        to_key = 'min_'+from_key 
        self.min_delete(to_key)
        #pipeline是使用的队列名称,不设置代表不使用私有队列，使用公有队列。
        pipeline = ''
        #要进行缩略的操作。
        fops = 'imageView2/1/w/50/h/50/q/100|imageslim'
        saveas_key = QiniuClass.urlsafe_base64_encode(to_bucket_name+':'+to_key)
        fops = fops+'|saveas/'+saveas_key
        pfop = QiniuClass.PersistentFop(q, from_bucket_name, pipeline)
        ops = []
        ops.append(fops)
        ret, info = pfop.execute(from_key, ops, 1)
        print(info) 
        new_src = 'http://opkrd0ovy.bkt.clouddn.com'
        new_url = urljoin(new_src, to_key)       
        #map要缩略的文件所在的空间和文件名。
        from_bucket_name = 'min-img'
        to_bucket_name = 'min-img'
        map_from_key = 'st_out.png'
        map_to_key = 'map_'+from_key
        self.min_delete(map_to_key)
        #pipeline是使用的队列名称,不设置代表不使用私有队列，使用公有队列。
        pipeline = ''
        #要进行缩略的操作。
        bg_img = QiniuClass.urlsafe_base64_encode(new_url)
        fops = 'imageView2/2/w/65/h/90/q/75|watermark/1/image/'+bg_img+'/dissolve/100/gravity/North/dx/0/dy/5|imageslim'
        print(fops)
        saveas_key = QiniuClass.urlsafe_base64_encode(to_bucket_name+':'+map_to_key)
        fops = fops+'|saveas/'+saveas_key
        pfop = QiniuClass.PersistentFop(q, from_bucket_name, pipeline)
        ops = []
        ops.append(fops)
        ret, info = pfop.execute(map_from_key, ops, 1)
        print(info)
        return urljoin(new_src, map_to_key)       


    def get_token(self):
        auth = QiniuClass.Auth(self._access_key, self._secret_key)
        token = auth.upload_token(self._bucket_name) 
        return token

    def list_all(self, prefix, limit=100):
        auth = QiniuClass.Auth(self._access_key, self._secret_key)
        rlist=[]
        bucket = QiniuClass.BucketManager(auth)
        marker = None
        eof = False
        while eof is False:
            ret, eof, info = bucket.list(self._bucket_name, prefix=prefix, marker=marker, limit=limit)
            marker = ret.get('marker', None)
            for item in ret['items']:
                item_info = {'url':urljoin(self._base_url,item["key"]),'original':'test'}
                print(item_info)
                rlist.append(item_info)
        if eof is not True:
            # 错误处理
            #print "error"
            pass
        return rlist

