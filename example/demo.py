# -*- coding: utf-8 -*-
'''
Create on 2016/03/29

@author genshen.hu
'''

import  MobpexPythonSDK.base
import  logging
import  json

'''
设置调用需要的参数,必填
'''
#密钥
secretKey = 'LS_1bfs9nsAFBWqFncutrdt3du3qm2bi0s'
#开发者的AppId
appId     = '15122404366710489367'
#商户注册的用户id
userId    = 'long.chen-1@yeepay.com'
#魔派SERVER SDK API请求地址  
serverRoot   = 'https://www.mobpex.com/yop-center'
#忽略ssl检查
ignoreSSLCheck='true'

'''
查询APP可用支付渠道列表
'''
def findChannelInfoByAppId():
    try:
        #获取客户端对象     
        client = MobpexPythonSDK.base.Client(appId,userId,serverRoot,secretKey,ignoreSSLCheck)  
        req = MobpexPythonSDK.base.TopRequest('/rest/v1.0/query/findChannelInfoByAppId')  
        content = client.getResponse(req)
        print(content)
        #验证服务器返回的数据是否被篡改
        flag =client.validResultSign(content)
        if flag:
            logging.info('签名验证成功!')
        else: 
            logging.info('签名验证失败！')
    except Exception as e :
       print(e) 

#测试 
findChannelInfoByAppId()

'''
预支付请求
'''
def testProOder():
    prePayRequest ={
      #商户系统的支付请求流水号
      "tradeNo":"834153959835676",
      #支付渠道
      "payChannel":"ALIPAY",
      #支付类型
      "payType":"APP",
      #本次购买商品或服务名称
      "productName":"维多利亚的秘密",
      #描述
      "productDescription":"apple",
      #合计金额,精确到小数点后2位
      "amount":"1.00"
    }
    try:
        prePayRequestJson = json.dumps(prePayRequest)
        #获取客户端对象     
        client = MobpexPythonSDK.base.Client(appId,userId,serverRoot,secretKey,ignoreSSLCheck,prePayRequest=prePayRequestJson)  
        req = MobpexPythonSDK.base.TopRequest('/rest/v1.0/pay/unifiedOrder')  
        jsonObj = client.getResponse(req)
        print(jsonObj)
        #验证服务器返回的数据是否被篡改
        flag =client.validResultSign(jsonObj)
        if flag:
            logging.info('签名验证成功 ')
        else: 
            logging.info('签名验证失败！')
    except Exception as e :
       print(e) 

#测试
testProOder()

'''
退款请求
'''
def testRefund():
    refundRequest={
      #商户系统支付请求流水
      "tradeNo":"834153959836",
      #商户系统的退款请求流水号
      "refundNo":"333443",
      #合计金额，精确到小数点后2位
      "amount":"0.01",
      #描述
      "description":"我要退款~~~"
    }
    try: 
          refundRequestJson = json.dumps(refundRequest)
          client = MobpexPythonSDK.base.Client(appId,userId,serverRoot,secretKey,ignoreSSLCheck,refundRequest=refundRequestJson)  
          req = MobpexPythonSDK.base.TopRequest('/rest/v1.0/pay/refund')  
          jsonObj = client.getResponse(req)
          print(jsonObj)
          #验证服务器返回的数据是否被篡改
          flag =client.validResultSign(jsonObj)
          if flag:
            logging.info('签名验证成功 ')
          else: 
            logging.info('签名验证失败！')
    except Exception as e :
       print(e) 
#测试
testRefund()
       
'''
 退款查询请求
'''
def testRefundQuery():
    #商户订单编号，和发起支付请求中的requestFlowId一致
    tradeNo="656113769613"
    #商户退款流水
    refundNo="20485228279"
    try:
        client = MobpexPythonSDK.base.Client(appId,userId,serverRoot,secretKey,ignoreSSLCheck,tradeNo=tradeNo,refundNo=refundNo)  
        req = MobpexPythonSDK.base.TopRequest('/rest/v1.0/pay/queryRefundOrder')  
        jsonObj = client.getResponse(req)
        print(jsonObj)
        #验证服务器返回的数据是否被篡改
        flag =client.validResultSign(jsonObj)
        if flag:
            logging.info('签名验证成功 ')
        else: 
            logging.info('签名验证失败！')
    except Exception as e :
       print(e) 

#测试
testRefundQuery()

'''
支付查询请求
'''
def  testPayQuery():
    #商户支付请求流水号
    tradeNo="834153959835676"
    try:
         client = MobpexPythonSDK.base.Client(appId,userId,serverRoot,secretKey,ignoreSSLCheck,tradeNo=tradeNo)  
         req = MobpexPythonSDK.base.TopRequest('/rest/v1.0/pay/queryPaymentOrder')  
         jsonObj = client.getResponse(req)
         print(jsonObj)
         #验证服务器返回的数据是否被篡改
         flag =client.validResultSign(jsonObj)
         if flag:
            logging.info('签名验证成功 ')
         else: 
            logging.info('签名验证失败！')
    except Exception as e :
       print(e) 
#测试 
testPayQuery()

