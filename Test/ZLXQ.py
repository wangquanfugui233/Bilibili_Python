import hashlib
import logging
import os
import requests
import time
import random


class ZLXQ:
    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(message)s')
        self.logger = logging.getLogger(__name__)
        self.headers = {
            "Host": "app.sjdhwu.com",
            "authorization": "",
            "yw-time": "",
            "yw-number": "10470706",
            "channel": "1",
            "versions": "331",
            "version-number": "331",
            "plat": "2",
            "yw-sign": "",
            "user-agent": "okhttp/4.9.0"
        }
        self.key = "E7XhdzLrCiwAYWEfEW31yfY2njTr9j9MHOuNouaNy2RNqPlvJwwYuqe5KPLnHNa9M"
        self.url = "https://app.sjdhwu.com/yw_api/v3/homeBubbleRewardInformation/"
        self.url1 = "https://app.sjdhwu.com/yw_api/v3/homeBubbleRewardCollection/"
        self.url_gift = 'https://app.sjdhwu.com/yw_api/v3/matchesGiftInformation/'
        self.url_wad = 'https://app.sjdhwu.com/yw_api/v3/watchAdsToIncreasePkTimes/'
        self.pk_ = 'https://app.sjdhwu.com/yw_api/v3/memberPk/'
        self.pk_info = 'https://app.sjdhwu.com/yw_api/v3/matchInformationV3/'
        self.pk_check = 'https://app.sjdhwu.com/yw_api/v3/pkInformationInterface/'
        self.pk_reload = 'https://app.sjdhwu.com/yw_api/v3/memberMatchV3/'
        self.money = 'https://app.sjdhwu.com/yw_api/v3/receiveBonusRewards/'
        self.sign = "https://app.sjdhwu.com/yw_api/v3/newSignIn"
        self.freeloopinfo = "https://app.sjdhwu.com/yw_api/v3/freeFlopInformation/"
        self.prizeget = "https://app.sjdhwu.com/yw_api/v3/prizeGet/"
        self.doubleprize = "https://app.sjdhwu.com/yw_api/v3/flopDoubled/"
        self.url_red = "https://app.sjdhwu.com/yw_api/v3/redEnvelopeRewardCollection/"
        self.red_double = "https://app.sjdhwu.com/yw_api/v3/redEnvelopeDoubledToReceive/"

    @staticmethod
    def get_timestamp():
        return int(time.time())

    @staticmethod
    def create_sign(secret):
        # ??????md5?????????
        new_md5 = hashlib.md5()
        new_md5.update(secret.encode('utf-8'))
        secret = new_md5.hexdigest().upper()
        return secret

    @staticmethod
    def fetch_cookie():
        cookies = os.getenv("zlcookie")
        cookie = cookies.split("@")
        return cookie

    def get_requests(self, url, sign):
        self.headers["yw-time"] = str(self.get_timestamp())
        self.headers["yw-sign"] = sign
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response.json()
            else:
                self.logger.error(response.json()['message'])
                return None
        except Exception as e:
            self.logger.error("??????????????????????????????{}".format(e))

    def post_requests(self, url, sign, data):
        self.headers["yw-time"] = str(self.get_timestamp())
        self.headers["yw-sign"] = sign
        try:
            response = requests.post(url, headers=self.headers, data=data)
            if response.status_code == 200:
                return response.json()
            else:
                self.logger.error(response.json()['message'])
                return None
        except Exception as e:
            self.logger.error("??????????????????????????????{}".format(e))

    def sign_in(self):
        str_key = "{}--10470706--{}ywaviTime--{}{}{}ywaviType--10{}".format(self.get_timestamp(), self.key,
                                                                            self.get_timestamp() - 15, self.key,
                                                                            self.key, self.key)
        sign = self.create_sign(str_key)
        data = {"ywaviType": 10, "ywaviTime": self.get_timestamp() - 15}
        self.logger.info("????????????")
        sign_in = self.post_requests(self.sign, sign, data)
        if sign_in:
            self.logger.info("????????????")
        else:
            pass

    def charge_bubbles(self):
        sign_str = "{}--10470706--{}--{}".format(self.get_timestamp(), self.key, self.key)
        sign = self.create_sign(sign_str)
        bubble_info = self.get_requests(self.url, sign)
        # self.logger.info(bubble_info)
        if bubble_info['data']:
            self.logger.info("???%s??????????????????" % len(bubble_info['data']))
            for i in bubble_info['data']:
                self.bubble(i['type'])
                time.sleep(1)
        else:
            self.logger.info("??????????????????,???????????????")

    def bubble(self, i):
        paras = {"type": i}
        sign_key = "{}--10470706--{}type--{}{}".format(self.get_timestamp(), self.key, i, self.key)
        sign = self.create_sign(sign_key)
        bubble = self.post_requests(self.url1, sign, paras)
        self.logger.info("???????????????????????????+ %s" % bubble['data']['number'])

    def check_pk(self):
        sign_str = "{}--10470706--{}--{}".format(self.get_timestamp(), self.key, self.key)
        sign = self.create_sign(sign_str)
        check_info = self.get_requests(self.pk_check, sign)
        self.logger.info("???pk????????? %s" % check_info['data']['remaining_pk_times'])
        return check_info['data']['remaining_pk_times']

    def match_pk(self):
        sign_str = "{}--10470706--{}--{}".format(self.get_timestamp(), self.key, self.key)
        sign = self.create_sign(sign_str)
        pk_info = self.get_requests(self.pk_info, sign)
        return pk_info['data']

    def reload_man(self):
        sign_str = "{}--10470706--{}--{}".format(self.get_timestamp(), self.key, self.key)
        sign = self.create_sign(sign_str)
        pk_info = self.post_requests(self.pk_reload, sign, None)
        if pk_info:
            self.logger.info("??????pk??????%s" % pk_info['message'])
        else:
            self.logger.info("??????pk_info: %s" % pk_info)

    def watch_ad(self):
        str_key = "{}--10470706--{}--{}".format(self.get_timestamp(), self.key, self.key)
        sign = self.create_sign(str_key)
        self.headers[
            'ymavi'] = "OG9HQXNtT1ljdlRGaEJzQmRhZFpPUlk0UXZ6d0JwT3hKVjRhbC9iZlhvUkdMWUd2MTRZUzB0Y3k4a20vbWRCMwo="
        ad_info = self.post_requests(self.url_wad, sign, None)
        if ad_info:
            self.logger.info("??????????????????")
            return True
        else:
            return False

    def user_info(self):
        str_key = "{}--10470706--{}--{}".format(self.get_timestamp(), self.key, self.key)
        sign = self.create_sign(str_key)
        user_info = self.get_requests(self.pk_check, sign)
        if user_info:
            self.logger.info("???????????????%s -- ??????%s --??????%s" % (
                user_info['data']['member']['nickname'], user_info['data']['member']['balance'],
                user_info['data']['member']['gold_coins']))
        else:
            self.logger.info("????????????????????????")

    @staticmethod
    def screen_match(pk_info):
        people = []
        for i in pk_info:
            if i['award_name'] == '':
                people.append(i['id'])
            else:
                continue
        return people

    def cycle_match(self):
        while True:
            num = self.check_pk()
            if num == '0':
                self.logger.info("??????15???")
                time.sleep(15)
                result = self.watch_ad()
                if result:
                    continue
                else:
                    self.logger.info("????????????pk")
                    break
            pk_number = self.match_pk()
            pk_people = self.screen_match(pk_number)
            if pk_people:
                for i in pk_people:
                    self.pk_ing(i)
                    time.sleep(3)
            else:
                self.logger.info("?????????????????????,??????????????????")
                self.reload_man()

    def pk_ing(self, i):
        data = {"match_id": i}
        mat_key = "{}--10470706--{}match_id--{}{}".format(self.get_timestamp(), self.key, i, self.key)
        sign = self.create_sign(mat_key)
        pk_result = self.post_requests(self.pk_, sign, data)
        if pk_result:
            self.logger.info("pk????????? %s??????" % pk_result['data']['award'][0]['number'])
        else:
            self.logger.info("pk????????? %s" % pk_result['message'])

    def fetch_money(self):
        sign_str = "{}--10470706--{}--{}".format(self.get_timestamp(), self.key, self.key)
        sign = self.create_sign(sign_str)
        self.headers[
            'ymavi'] = "OG9HQXNtT1ljdlRGaEJzQmRhZFpPUlk0UXZ6d0JwT3hKVjRhbC9iZlhvUkdMWUd2MTRZUzB0Y3k4a20vbWRCMwo="
        money_info = self.post_requests(self.money, sign, None)
        if money_info:
            self.logger.info(money_info['data'])
        else:
            pass

    def free_flop(self):
        str_key = "{}--10470706--{}--{}".format(self.get_timestamp(), self.key, self.key)
        sign = self.create_sign(str_key)
        data = self.get_requests(self.freeloopinfo, sign)
        if data:
            self.logger.info("?????????????????????%s" % data['data']['flop_num'])
            return data['data']['flop_num']
        else:
            self.logger.info("??????????????????????????????")

    def prize_flop(self):
        str_key = "{}--10470706--{}--{}".format(self.get_timestamp(), self.key, self.key)
        sign = self.create_sign(str_key)
        data = self.get_requests(self.prizeget, sign)
        if data:
            if data['data']['contens'] == "":
                self.logger.info(
                    "?????????%s" % (data['data']['name']))
                return None
            else:
                self.logger.info(
                    "?????????%s --%s" % (data['data']['name'], data['data']['contens']))
                return data['data']['association_id']
        else:
            self.logger.info("????????????")

    def double_flop(self, i):
        data = {"association_id": i}
        sign_key = "{}--10470706--{}association_id--{}{}".format(self.get_timestamp(), self.key, i, self.key)
        sign = self.create_sign(sign_key)
        result = self.post_requests(self.doubleprize, sign, data)
        if result:
            self.logger.info("?????????%s" % result['data']['contens'])
        else:
            self.logger.info("????????????")

    def cyc_flop(self):
        self.logger.info("????????????")
        num = self.free_flop()
        for i in range(int(num)):
            self.logger.info("???%s?????????" % (i + 1))
            as_id = self.prize_flop()
            if as_id:
                self.double_flop(as_id)
            else:
                self.logger.info("?????????")
            self.logger.info("????????????")
            if i == int(num) - 1:
                break
            time.sleep(random.randint(15, 17))

    def red_reward(self):
        str_key = "{}--10470706--{}--{}".format(self.get_timestamp(), self.key, self.key)
        sign = self.create_sign(str_key)
        data = self.post_requests(self.url_red, sign, None)
        if data:
            self.logger.info("?????????%s" % data['data']['number'])
            return data['data']['association_id']
        else:
            self.logger.info("??????????????????")
            return None

    def red_double_reward(self, i):
        data = {"association_id": i}
        sign_key = "{}--10470706--{}association_id--{}{}".format(self.get_timestamp(), self.key, i, self.key)
        sign = self.create_sign(sign_key)
        result = self.post_requests(self.red_double, sign, data)
        if result:
            self.logger.info("?????????%s" % result['data']['number'])
        else:
            self.logger.info("????????????")

    def red(self):
        self.logger.info("??????????????????")
        i = self.red_reward()
        if i:
            self.red_double_reward(i)
        else:
            pass

    def run(self):
        cookies = self.fetch_cookie()
        for i in cookies:
            self.headers['authorization'] = i
            self.user_info()
            self.sign_in()
            self.logger.info("wait 15-17s")
            time.sleep(random.randint(15, 17))
            self.charge_bubbles()
            self.logger.info("wait 15-17s")
            time.sleep(random.randint(15, 17))
            self.fetch_money()
            self.logger.info("wait 15-17s")
            time.sleep(random.randint(15, 17))
            self.cycle_match()
            self.logger.info("wait 15-17s")
            time.sleep(random.randint(15, 17))
            self.cyc_flop()
            self.red()


if __name__ == "__main__":
    zlxq = ZLXQ()
    zlxq.run()
