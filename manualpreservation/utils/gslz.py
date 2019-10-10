# _*_ coding: UTF-8 _*_
import re
import os


# from util.singleton import Singleton
# from util.string_util import StringUtil

class Singleton(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_inst'):
            cls._inst = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._inst


class StringUtil(Singleton):
    def __init__(self):
        pass

    def isNotNullOrEmpty(self, result):
        if (result is not None and len(result) > 0):
            return True
        return False

    def replace_empty(self, input_str):
        if self.isNotNullOrEmpty(input_str):
            result = re.sub('\s+', '', input_str)
            return result
        return input_str

    def tupleIsNotNullOrEmpty(self, result):
        if (self.isNotNullOrEmpty(result) and result != []):
            return True
        return False

    def replaceStringBlank(self, str):
        if self.isNotNullOrEmpty(str):
            return self.replace_empty(str).replace('：', ':')
        return str


class BussinessURLUtil(Singleton):
    def __init__(self):
        try:
            # configs_file = open(os.path.join(os.path.dirname(os.path.dirname(__file__)),config.BUSSINESS_CONFIG_PATH))
            configs = {
                "oldURLReg": "entyId=\\w{1,}",
                "newURLReg": "&serial=.*?&signData=[A-Za-z0-9_\u4E00-\u9FA5\\.,@?^=%&amp;:/~\\+#//]{1,}",
                "prevURL": "http://218.242.124.22:8081/businessCheck/verifKey.do?showType=extShow",
                "tag": "$|$"
            }
            self.__stringUtil = StringUtil()
            self.__new_gslz_url_reg = configs.get('newURLReg')
            self.__tag = configs.get('tag')
            self.__prevURL = configs.get('prevURL')
        except Exception as e:
            raise e

    def __parseURL(self, url):
        if url != [] and len(url) > 0:
            return self.__tag.join(url.replace('&serial=', '').split('&signData='))
        return None

    def __getBusinessLicenseURL(self, pageContent):
        regResult = re.findall(self.__new_gslz_url_reg, self.__stringUtil.replaceStringBlank(pageContent))
        if regResult != [] and len(regResult) > 0:
            return regResult[0]
        return None

    def getLicenseNO(self, pageContent):
        regResult = re.findall(self.__new_gslz_url_reg, self.__stringUtil.replaceStringBlank(pageContent))
        if regResult != [] and len(regResult) > 0:
            return self.__parseURL(regResult[0])
        return None

    def getBusinessLicenseURL(self, paegContent):
        if self.__stringUtil.isNotNullOrEmpty(paegContent):
            licenseNo = self.__getBusinessLicenseURL(paegContent)
            if licenseNo is not None:
                return self.__prevURL + licenseNo
        return None

if __name__ == '__main__':
    date = []
    nb_dir = '/home/netboss/Z2018066/'
    o_list = os.listdir(nb_dir)
    for a in o_list:
        a = a + '/'
        date.append(a)
    for z in date:
        html_file = nb_dir + z + 'source.html'
        try:
            f=open(html_file,'r')
            content= f.read()
            ls = BussinessURLUtil()
            print(z+str(ls.getBusinessLicenseURL(content)))
            print(z+str(ls.getLicenseNO(content)))
        except Exception as e:
            print(e)