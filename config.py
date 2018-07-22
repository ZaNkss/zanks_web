# app的配置文件


# Config父类，一些基本配置
class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:xxxxx@localhost:3306/test?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


# 开发环境配置
class DevConfig(Config):
    Debug = True


# 产品环境配置
class ProductConfig(Config):
    pass


config = {
    'development': DevConfig,
    'default': ProductConfig
}