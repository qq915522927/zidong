# coding=utf8

#####################################
# 功能 ： 测试职位申请流程
# 说明 ： 验证码需手动输入
#####################################
from selenium import webdriver
import time
from Queue import Queue
import unittest

driver = webdriver.PhantomJS()
_start_url = 'https://cn.app.seedlinktech.com/drago/position/3657/'
_login_url = 'https://cn.app.seedlinktech.com/drago/candidate/login/?next=/drago/answer/basic/&pid=3657&signup=true'
_info_url = 'https://cn.app.seedlinktech.com/drago/answer/basic/?pid=3657'
_q1_ur = 'https://cn.app.seedlinktech.com/drago/question/hunting/?pid=3657&nowPage=1'
_thank_url = 'https://cn.app.seedlinktech.com/drago/application/thankyou/?pid=3657&from=oeq'
answer1 =u'''
改变自己的是一个就是运动吧，高中时候身体不好，得咽喉炎，嗓子坏了，各种萎靡不振，在别人眼中就是无精打采。
原本我是很好强的人，初中考试经常拿第一，到了高中虽然都很强，但我也没有示弱的意思。但是嗓子坏了后，说话就变少了很多，
很多想说的话因为嗓子疼没说，同时也避免了很多不该说的话。到大学从大二开始，就开始注重自己的健康了，应为之前熬夜，游戏，
已经非常亚健康了，然后就开始锻炼了。开始觉得跑步好累，一天只跑两圈，后来渐渐觉得不累了，越跑越多，一段时间每条跑25圈，
不过确实太猛了，跑的跟腱疼。经过锻炼身体状况好了不少，精力也集中了，嗓子也有好转。
'''
answer2 =u'''
最难的时候就是高三吧，那时候身体状况极差，基本每天都是感冒的状态，每天睡眠都不够，加上嗓子坏了的
缘故，我的性格完全变了，当时觉得上学毫无意义，完全没有动力去上学考试，当时甚至想不考大学了，有一天下午
我没去上课，骑车去了一个很偏的山区，回来的路上遇到妈妈，她刚从医院出来，以为我出事了，去医院找我。她很生气，
更多的是着急。然后我去了学校，班主任也刚从外面找我回来，同学们都在教室外等我。然后我就感觉没事了，因为周围的爱很多。
'''
answer3=u'''
就拿这个小任务来说吧，刚开始就用函数一步一步来吧，然后想起来了这些输出的功能正好可以做成装饰器，然后就编写了装饰器，然后
写着写着又发现这不符合面向对象的思想，那就改成类吧，然后既然是测试那就用unittest单元测试模块吧，虽然不太懂单元测试，但总觉得这样比较好
然后就改了。面对这类问题，在自己精力和时间充沛的情况下，即使花费更多的精力，会尽量的去向更优的方案靠拢。
'''
def output(func):
    '''
        输出信息
    '''

    def wrap(dsc, *args,**kwargs):
        print(dsc)
        return func(dsc, *args,**kwargs)

    return wrap


def resultMsg(func):
    """
       判断是否通过，并打印提示
       result:true or false
    """

    def wrap(*args,**kwargs):
        result = func(*args,**kwargs)
        if result is True:
            print 'pass'
        else:
            print '[X]not pass'
        print '--------------------------'
        return result

    return wrap


class JobApplicaion(object):
    @staticmethod
    @resultMsg
    @output
    def index_n1(dsc, result, driver):
        '''

        :param dsc: 描述
        :param result: 预期跳转的url
        :return:
        '''
        time.sleep(2)

        driver.find_element_by_xpath('/html/body/div[4]/div/div/footer/div/div/a').click()
        time.sleep(1)
        if result == driver.current_url:
            return True
        else:
            return False

    @staticmethod
    @resultMsg
    @output
    def register_n2(dsc,phone, check, result, driver):
        '''
        注册页面
        :param dsc: ，描述
        :param phone: 电话或email

        :param check: 是否同意协议
        :param result: 预期的结果
        :param driver:driver
        验证码手动输入
        :return:
        '''

        inp_username = driver.find_element_by_id("sign-up-user-name")
        inp_cap = driver.find_element_by_id("id_captcha_1")
        js = 'document.querySelectorAll("#privacy")[0].style.display="block";'
        driver.execute_script(js)
        inp_check =  driver.find_element_by_xpath('//*[@id="privacy"]')
        inp_username.clear()
        inp_cap.clear()

        inp_username.send_keys(phone)
        code = raw_input('please type capatcha:')
        inp_cap.send_keys(code)

        if check:
            if inp_check.is_selected():
                inp_check.click()
                inp_check.click()
            else:
                inp_check.click()
        else:
            if inp_check.is_selected():
                inp_check.click()
        submit = driver.find_element_by_id("login-next")
        submit.click()
        time.sleep(2)
        # a = submit.get_attribute('disabled')
        try:
            if submit.get_attribute('disabled') == u'true':
                if check is False:
                    return True
                else:
                    return False

        except:
            # 没找到按钮说明页面跳转了
            if dsc == u'注册信息正确':
                if driver.current_url == _info_url:
                    return True
                else:
                    return False

        if dsc == u'测试手机号或邮箱错误':
            # 判断phone是否符合标准
            error_phone = driver.find_element_by_xpath('//*[@id="sign-up-invalid-user-name"]/article/p')
            if error_phone.is_displayed():
                return True
            else:
                return False

        if dsc == u'测试验证码错误':
            error_code = driver.find_element_by_xpath('//*[@id="sign-up-invalid-captcha"]/article/p')
            if error_code.is_displayed():
                return True
            else:
                return False

    @staticmethod
    @resultMsg
    @output
    def info_n3(dsc, name, phone, email, pwd, driver):
        '''
        填写信息页面
        :param dsc:
        :param name:
        :param phone:
        :param email:
        :param pwd:
        :param driver:
        :return:
        '''
        time.sleep(2)
        inp_name = driver.find_element_by_xpath('//*[@id="name"]/input')
        inp_phone = driver.find_element_by_xpath('//*[@id="mobile"]/input')
        inp_email = driver.find_element_by_xpath('//*[@id="email"]/input')
        inp_pwd = driver.find_element_by_xpath('//*[@id="password-input-field"]')
        btn = driver.find_element_by_id('next')

        inp_name.clear()
        inp_phone.clear()
        inp_email.clear()
        inp_pwd.clear()

        inp_name.send_keys(name)
        inp_phone.send_keys(phone)
        inp_email.send_keys(email)
        inp_pwd.send_keys(pwd)
        btn.click()
        time.sleep(1.5)

        if name == '' or phone == '' or email == '' or pwd == '':
            #填入信息中任何一个为空
            correct_count = 0
            empty_list = []
            #获取预期为空的错误信息，存入列表
            for x, y in {u'请输入姓名': name, u'请输入手机号': phone, u'请输入邮箱': email, u'密码不应为空': pwd}.items():
                if y == '':
                    empty_list.append(x)
            #找到所有的错误提示元素
            errors = driver.find_elements_by_xpath('//em[@class="wrong animated bounceInRight"]')
            time.sleep(1)
            #遍历所有的错误提示，如果他为displayed且text值在预期的列表中，则说明这个错误提示符合预期
            for error in errors:
                if error.text in empty_list:
                    correct_count += 1
            # print correct_count
            #最后比较所有的符合预期的错误信息数量是否和预期数量相等，相等则true
            if correct_count == len(empty_list):
                return True
            else:
                return False

        if dsc == u'邮箱格式不正确':
            if driver.find_element_by_xpath('//*[@id="email-null"]/em').is_displayed():
                return True
            else:
                return False

        if dsc == u'电话格式不正确':
            if driver.find_element_by_xpath('//*[@id="mobile-null"]/em').is_displayed():
                return True
            else:
                return False

        if dsc == u'密码格式不正确':
            err_pwd = driver.find_element_by_xpath('//*[@id="password"]/div[1]/em')

            if err_pwd.is_displayed():
                # and err_pwd.text == u'您的密码长度须在8到20位之间，并至少包含以下4种类型中的3种：英文大写、英文小写、数字及符号。':
                return True
            else:
                return False
        if dsc == u'电话已被使用':
            err_pwd = driver.find_element_by_xpath('//*[@id="mobile-wrong"]/em')

            if err_pwd.is_displayed():
                # and err_pwd.text.decode('utf8') == u'此号码已经被使用，请使用其他号码。':
                return True
            else:
                return False

        if dsc == u'邮箱已被使用':


            err_pwd = driver.find_element_by_xpath('//*[@id="email-wrong"]/em')

            if err_pwd.is_displayed():
                # and err_pwd.text == u'此邮箱已经被使用，请使用其他邮箱。':
                return True
            else:
                return False

        if dsc == u'信息正确':
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="know"]').click()
            time.sleep(1)

            if driver.current_url == _q1_ur:
                return True
            else:
                return False

    @staticmethod
    @resultMsg
    @output
    def q1_n4(dsc, answer, driver):
        '''
        三个问题的页面
        :param dsc:
        :param answer:
        :param driver:
        :return:
        '''
        inp_answer = driver.find_element_by_id('post')
        inp_answer.send_keys(answer)
        time.sleep(1)
        #获取字数
        nums = driver.find_elements_by_xpath('//div[@class="open-ended-box"]//p[@class="at-least"]/span')
        l = filter(lambda num:num.text!='',nums)
        num = l[0].text



        if len(answer) < 100:
            if len(answer) == int(num):
                return True
            else:
                return False
        if len(answer) >= 100:
            #获取点击按钮
            btns = driver.find_elements_by_xpath(
                '//footer//aside[2]/button[1]')
            btn_l = filter(lambda btn:btn.text!='',btns)
            btn = btn_l[0]
            if btn.get_attribute('disabled') != u'true':

                time.sleep(1)
                #获取点击前的页码
                orign_indexs = driver.find_elements_by_xpath(
                    '//div[@class="open-ended-box"]//h2/em')
                o_l=filter(lambda orgin:orgin.text!='',orign_indexs)
                orign_index=o_l[0].text
                if int(orign_index) in [1,2]:

                    # if orign_index == u'':
                    #     orign_index = 1
                    btn.click()
                    time.sleep(1)
                    # 页码
                    indexs = driver.find_elements_by_xpath('//div[@class="open-ended-box"]//h2/em')
                    i_l = filter(lambda index: index.text != '',indexs)
                    index = i_l[0].text

                    if int(index) == int(orign_index) + 1:
                        return True
                else:
                    # 右下角提示信息
                    finish_info = driver.find_element_by_xpath(
                        '/html/body/div[4]/div/div/div[1]/div/div[3]/div/div[3]/article/p/em[1]').text
                    btn.click()
                    time.sleep(1)
                    btn_confr = driver.find_element_by_id('finish-save')
                    if btn_confr.is_displayed():
                            # and finish_info == u"点击 '完成'，答案会被自动保存":
                        btn_confr.click()
                        time.sleep(2)
                        driver.save_screenshot('1.png')
                        if driver.current_url == _thank_url:
                            return True
            else:
                return False


class JobAppTest(unittest.TestCase):
    register_task_list = [(u'测试手机号或邮箱错误', '1878778', True, u'请输入手机或邮箱', driver),
                          (u'测试验证码错误', '{:d}1'.format(int(time.time())), True, u'请正确输入图中文字或点击图片换一张', driver),
                          (u'测试不同意协议', '{:d}1'.format(int(time.time())), False, u'', driver),
                          (u'注册信息正确', '{:d}@qq.com'.format(int(time.time())), True, u'', driver), ]

    info_list = [
        (u'用户名为空', '', '{:d}1'.format(int(time.time())), '{:d}@qq.com'.format(int(time.time())), 'abcABC123', driver),
        (u'电话为空', 'wuzhiwen', '', '{:d}@qq.com'.format(int(time.time())), 'abcABC123', driver),
        (u'邮件为空', 'wuzhiwen', '{:d}1'.format(int(time.time())), '', 'abcABC123', driver),
        (u'密码为空', 'wuzhiwen', '{:d}1'.format(int(time.time())), '{:d}@qq.com'.format(int(time.time())), '', driver),
        (u'邮箱格式不正确', 'wuzhiwen', '{:d}1'.format(int(time.time())), '23423423', 'abcABC123', driver),
        (u'电话格式不正确', 'wuzhiwen', '453453gdf', '23423423', 'abcABC123', driver),
        (u'密码格式不正确', 'wuzhiwen', '{:d}1'.format(int(time.time())), '{:d}@qq.com'.format(int(time.time())), 'abc123123',
         driver),
        (u'电话已被使用', 'wuzhiwen', '18301929561', '{:d}@qq.com'.format(int(time.time())), 'ABCa3bc123123', driver),
        (u'邮箱已被使用', 'wuzhiwen', '{:d}1'.format(int(time.time())), '915522927@qq.com', 'ABCa3bc123123', driver),
        (u'信息正确', 'wuzhiwen', '{:d}1'.format(int(time.time())), '{:d}@qq.com'.format(int(time.time())), 'ABCabc123123',
         driver),

    ]
    # register_task_list = [  (u'注册信息正确', '{:d}@qq.com'.format(int(time.time())), True, u'', driver), ]
    # info_list =[(u'信息正确', 'wuzhiwen', '{:d}1'.format(int(time.time())), '{:d}@qq.com'.format(int(time.time())), 'ABCabc123123',
    #      driver),]
    answer_list = [(u'问题一回答少于100字',u'少于100字',driver),
                   (u'问题一回答多于100字',answer1,driver),
                   (u'问题二回答少于100字',u'少于100字',driver),
                   (u'问题二回答多于100字',answer2,driver),
                   (u'问题三回答少于100字',u'少于100字',driver),
                   (u'问题三回答多于100字',answer3,driver),
                   ]
    # def __init__(self):
    #
    #     # super(JobAppTest,self).__init__(self)
    #     # self.driver = webdriver.PhantomJS()
    #     self.driver.get(_start_url)

    def setUp(self):
        pass
        # self.driver = webdriver.PhantomJS()
        # self.driver.get(_start_url)

    def tearDown(self):
        pass
        # print 'teardown'
        # self.driver.close()

    # def test_init(self):
    #     # self.driver = webdriver.PhantomJS()
    #     self.driver.get(_start_url)

    def test_a_index_n1(self):
        time.sleep(1)
        result = JobApplicaion.index_n1(u'入口页测试', _login_url, driver)
        driver.save_screenshot('captcha.png')
        self.assertTrue(result)

    def test_b_register_n2(self):
        time.sleep(1)
        for item in self.register_task_list:
            result = JobApplicaion.register_n2(*item)
            self.assertTrue(result)

    def test_c_info_n3(self):
        for item in self.info_list:
            result = JobApplicaion.info_n3(*item)
            self.assertTrue(result)

    def test_d_q_n4(self):
        for item in self.answer_list:
            result = JobApplicaion.q1_n4(*item)
            self.assertTrue(result)

if __name__ == '__main__':
    driver.get(_start_url)
    unittest.main()
    driver.close()

    # driver = webdriver.PhantomJS()

    # register_task_list = [(u'测试手机号或邮箱错误', '1878778', True, u'请输入手机或邮箱', driver),
    #                       (u'测试验证码错误', '18301929561', True, u'请正确输入图中文字或点击图片换一张', driver),
    #                       (u'测试不同意协议', '18301929561', False, u'', driver),
    #                       (u'注册信息正确', '{:d}@qq.com'.format(int(time.time())), True, u'', driver), ]
    # info_list = [
    #     (u'用户名为空', '', '{:d}1'.format(int(time.time())), '{:d}@qq.com'.format(int(time.time())), 'abcABC123', driver),
    #     (u'电话为空', 'wuzhiwen', '', '{:d}@qq.com'.format(int(time.time())), 'abcABC123', driver),
    #     (u'邮件为空', 'wuzhiwen', '{:d}1'.format(int(time.time())), '', 'abcABC123', driver),
    #     (u'密码为空', 'wuzhiwen', '{:d}1'.format(int(time.time())), '{:d}@qq.com'.format(int(time.time())), '', driver),
    #     (u'邮箱格式不正确', 'wuzhiwen', '{:d}1'.format(int(time.time())), '23423423', 'abcABC123', driver),
    #     (u'电话格式不正确', 'wuzhiwen', '453453gdf', '23423423', 'abcABC123', driver),
    #     (u'密码格式不正确', 'wuzhiwen', '{:d}1'.format(int(time.time())), '{:d}@qq.com'.format(int(time.time())), 'abc123123',
    #      driver),
    #     (u'电话已被使用', 'wuzhiwen', '18301929561', '{:d}@qq.com'.format(int(time.time())), 'ABCa3bc123123', driver),
    #     (u'邮箱已被使用', 'wuzhiwen', '{:d}1'.format(int(time.time())), '915522927@qq.com', 'ABCa3bc123123', driver),
    #     (u'信息正确', 'wuzhiwen', '{:d}1'.format(int(time.time())), '{:d}@qq.com'.format(int(time.time())), 'ABCabc123123',
    #      driver),
    #
    # ]

    # #测试注册页
    # for task in register_task_list:
    #     driver.get(_start_url)
    #     resultMsg(index_n1('入口页测试',_login_url,driver))
    #     driver.save_screenshot('captcha.png')
    #     resultMsg(register_n2(*task))


    # 测试信息页
    # driver.get(_start_url)
    # resultMsg(index_n1('入口页测试', _login_url, driver))
    # driver.save_screenshot('captcha.png')
    # resultMsg(register_n2(*register_task_list[3]))
    # time.sleep(2)
    # for info in info_list:
    #     resultMsg(info_n3(*info))
    #
    # driver.quit()
