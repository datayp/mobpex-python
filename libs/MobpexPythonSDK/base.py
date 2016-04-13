# -*- coding: utf-8 -*-
'''
Created on 2016-03-28
@author   genshen.hu
'''

import datetime  
import urllib, hashlib  
import base64 
import ssl 
import  logging
logging.basicConfig(level=logging.INFO)
try :  
    import json  
except ImportError : 
    import simplejson as json
try:
    import urllib2
except ImportError:
    flag='urllib'
    pass
from collections import OrderedDict
try:
    import urllib.request
    import urllib.parse
except ImportError:
    flag='urllib2'
    pass

'''
定义变量
'''
Format     = 'json'  
SignMethod = 'md5'   
locale     ='zh_CN'
timeTemp = datetime.datetime.now().microsecond  
time     =str(timeTemp)
class Client :  
    def __init__(self,appId,userId,Gateway,secretKey,ignoreSSLCheck,**kwargs) :  
       #===========================================================================
       # 客户端入口
       #===========================================================================
        self.sys_params = {  
                    'appId' : appId,  
                    'format'  : Format,  
                    'userId':userId,
                    'format':Format,
                    'locale':locale,
                     'signRet':'true',
                     'ts':time
        }  
        self.secretKey = secretKey 
        self.gateway = Gateway
        self.ignoreSSLCheck=ignoreSSLCheck
        if kwargs :  
            self.sys_params.update(kwargs)  
    
    def sign(self, params) :
    #===========================================================================
    # '''签名方法
    # @param params: 支持字典和string两种
    # '''
    #===========================================================================
        keys = params.keys()
        key =sorted(keys)
        s = self.secretKey 
        for i in key :
            temp=i+params[i] 
            s += temp
        s += self.secretKey 
        m = hashlib.md5()
        signs=s.encode("utf-8")          
        m.update(signs)  
        return m.hexdigest()

    def getResponse(self, request) : 
    #===========================================================================
    # '''获取服务器返回方法
    # @param request
    # '''
    #=========================================================================== 
            d = self.sys_params.copy()  
            api_params = request.get_api_params()  
            d['method'] = request.get_method_name()  
            d['ts'] = time
            #获取版本号
            d['v']=request.get_version()
            api_params.update(d)  
            d['sign'] = self.sign(api_params)  
            gateway=self.gateway
            methodName=request.get_method_name() 
            #忽略ssl证书
            if self.ignoreSSLCheck=='true':
                ssl._create_default_https_context = ssl._create_unverified_context
            #请求头    
            headers={
                      "Content-Type":"application/x-www-form-urlencoded;charset=utf-8",
                      "Cache-Control": "no-cache"
                      }
            #url拼装 
            url=gateway+methodName
            try:
               if flag=='urllib2':
                  data_string =  urllib.urlencode(d)
                  req = urllib2.Request(url,data_string,headers) 
                  res = urllib2.urlopen(req,timeout=30)
                  if res.code  is not  200:
                      raise RequestException('非法状态:'+str(res.status)+",body:"+str(res.read().decode('utf-8')))   
               else:
                  data_string=urllib.parse.urlencode(d).encode(encoding='UTF8')
                  res= urllib.request.urlopen(url,data_string,timeout=30) 
                  if res.status is not 200:
                       raise RequestException('非法状态:'+str(res.status)+",body:"+str(res.read().decode('utf-8')))  
               content = res.read().decode('utf-8') 
               if content:      
                  jsonObj=json.loads(content,encoding='utf-8',object_pairs_hook=OrderedDict) 
                  return jsonObj
               else:
                  return 
            except Exception as e :
                 print(e)     
            finally:
                 #关闭连接
                 res.close() 

    def validResultSign(self,params): 
    #===========================================================================
    # '''服务端数据验证签名方法
    # @param params: 支持字典
    # '''
    #===========================================================================
          if params  is None:
             return  False
          Result=''
          ext=''
          ts=''
          status=''
          if 'state' in params:
              status=params["state"]
          if 'ts' in params:
              ts=str(params["ts"])
          if 'ext' in params:
               extContent=params['ext']
               extStr=json.dumps(extContent,ensure_ascii=False)
               ext=extStr.replace('\t','').replace('\n','').replace(' ','')
          if 'result' in params:
              resultContent =params['result']
              resultStr=json.dumps(resultContent,separators=(',',':'),ensure_ascii=False)
              Result=resultStr.replace('\t','').replace('\n','').replace(' ','').strip()
          #进行sign字符串
          signStrTemp=self.secretKey+status+Result+ts+ext+self.secretKey
          signStr=signStrTemp.encode("utf-8")
          m = hashlib.md5()  
          m.update(signStr)  
          tempSign=m.hexdigest()
          if 'sign' in params :
             if tempSign == params['sign']:
                  return True
             else:
                  return False  
          else:
            return False

class TopRequest : 
    #===========================================================================
    # '''
    # 参数转换类
    # '''
    #=========================================================================== 
    def __init__(self, method_name) :  
        self.method_name = method_name  
        self.api_params = {}  
    
    def get_api_params(self) : 
        return self.api_params  
    
    def get_method_name(self) :
        return self.method_name 

    def  get_version(self):
         return self.get_middle_str(self.method_name,'rest/v','/')
             
    def __setitem__(self, param_name, param_value) : 
        self.api_params[param_name] = param_value

    def get_middle_str(self,content,startStr,endStr):
        startIndex=content.find(startStr)
        if startIndex >= 0:
          startIndex+=len(startStr)
          endIndex=content.find(endStr,startIndex)
          if endIndex >= 0:
               ver=content[startIndex:endIndex].strip()
               if ver:
                  return ver
               else:
                  return ''
          else:
               return ''        
        else:
          return ''

class RequestException(Exception):
    #===========================================================================
    # 请求连接异常类
    #===========================================================================
    pass 
