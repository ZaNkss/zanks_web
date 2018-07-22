import json
from queue import Queue
import requests
from flask import Blueprint, request
from app.models.ac_userInfo import AcUserInfoController, AcUserInfo
from logger import logger
from instance.private_info import AUTHORIZECODE, MINIAPP_ID, MINIAPP_SECRET

# 创建蓝图，该模块为空调遥控模块
acController = Blueprint('acController', __name__)
# 维护一个从遥控器端发来的请求队列，最大可维护数为100
requestList = Queue(100)


# 处理授权请求
@acController.route('/authorize', methods=['POST'])
def ac_authorize():
    # 接收数据
    user_info = request.get_json()['userInfo']
    authorize_code = request.get_json()['authorizeCode']
    openid = request.get_json()['openid']
    logger.warn("收到来自" + user_info['nickName'] + "的请求，授权码为" + authorize_code)

    # 处理授权请求
    if authorize_code == AUTHORIZECODE:
        isauthorize = True
        msg = '授权成功'
        logger.warn(user_info['nickName'] + "获取授权成功")
        is_auth = True
    else:
        isauthorize = False
        msg = '授权码错误'
        logger.warn(user_info['nickName'] + "获取授权失败")
        is_auth = False
    # 更新数据库
    ac_user_info = AcUserInfo(openid, user_info['nickName'], is_auth)
    if AcUserInfoController.select(openid).__len__() == 0:
        AcUserInfoController.add(ac_user_info)
    else:
        AcUserInfoController.update(ac_user_info)

    return msg


# 处理初始化请求
@acController.route('/onLogin', methods=['POST'])
def ac_onlogin():
    # print(request.get_json())
    # 接收数据
    code = request.get_json()['code']
    openid = request.get_json()['openid']
    reslut = AcUserInfoController.select(openid)
    if reslut.__len__() == 0:
        # 该用户为初次使用这个小程序
        # 向微信官方请求openid
        response = requests.get('https://api.weixin.qq.com/sns/jscode2session?'
                                'appid=%s&'
                                'secret=%s&'
                                'js_code=%s&'
                                'grant_type=authorization_code' %(MINIAPP_ID, MINIAPP_SECRET, code))
        # 将该用户的信息初始化并存入数据库中
        openid = response.json()['openid']
        is_auth = False
        ac_user_info = AcUserInfo(openid,'default',is_auth)
        AcUserInfoController.add(ac_user_info)
    else:
        # 该用户在授权列表里
        is_auth = reslut[0][2]
        # print(is_auth)
        if is_auth == 0:
            is_auth = False
        else:
            is_auth = True
    # 构建返回的json字符串
    msg = {'openid': openid, 'is_auth': is_auth}
    msg = json.dumps(msg)
    return msg


# 处理开机请求
@acController.route('/onStart', methods=['POST'])
def ac_on_start():
    # print(request.get_json())
    openid = request.get_json()['openid']
    reslut = AcUserInfoController.select(openid)
    if reslut.__len__() == 0:
        return 'false'
    else:
        if reslut[0][2] == 0:
            return 'false'
        else:
            # 拥有授权，开始处理
            requestList.put('start')
            logger.warn("添加来自 " + reslut[0][1] + " 的 开机 请求。目前请求池数目为: "
                        + requestList.qsize().__str__())
            return 'ok'


# 处理关机请求
@acController.route('/onStop', methods=['POST'])
def ac_on_stop():
    # print(request.get_json())
    openid = request.get_json()['openid']
    reslut = AcUserInfoController.select(openid)
    if reslut.__len__() == 0:
        return 'false'
    else:
        if reslut[0][2] == 0:
            return 'false'
        else:
            # 拥有授权，开始处理
            requestList.put('stop')
            logger.warn("添加来自 " + reslut[0][1] + " 的 关机 请求。目前请求池数目为: "
                        + requestList.qsize().__str__())
            return 'ok'


# 处理来自树莓派的请求
@acController.route('/getOpt', methods=['GET'])
def ac_get_opt():
    if requestList.empty():
        return 'nothing'
    else:
        opt = requestList.get()
        if opt == 'start':
            logger.warn('一个 开机 请求被成功处理，目前请求池容量： '
                        + requestList.qsize().__str__())
            return opt
        elif opt == 'stop':
            return opt
        else:
            return 'go away'



