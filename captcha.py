#. _*_ encoding=utf-8 -*_
#. __author__="monian"
#. Date:2018/7/14

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
import time,random
from PIL import Image
from io import  BytesIO

class Login():
    def __init__(self):
        self.email='632388667@qq.com'
        self.password='6126859xd'
        self.browser = webdriver.Chrome()
        self.browser.maximize_window()
        self.wait=WebDriverWait(self.browser,10)
        self.browser.get('https://auth.geetest.com/login/')
        self.action=ActionChains(self.browser)

    def user(self):
        email=self.browser.find_element(By.XPATH,'//*[@id="base"]/div[2]/div/div/div[3]/div/form/div[1]/div/div[1]/input')
        password=self.browser.find_element(By.XPATH,'//*[@id="base"]/div[2]/div/div/div[3]/div/form/div[2]/div/div[1]/input')
        self.action.click(email).perform()
        time.sleep(1)
        email.send_keys(self.email)
        time.sleep(1)
        self.action.click(password).perform()
        time.sleep(1)
        password.send_keys(self.password)
    def position(self):
        image=self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_canvas_img')))
        location=image.location
        location['x']=location['x']
        location['y']=location['y']
        size=image.size
        size['height']=size['height']
        size['width']=size['width']
        rangle = (int(location['x']), int(location['y']), int(location['x'] + size['width']),
          int(location['y'] + size['height']))
        return rangle

    def get_position1(self):
        #获取图片位置
        button1=self.browser.find_element(By.CLASS_NAME,'geetest_radar_tip')
        self.action.click(button1).perform()
        #self.browser.switch_to.frame(self.browser.find_element_by_tag_name("iframe"))
        #image1=self.browser.find_element(By.XPATH,'/html/body/div[3]/div[2]/div[1]/div/div[1]/div[1]/div/a/div[1]/canvas')
        rangle=self.position()
        return rangle

    def get_position2(self):
        button2=self.browser.find_element(By.CLASS_NAME,'geetest_slider_button')
        button2.click()
        rangle=self.position()
        return rangle

    def image(self,rangle):
        screenshot=self.browser.get_screenshot_as_png()
        screenshot=Image.open(BytesIO(screenshot))
        captche=screenshot.crop(rangle)
        return captche

    def get_image1(self):
        rangle=self.get_position1()
        time.sleep(2)
        captche=self.image(rangle)
        width=captche.size[0]
        height=captche.size[1]
        #captche = captche.resize((int(width*0.8), int(height*0.8)),Image.ANTIALIAS)
        captche.save('a.png')
        return captche

    def get_image2(self):
        rangle=self.get_position2()
        time.sleep(3)
        captche=self.image(rangle)
        width=captche.size[0]
        height=captche.size[1]
        #captche = captche.resize((int(width*0.8), int(height*0.8)),Image.ANTIALIAS)
        captche.save('b.png')
        return captche

    def is_pixel_equal(self, image1, image2, x, y):
        #判断两个像素是否相同
        pixel1=image1.load()[x,y]
        pixel2=image2.load()[x,y]
        a=pixel1[0]-pixel2[0]
        b=pixel1[1]-pixel2[2]
        c=pixel1[2]-pixel2[2]
        threshold=60
        if abs(a)<threshold and abs(b)<threshold and abs(c)<threshold:
            return True
        else:
            return False

    def get_gap(self, image1, image2):
        #获得缺口
        left=60    #滑片宽度
        for i in range(left, image1.size[0]):
            for j in range(image1.size[1]):
                if not self.is_pixel_equal(image1, image2, i, j):
                    left = i
                    return left
        return left

    def get_track(self,distance):
        #获得滑块的运动轨迹
        track=[]
        current=0
        v=0
        t=0.2
        m=distance*0.35
        n=distance*0.7
        while current<distance:
            if current<n:
                a=4
            else:
                a=-6
            v0=v
            v=v0+a*t
            move=v0*t+0.5*a*t*t
            current+=move
            track.append(round(move))
        return track

    def move_to_grap(self):
        image1=self.get_image1()
        image2=self.get_image2()
        success=self.browser.find_element(By.CLASS_NAME,'geetest_success_radar_tip_content')
        slider=self.browser.find_element(By.CLASS_NAME,'geetest_slider_button')
        button=self.browser.find_element(By.CLASS_NAME,'ivu-btn')
        # +20多向前移动20的距离
        distance=(self.get_gap(image1,image2)-6)+20
        print(distance)
        track=self.get_track(distance)
        print(track)
        back_tracks=[-3,-3,-2,-2,-2,-2,-2,-1,-1,-1,-1]     #待会回移的轨迹段
        # while success.text!='验证成功':
        # for i in range(0,2):
        self.action.click_and_hold(slider)
        for x in track:
           self.action.move_by_offset(xoffset=x,yoffset=0)
        time.sleep(0.5)
        for y in back_tracks:
            self.action.move_by_offset(xoffset=y,yoffset=0)
        self.action.move_by_offset(xoffset=-3,yoffset=0)         #小范围震荡
        self.action.move_by_offset(xoffset=3,yoffset=0)
        time.sleep(0.5)
        self.action.release(slider)
        self.action.perform()
        time.sleep(2)
        # print(success.text)
        # if success.text=='验证成功':
        self.action.click(button).perform()




l=Login()
l.user()
l.move_to_grap()
