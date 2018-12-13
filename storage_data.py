import os
import time
import schedule
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL
from email.utils import formataddr
from pymysql import connect


class SaveData(object):

    # 初始化信息
    def __init__(self):
        self.host = os.getenv('HOST') # 系统环境变量自己添加
        self.port = os.getenv('PORT')
        self.user = os.getenv('USER')
        self.passwd = os.getenv('PASSWD')
        self.db = os.getenv('DB')
        self.charset = os.getenv('CHARSET')
        self.str1 = ''
        self.num = 0
        self.errnum = 0
        pass

    def save_data(self):
        # 创建连接
        conn = connect( host=self.host, user=self.user, password=self.passwd,
                        database=self.db, port=self.port,charset='utf8')
        # 创建一个游标对象
        cs = conn.cursor()
        sql = '查询语句查询放的位置,只能放一句查询语句,多的话另处理'
        cs.execute(sql)
        datas = cs.fetchall()
        if len(datas) == 0:
            self.str1 = '暂时无需要存储的数据'
            cs.close()
            conn.close()
            return self.str1
        else:
            for data in datas:
                print(data)
                # sql_stor = "insert into storage(name, imgurl, price) values('%s','%s','%s')"%(data[1],data[2],data[3])
                sql_stor = '根据查询结果插入数据,前提是把数据库的表手动建好处于同一数据库下' # 需要代码建表的再处理
                try:
                    cs.execute(sql_stor)
                    self.num += 1
                except:
                    self.errnum += 1
            conn.commit()
            cs.close()
            conn.close()
        return '<h2>' + str(self.num)+'条数据插入成功' + '<h2><br/><br/><h2>' + str(self.errnum) + '条数据插入失败<h2>'

    def send_email(self, content):
        host_server = 'smtp.163.com'
        sender = 'xiaskyf@163.com'
        pwd = 'xia763541'
        send_mail = 'xiaskyf@163.com'
        receivers = 'effy.xu@letote.cn'  # 收件人邮箱
        # 邮件的正文内容
        mail_time = time.strftime('%Y-%m-%d %X', time.localtime())
        mail_content = content +'<br/><br/>'+ mail_time

        # 邮件标题
        mail_title = '公司数据库定时操作结果'
        smtp = SMTP_SSL(host_server)
        smtp.ehlo(host_server)
        smtp.login(sender, pwd)

        msg = MIMEText(mail_content, 'html', 'utf-8')
        msg['Subject'] = Header(mail_title, 'utf-8')
        msg['From'] = formataddr(['公司', sender])
        msg['To'] = formataddr(['徐燕', receivers])
        smtp.sendmail(send_mail, receivers, msg.as_string())
        smtp.quit()

    def run(self):
        send_content = self.save_data()
        self.send_email(send_content)

def main():

    x_storage = SaveData()
    x_storage.run()

schedule.every().monday.at('9:00').do(main)  # 每周一执行函数

if __name__ == '__main__':
    while True:
        schedule.run_pending()