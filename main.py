from curl_cffi import requests, CurlOpt
import pyotp
from loguru import logger
import time
import os

# 本程序自动购买功能仅适用于开启基于OTP二次验证的账号



"""
添加微信号:fengzhongweixiao1314
进入程序交流群,使用教程及后续代码更新将在交流群发布
交流群将会不定时空投nft装饰品及不同品级沙漏作为福利哦
"""

logger.error("添加微信号:fengzhongweixiao1314")
logger.error("进入程序交流群,使用教程及后续代码更新将在交流群发布")
logger.error("交流群将会不定时空投nft装饰品及不同品级沙漏作为福利哦")

logger.info("添加微信号:fengzhongweixiao1314")
logger.info("进入程序交流群,使用教程及后续代码更新将在交流群发布")
logger.info("交流群将会不定时空投nft装饰品及不同品级沙漏作为福利哦")


logger.success("添加微信号:fengzhongweixiao1314")
logger.success("进入程序交流群,使用教程及后续代码更新将在交流群发布")
logger.success("交流群将会不定时空投nft装饰品及不同品级沙漏作为福利哦")


logger.error("本程序仅供学习交流使用,禁止转载及出售,侵权请联系删除")
logger.info("本程序仅供学习交流使用,禁止转载及出售,侵权请联系删除")
logger.success("本程序仅供学习交流使用,禁止转载及出售,侵权请联系删除")

def convert_cookies_to_dict(t_cookies):
    if t_cookies == "":
        return {}
    t_cookies = dict([l.split("=", 1) for l in t_cookies.split("; ")])
    return t_cookies



_cookies = ""  # 输入账号的Cookies 如果不输入将会在扫到合适沙漏时使用默认浏览器弹出购买页面
cookies = convert_cookies_to_dict(_cookies)

deviceId = ""  # 输入浏览器的X-Device-Id 如果不输入将会在扫到合适沙漏时使用默认浏览器弹出购买页面

sessionId = ""  # 输入浏览器的X-Session-Id 如果不输入将会在扫到合适沙漏时使用默认浏览器弹出购买页面

twoFactor = ""  # 输入账号绑定的谷歌二次验证密钥,开源项目,不会上传你的二次验证密钥, 如果不输入将会在扫到合适沙漏时使用默认浏览器弹出购买页面
# 二次验证基于本地时间,请确保本地时间准确

totp = None
if twoFactor != "":
    totp = pyotp.TOTP(twoFactor)

# 设置市场扫货参数

optionName = "Hourglass_Epic"  # 该参数在商城的Items页面可以找到 例:https://openloot.com/items/BT0/Hourglass_Epic 取后面的Hourglass_Epic
highPrice = 200  # 设置白板沙漏自动买入最高价格 如过不扫白板沙漏 可以设置为0
lowTime = 1  # 设置沙漏时间区间低值 单位小时
highTime = 300  # 设置沙漏时间区间高值 单位小时
highTimePrice = 5  # 减去地板价后的最高时间价格 当highTimePrice设置为0时,将只按地板价扫白板沙漏或装饰品nft
maxPage = 3  # 最多扫到第几页,openloot有请求频率限制,不要扫太多页避免本机IP被拉黑,扫白板或装饰品nft时只会获取第一页
delayTime = 10  # 每次扫市场后等待秒数
maxBuyNum = 1 # 最大购入几个后停止程序

# 情景一   highPrice 设置300  highTimePrice设置0 即只扫白板沙漏或其他Nft
# 此时扫到地板价300 则会自动购入 地板价高于300 哪怕是300.01也不会触发自动购入流程

# 情景二   highPrice 设置500  lowTime设置50  highTime设置100  highTimePrice设置2.8  Time相关的3个参数只针对沙漏生效 且设置后将不会购买白板沙漏
# 此时扫到地板价 501 则以highPrice设置的500为地板价计算时间价格   如果扫到了一个价格724 时间80小时 则计算出时间价格刚好为2.8 符合限制条件 触发自动购入流程
# 此时扫到地板价 499 则以499为地板价计算时间价格 满足条件将自动购入

def auth(ordersId,errorNum=0):
    if errorNum > 8:
        return
    buyHeaders = {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "content-type": "application/json",
        "pragma": "no-cache",
        "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "x-client-id": "marketplace",
        "x-device-id": deviceId,
        "x-is-mobile": "false",
        "x-session-id": sessionId,
        "origin":"https://openloot.com",
        "Referer": f"https://openloot.com/checkout?orderIds={ordersId}",
    }
    postData = {"authType":"app","code":totp.now(),"removeType":"app"}
    r = requests.post(
        "https://api.openloot.com/auth/upgrade/twofactor",
        impersonate="chrome120",
        headers=buyHeaders,
        cookies=cookies,
        json=postData
    )
    try:
        if r.status_code == 403:
            data = r.json()
            if (data["error"] == "Invalid authentication code"):
                logger.error("二次验证不正确,正在重试")
                time.sleep(0.5)
                auth(ordersId,errorNum+1)
                return
    except Exception as e:
        logger.error(f"error : {e}")
        auth(ordersId,errorNum+1)
        return
    if r.status_code != 200:
        logger.error(f"二次验证出错,http状态码{str(r.status_code)},返回内容{r.text}")
    logger.success("二次验证成功,继续跳转购买")
    buy(ordersId)
    return

buyNum = 0
def buy(ordersId,errorNum = 0):
    if errorNum > 8:
        return
    if cookies == "" or  deviceId == "" or sessionId == "" or twoFactor == "":
        os.system(f"start https://openloot.com/checkout?orderIds={ordersId}")
        global buyNum
        buyNum = buyNum + 1
        return
    buyHeaders = {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "content-type": "application/json",
        "pragma": "no-cache",
        "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "x-client-id": "marketplace",
        "x-device-id": deviceId,
        "x-is-mobile": "false",
        "x-session-id": sessionId,
        "origin":"https://openloot.com",
        "referer": f"https://openloot.com/checkout?orderIds={ordersId}",
    }
    postData = {"orders":[ordersId],"paymentMethod":"wallet"}
    r = requests.post(
        "https://api.openloot.com/v2/market/secondary/orders",
        impersonate="chrome120",
        headers=buyHeaders,
        cookies=cookies,
        json=postData
    )
    try:
        if r.status_code == 403:
            data = r.json()
            if (data["error"] == "2FA authentication required"):
                logger.info(f"正在二次验证")
                auth(ordersId)
                return
        elif r.status_code == 500:
            data = r.json()
            if (data["code"] == "Error"):
                logger.error(f"购买{ordersId}时出错,{data["message"]}")
                return
    except Exception as e:
        logger.error(f"error : {e}")
        buy(ordersId,errorNum+1)
        return
    if r.status_code != 200:
        logger.error(f"购买{ordersId}时出错,http状态码{str(r.status_code)},返回内容{r.text}")
        return
    logger.success(f"购买{ordersId}成功,{r.text}")
    buyNum = buyNum + 1
    return
headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding":"gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
}
while True:
    
    if highTimePrice <= 0:
        r = requests.get(
            f"https://api.openloot.com/v2/market/listings/BT0_{optionName}/items?onSale=true&page=1&pageSize=5&sort=price%3Aasc",
            impersonate="chrome120",
            headers=headers,
        )
        if r.status_code != 200:
            logger.error(f"请求第1页时出错,http状态码{str(r.status_code)},返回内容{r.text}")
            time.sleep(delayTime)
            continue
        data = r.json()
        for item in data["items"]:
            if item["price"] <= highPrice:
                logger.info(f"获取到 #{str(item["item"]["issuedId"])} 价格为 $ {str(item["price"])} 符合购入条件")
                buy(item["orderId"])
                if buyNum >= maxBuyNum:
                    break
            else:
                break
    
    else:
        floorPrice = 0
        getFloor = False
        for i in range(maxPage):
            pageIndex = i + 1
            logger.info(f"正在加载第{str(pageIndex)}页")
            r = requests.get(
                f"https://api.openloot.com/v2/market/listings/BT0_{optionName}/items?onSale=true&page={str(pageIndex)}&pageSize=50&sort=price%3Aasc",
                impersonate="chrome120",
                headers=headers,
            )
            if r.status_code != 200:
                logger.error(f"请求第{str(pageIndex)}页时出错,http状态码{str(r.status_code)},返回内容{r.text}")
                break
            data = r.json()
            for item in data["items"]:
                if getFloor == False and item["price"] < highPrice:
                    floorPrice = item["price"]
                    getFloor = True
                    logger.info(f"当前地板价格 $ {str(floorPrice)}")
                elif getFloor == False and item["price"] >= highPrice:
                    floorPrice = highPrice
                    getFloor = True
                    logger.info(f"当前地板价格 $ {str(floorPrice)}")
                
                if item["item"]["extra"] != None and item["item"]["extra"]["attributes"][0]["name"] == "TimeRemaining":
                    hour = float(item["item"]["extra"]["attributes"][0]["value"] ) / 60
                    if hour <= 0:
                        continue
                    timePrice = (item["price"] - floorPrice) / hour
                    #print(timePrice)
                    if timePrice > highTimePrice:
                        continue
                    if lowTime <= hour and hour <= highTime:
                        logger.info(f"获取到 #{str(item["item"]["issuedId"])} 价格为 $ {str(item["price"])} * 时间 {str(round(hour, 2))}小时 * 时间价格 $ {str(round(timePrice, 2))} 符合购入条件")
                        buy(item["orderId"])
                        if buyNum >= maxBuyNum:
                            break
            if buyNum >= maxBuyNum:
                break
            time.sleep(1)
    if buyNum >= maxBuyNum:
        break
    time.sleep(delayTime)


    
                
                

logger.success("程序执行完毕")



