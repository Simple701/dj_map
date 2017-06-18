#coding:utf-8
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required 
from mymap.models import Marker, Post
from mymap.flask_qiniustorage import Qiniu
import json
from mymap.forms import MarkerForm ,PostForm
import os,sys,re
from django.http import JsonResponse


@login_required  
def index(request):
    mks = list(u_marks(request))
    if len(mks) == 0 :
        mks=''
    return render(request, 'map.html',{'mks': json.dumps(mks) })

@login_required  
def mk_list(request):
    mks = list(u_marks(request))
    if len(mks) == 0 :
        mks=''
    return render(request, 'mark_list.html',{'mks': json.dumps(mks) })

@login_required  
def mk_del(request):
    if request.method == 'POST':
        m_id = request.POST.getlist('mark_id')
        print(m_id)
        rt=u_marks_del(m_id[0])
    mks = list(u_marks(request))
    if len(mks) == 0 :
        mks=''
    return JsonResponse(mks,safe=False)


@login_required  
def mk_update(request):
    if request.method == 'POST':
        m_id = request.POST.getlist('id')[0]
        m_date = request.POST.getlist('dt')[0]
        m_title = request.POST.getlist('name')[0]
        print(m_id)
        rt=u_mark_update(m_id,m_title,m_date)
    mks = list(u_marks(request))
    if len(mks) == 0 :
        mks=''
    return JsonResponse(mks,safe=False)

@login_required 
def mk_add(request):
    if request.method == 'POST':
        mfm = MarkerForm(request.POST)
        if mfm.is_valid():
            rt = u_marks_add(mfm,request)
            return HttpResponseRedirect("/") 
    else :
        mfm = MarkerForm()
    return render(request,'welcome.html',{'mfm': mfm})

@login_required
def mk_pt_get(request):
    m_id = request.GET['id']
    pt_id='0'
    c_text='this is one text!'
    pt = u_mk_post(m_id)
    if pt :
        pt_id=pt['id']
        c_text=pt['content']

    return render(request,'read_more.html',{'mk_id': m_id,'pt_id': pt_id,'c_text':c_text})


@login_required 
def pt_add(request):
    rt=''
    if request.method == 'POST':
        pfm = PostForm(request.POST)
        if pfm.is_valid() and pfm.cleaned_data['post_id']=='0' :
            rt = u_post_add(pfm,request)
        else:
            u_post_update(pfm,request)
            rt= pfm.cleaned_data['post_mid']

    return HttpResponseRedirect("/do_editor?id="+str(rt))



###########################tools function 
def change_img_url(img_text):
    map_url="http://opkrd0ovy.bkt.clouddn.com/map_2026_1483883967000510.jpg"
    new_text=img_text
    regex=r'\"(http://oaqpu3kp9\.bkt\.clouddn\.com/u[0-9]+_[0-9]+\.\D\D\D)\"'
    n=1
    for match in re.finditer(regex, img_text) :
        result = match.group(1) 
        if n== 1:
            m_img = result.replace('oaqpu3kp9.bkt.clouddn.com/','opkrd0ovy.bkt.clouddn.com/map_')
            map_url=m_img
        text_rt = new_text.replace(result,result+'?imageView2/1/w/100/h/100/q/75|imageslim')
        new_text=text_rt
        n=n+1
    
    return new_text,map_url   



########################### Marks function 
def u_marks_del(m_id):
    print('u_marks_del')
    mks = Marker.objects.filter(id=m_id)
    mks.delete()
    return 1

def u_mark_update(m_id,m_title,m_date):
    print('u_mark_update')
    qs = Marker.objects.get(id=m_id) 
    qs.title=m_title
    qs.mdate=m_date
    qs.save()
    return 1

def u_marks(rq):
    print('u_marks')
    uid=rq.session['_auth_user_id']
    qs = Marker.objects.filter(author=uid) 
    mks = []
    for m in qs :
        pt=u_mk_post(m.id)
        m_img = "http://opkrd0ovy.bkt.clouddn.com/map_2026_1483883967000510.jpg"
        pt_id=0
        pt_content='This is a new world~'
        if pt :
            pt_id=pt['id']
            pt_content,m_img = change_img_url(pt['content']) 

        mks.append({
            "m_id":m.id,
            "pointx":m.pointx,
            "pointy":m.pointy,
            "c_text":pt_content,
            "c_id":pt_id,
            "title":m.title,
            "m_date":m.mdate,
            "img":m_img
            })
    return mks

def u_marks_add(mfm,rq):
    print('u_marks_add')
    m = Marker(
        pointx=mfm.cleaned_data['mark_loc'].split(",")[0],
        pointy=mfm.cleaned_data['mark_loc'].split(",")[1],
        mdate=mfm.cleaned_data['mark_time'],
        title=mfm.cleaned_data['mark_name'],
        img="",
        author=rq.session['_auth_user_id']
    )
    m.save()
    return 1


########################### Post function
def u_post_add(pfm,rq):
    print('u_post_add')
    m = Post(
        mk_id=pfm.cleaned_data['post_mid'],
        title='',
        content=pfm.cleaned_data['post_content'],
        author=rq.session['_auth_user_id']
    )
    m.save()
    rt = m.mk_id
    return rt

def u_post_update(pfm,rq):
    print('u_post_update')
    qs = Post.objects.get(id=pfm.cleaned_data['post_id']) 
    qs.content = pfm.cleaned_data['post_content']
    qs.save()
    return 1

def u_mk_post(mk_id):
    print('u_mk_post')
    qs = Post.objects.filter(mk_id=mk_id) 
    pt = {}
    for p in qs :
        pt={
            "id":p.id,
            "mk_id":p.mk_id,
            "content":p.content,
            "title":p.title
            }
    return pt
########################### editor function
@login_required
def get_token(request):
    qiniu_store = Qiniu()
    token = qiniu_store.get_token()
    return HttpResponse(token) 

########################### editor function
@login_required
def get_min_url(request):
    qiniu_store = Qiniu()
    img_key=request.GET['key']
    min_url = qiniu_store.min_url(img_key)
    print(min_url)
    return HttpResponse(min_url) 

@login_required
def ediror_upload(request):
    uid=request.session['_auth_user_id']
    qiniu_store = Qiniu()
    action = request.GET['action']
    # 解析JSON格式的配置文件
    # 这里使用PHP版本自带的config.json文件
    with open(os.path.join('mymap/static','ueditor', 'php','config.json')) as fp:
        try:
            # 删除 `/**/` 之间的注释
            CONFIG = json.loads(re.sub(r'\/\*.*\*\/', '', fp.read()))
            CONFIG['LoginUid']=uid
        except:
            CONFIG = {}
            print(2)

    if action == 'config':
        # 初始化时，返回配置文件给客户端
        result = CONFIG

    if action in ('uploadimage', 'uploadvideo', 'uploadfile'):
        upfile = request.files['file']  # 这个表单名称以配置文件为准
        print(123)
        name, ext = os.path.splitext(upfile.filename)
        ##生成一个随机数目，防止批量上传的时候文件名同名出错
        randNumber = str(math.floor(random.random()*10))+str(math.floor(random.random()*20))
        new_name = str(int(time.time()))+randNumber+ext;
        # upfile 为 FileStorage 对象
        # 这里保存文件并返回相应的URL
        fname = 'u'+uid+'_'+new_name 
        out_fname = qiniu_store.save(upfile,fname)
        result = {
            "state": "SUCCESS",
            "url": out_fname,
            "title": "demo.jpg",
            "original": "demo.jpg"
        }

    if action  == 'listimage':
        rlist = qiniu_store.list_all('u'+uid+'_')
        total = len(rlist)
        print(total)
        result = {
            "state": "SUCCESS",
            "list" : rlist,
            "start": 0,
            "total": total
        }

    ##
    return HttpResponse(json.dumps(result), content_type='application/json')

