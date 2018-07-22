# acController 的用户信息表
# 表结构：
# -----------------------------------
# | openid | nickname | isAuthorize |
# -----------------------------------
import pymysql
from instance.private_info import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_CHARSET


class AcUserInfo():
    openid = 'openid'
    nickname = 'nickname'
    is_auth = False

    def __init__(self,openid,nickname,is_auth):
        self.openid = openid
        self.nickname = nickname
        self.is_auth = is_auth


class AcUserInfoController:

    @classmethod
    def add(self, acuserinfo):
        db = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_NAME, charset=DB_CHARSET)
        sql = 'insert into ac_user_info (openid,nickname,is_auth) values ("%s","%s",%s)'\
              %(acuserinfo.openid,acuserinfo.nickname,acuserinfo.is_auth)
        # print(sql)
        cursor = db.cursor()
        # cursor.execute(sql)
        # db.commit()
        try:
            cursor.execute(sql)
            db.commit()
            # print('ok')
            return True
        except Exception as e:
            db.rollback()
            # print('false')
            return False
        finally:
            db.close()

    @classmethod
    def update(self, acuserinfo):
        db = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_NAME, charset=DB_CHARSET)
        sql = 'update ac_user_info set nickname = "%s",is_auth = %s where openid = "%s"' \
              % (acuserinfo.nickname, acuserinfo.is_auth,acuserinfo.openid)
        # print(sql)
        cursor = db.cursor()
        try:
            cursor.execute(sql)
            db.commit()
            # print('ok')
            return True
        except Exception as e:
            db.rollback()
            # print('false')
            return False
        finally:
            db.close()

    @classmethod
    def delete(self,openid):
        db = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_NAME, charset=DB_CHARSET)
        sql = 'delete From ac_user_info where openid = "%s"' %(openid)
        # print(sql)
        cursor = db.cursor()
        try:
            cursor.execute(sql)
            db.commit()
            # print('ok')
            return True
        except Exception as e:
            db.rollback()
            # print('false')
            return False
        finally:
            db.close()


    @classmethod
    def select(self,openid):
        db = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_NAME, charset=DB_CHARSET)
        sql = 'select * from ac_user_info where openid = "%s"' %(openid)
        # print(sql)
        cursor = db.cursor()
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            db.commit()
            # print('ok')
            return results
        except Exception as e:
            db.rollback()
            # print('false')
            return False
        finally:
            db.close()
        pass

# ac = AcUserInfo
# ac.openid = "hello"
# ac.nickname = "帽子底下有呆毛"
# ac.is_auth = False
# print(AcUserInfoController.add(ac))
# ac.nickname = "帽子底下没有毛"
# print(AcUserInfoController.update(ac))
# print(AcUserInfoController.select(ac.openid)[0][2])

# if AcUserInfoController.select(ac.openid).__len__() == 0:
#     print('null')
# print(AcUserInfoController.delete(ac.openid))
