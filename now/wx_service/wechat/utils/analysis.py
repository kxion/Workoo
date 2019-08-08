import time
import sys
import re
from xml.etree import ElementTree as ET

from django.utils.encoding import smart_str
from django.db.utils import IntegrityError
from wechat.models import UserInfo, TransactionInfo
from wechat.utils.service import DealService, AccountInfo
from wechat.utils.common import get_event
from wechat.tasks import main
from query_service.mycelery import app

# from now.wx_service.wechat.tasks import main
# from now.wx_service.query_service.mycelery import app
# from now.wx_service.wechat.utils.service import DealService
# from now.wx_service.wechat.models import UserInfo, TransactionInfo


class Analysis:
    def __init__(self, xmlData):
        print("接收到的数据：" + xmlData)
        self.xmlData = ET.fromstring(xmlData)
        self.msgType = self.xmlData.find("MsgType").text
        self.toUserName = self.xmlData.find("ToUserName").text
        self.fromUserName = self.xmlData.find("FromUserName").text
        self.deal = DealServer(self.fromUserName)

    def reply(self, xmlText=None):
        if xmlText == None:
            xmlData = self.xmlData
            msgType = self.msgType
            toUserName = self.toUserName
            openid = self.fromUserName
            fromUserName = self.fromUserName
        else:
            xmlData = ET.fromstring(xmlText)
            msgType = xmlData.find("MsgType").text
            toUserName = xmlData.find("ToUserName").text
            openid = xmlData.find("FromUserName").text

        if msgType == 'text':
            content = xmlData.find("Content").text
            reply_content = self.deal.text(content)

            return TextMsg(toUserName, fromUserName,
                           reply_content).structReply()

        elif msgType == 'image':
            mediaId = xmlData.find("MediaId").text

            ImageMsgObj = ImageMsg(toUserName, fromUserName, mediaId)
            return ImageMsgObj.structReply()

        elif msgType == 'event':
            eventKey = xmlData.find("EventKey").text

            reply_content = self.deal.event(eventKey)

            return TextMsg(toUserName, fromUserName,
                           reply_content).structReply()


class DealServer(object):
    def __init__(self, openid):
        self.openid = openid
        self.sn_pattern = re.compile(r"^[0-9a-zA-Z]{11,12}$")
        self.imei_pattern = re.compile(r"^[0-9]{15}$")
        self.event_list = get_event()

    def judge_imei(self, content):
        return re.match(self.imei_pattern, content) or re.match(
            self.sn_pattern, content)

    def judge_text(self, content):
        """判断文本格式

        `return`:  
            
            0: 格式错误
            1: 更多服务
            2: 批量查询
            3: 单个查询
        """
        content = content.replace(" ", "")
        if UserInfo.objects.query_current(self.openid) == "MOVE_SERVICES":
            if content in ["1", "2", "3", "4"]:
                return 1
            else:
                return 0
        elif "\n" in content:
            return 2
        elif self.judge_imei(content):
            return 3
        else:
            return 0

    def do_server(self, imei):
        if sys.platform == "win32":
            reply_content = "\n\n".join((DealService(
                openid=self.openid, current=self.current,
                imei=imei).main(), AccountInfo(self.openid).money_info()))
        else:
            reply_content = "爱锋妹正在为您查询中····· \n注意：请勿重复提交信息 \n如超过5分钟未出结果请联系客服 aifengchaxun1"
            main.delay("gh_8218d7e02312", self.openid, current, imei)

        return reply_content

    def text(self, content):
        code = self.judge_text(content)

        if code == 1:
            sign = int(content.replace("\n", ""))
            if sign == 1:
                event_key = "GUARANTEE_QUERY"
            elif sign == 2:
                event_key = "ID_QUERY"
            elif sign == 3:
                event_key = "ID_BLACK_WHITE_"
            elif sign == 4:
                event_key = "TYPE_CHECK"

            UserInfo.objects.update_current(self.openid, event_key)

            return "已切换{} \n等待时间: 5-30 秒 \n单价: {} 元 \n请勿重复提交 \n请发送 15 位 imei 或 12 位序列号查询".format(
                self.event_list[event_key]["name"],
                self.event_list[event_key]["count"])
        elif code == 2 or code == 3:

            try:
                self.current = UserInfo.objects.query_current(self.openid)
            except UserInfo.DoesNotExist:
                reply_content = "请在菜单栏选择要查询的项目"
            else:
                if code == 2:
                    reply_content = ""
                    imei_list = content.split("\n")
                    for value in imei_list:
                        reply_content = "\n".join(
                            (reply_content,
                             self.do_server(value.replace(" ", ""))))
                elif code == 3:
                    imei = content.replace(" ", "")
                    reply_content = self.do_server(imei)

                return reply_content

        elif code == 0:
            return "请输入正确的 IMEI 或 SN"

    def event(self, event_key):

        # try:
        #     UserInfo.objects.insert_user(self.openid, current=event_key)
        # except IntegrityError as exc:
        #     if exc.args[0] == 1062 and "Duplicate entry" in exc.args[1]:
        #         UserInfo.objects.update_current(self.openid, event_key)
        #     else:
        #         return "出现错误，请联系管理员"
        if UserInfo.objects.query_current(self.openid):
            UserInfo.objects.update_current(self.openid, event_key)
        else:
            UserInfo.objects.insert_user(self.openid, current=event_key)

        if event_key == "MOVE_SERVICES":
            return "回复数字切换查询\n1、保修查询\n2、ID查询\n3、ID黑白查询\n4、苹果型号查询"
        elif event_key == "EXTENDED_QR_CODE":
            return "该服务还没准备好哦，请稍后"
        elif event_key == "ACCOUNT_INFORMATION":
            return AccountInfo(openid=self.openid).account_information()
        else:
            try:
                reply_content = "已切换{} \n等待时间: 5-30 秒 \n单价: {} 元 \n请勿重复提交 \n请发送 15 位 imei 或 12 位序列号查询".format(
                    self.event_list[event_key]["name"],
                    self.event_list[event_key]["count"])
            except KeyError as exc:
                return "出现错误，请联系管理员"
                # if exc.args[0] == "count":
                #     "该服务还没准备好哦，请稍后"
            else:
                return reply_content


class TextMsg:
    def __init__(self, toUser, fromUser, recvMsg):
        self._toUser = toUser
        self._fromUser = fromUser
        self._recvMsg = recvMsg
        self._nowTime = int(time.time())

    def structReply(self):
        content = self._recvMsg
        text = """
                <xml>
                <ToUserName><![CDATA[{0}]]></ToUserName>
                <FromUserName><![CDATA[{1}]]></FromUserName>
                <CreateTime>{2}</CreateTime>
                <MsgType><![CDATA[text]]></MsgType>
                <Content><![CDATA[{3}]]></Content>
                </xml>
                """.format(self._fromUser, self._toUser, self._nowTime,
                           content)  #前面两个参数的顺序需要特别注意

        return text


class ImageMsg:
    def __init__(self, toUser, fromUser, mediaId):
        self._toUser = toUser
        self._fromUser = fromUser
        self._rediaId = mediaId
        self._nowTime = int(time.time())
        self._mediaId = mediaId

    def structReply(self):
        text = """
                <xml>
                <ToUserName><![CDATA[{0}]]></ToUserName>
                <FromUserName><![CDATA[{1}]]></FromUserName>
                <CreateTime>{2}</CreateTime>
                <MsgType><![CDATA[image]]></MsgType>
                <Image>
                <MediaId><![CDATA[{3}]]></MediaId>
                </Image>
                </xml>
                """.format(self._fromUser, self._toUser, self._nowTime,
                           self._mediaId)  #前面两个参数的顺序需要特别注意

        return text


if __name__ == "__main__":
    # os.chdir(
    #     os.path.dirname(
    #         "C:/UsersShadowMimosa/Documents/GitRepository/Workoo/now/wx_service/"
    #     ))
    body = """
            <xml>       
                <ToUserName><![CDATA[toUser]]></ToUserName>
                <FromUserName><![CDATA[FromUser]]></FromUserName>
                <CreateTime>123456789</CreateTime>
                <MsgType><![CDATA[event]]></MsgType>
                <Event><![CDATA[CLICK]]></Event>
                <EventKey><![CDATA[EVENTKEY]]></EventKey>
            </xml>
            """
    Analysis().reply(smart_str(body))