class Config(object):
    """配置信息"""
    # session_key配置
    SECRET_KEY = "SDSDFWE#KHISKHFK"


    # 对cookies中的session进行混淆
    SESSION_USE_SIGNER = True
    # session有效时间：单位（s）
    PERMANENT_SESSION_LIFETIME = 86400
    # 上传文件的最大字节
    MAX_CONTENT_LENGTH = 1024*1024*10


class DevelopmentConfig(Config):
    """开发环境配置信息"""
    DEBUG = True


class ProductionConfig(Config):
    """生产环境配置信息"""
    pass


config_map = {
    "develop": DevelopmentConfig,
    "product": ProductionConfig
}
