# -*- coding: utf-8 -*-
TEMPLATES = {}
TEMPLATES['config.ini'] = """
[general]
; 输出格式，支持 epub 和 mobi，默认为 mobi
; TODO:epub计划中还不支持
output_format = mobi

; 输出 kindle格式的类型： book 或 periodical
kindle_format = book

; 是否发送邮件，如果不发送可以直接拷贝 /data/ 中相应文件到kindle： 1 发送， 0 不发送
mail_enable = 0

; 用户时区, 更多可用查看pytz.all_timezones
timezone = Asia/Shanghai

[reader]
; google reader 用户名
username = yourname@gmail.com

; google reader 密码，可以不写提示时再输入
password =

; 需要抓取的分类，此项优先于 skip_categories， 仅当此项为空时 skip_categories 设置有效
select_categories =

; 跳过分类，用英文逗号隔开, 例如：label1,label2
skip_categories =

; 是否要标记为已读： 1 标记， 0 不标记
mark_read = 0

; 每个feed中最多抓取条目
max_items_number = 20

; 排除已读 1 是 0 否， 如果设置为是则为只加载未读条目，反之亦然
exclude_read = 1

; 每篇文章最多下载图片数数目， -1 为不限， 图片太多可能需要时间很长并且造成mobi过大无法发送
; 如果下载图片需要kindlegen支持，请确保kindlereader.exe所在目录中包含kindlegen.exe
max_image_per_article = 5

; 生成mobi中文章的顺序，0:默认新帖在前，1:旧贴在前
time_order = 0

; 邮件发送设置
[mail]

; 发件人，请使用亚马逊注册邮箱，或你的"Your Kindle's approved email list"中的其他邮箱
from = youremail

; 亚马逊提供的投递邮箱地址，注意 @free.kindle.com只能投递到wifi， @kindle.com可以投递到3G但要收费，也可以填写一个其他邮箱地址，由该邮箱转发到你的kindle邮箱地址
to = "name"@free.kindle.com

; smtp服务器地址可以使用gmail的smtp服务器
host = smtp.gmail.com

; smtp服务器端口, 不加密一般为 25, 加密一般为 465
port = 465

; smtp服务器是否需要 ssl： 1 需要， 0 不需要， 请根据你使用的smtp实际情况选择
ssl = 1

; smtp服务器需要认证时请填写下面两项，任何一项不填写则认为你的smtp服务器不需要认证
username =
password =
"""
