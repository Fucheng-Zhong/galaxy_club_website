# 构成

## 使用gunicorn方式部署，端口8002
## MySQL数据库,名称mydb, 在setting设置
## APP: users, galaxy,

# users APP
## users APP 为用户注册和鉴权系统，有一个table用于存放用户数据

## 注册
### describe：POST方法在request body传输注册信息，此时会发送邮件到用户邮箱，成功返回success. 
### url: /register  
### variable: body:['username','password','email','confirmedPassword']
### error: 用户/邮箱已注册，密码不一致，字符空/过长

## 验证码
### describe：POST方法在request body传输注册信息，验证码有5次机会(暂定)，没错误一次用户权限-1，成功则用户permissions=1, permissions<-5 时账户会被冻结. 成功返回success 
### url: /smsCode  
### variable: body:['username','password','email','smsCode']
### error: 用户/邮箱不存在注册，密码不一致，字符空/过长，验证码不正确, 验证码失效，重新发送验证码.

## 登录
### describe: POST方法在request body传输登录信息，成功则返回有期限的token
### url: /auth
### variable: body: ['username','password']
### error: 用户/密码错误

## 鉴权
### describe: POST方法在request body传输用户名和token，后端进行校验并返回请求
### url: /authenticate
### variable: body: ['username','token']
### error: 用户/token错误, token过期



# galaxy APP

## galaxy APP用于分配待分类星系给用户，并存储分类结果。有2个table，一个用于存储星系列表，一个用于存储分类结果。

## 请求图像
### describe: POST方法来请求待分类图像，鉴权后会返回特定或随机的，未被该用户分类过的，被分类次数少于5（暂时）的图像。
### url: /requry_image
### variable: body: ['username','token']
### error: 用户/token错误, token过期，鉴权错误，无此用户/galaxy，无未被分类galaxy

## 返回结果
### describe: POST方法来提交分类后的结果。先进行鉴权，permissions>=1的用户才能提交结果，随后结果先被检查是否在用户/galaxy列表中，检查是已经被该用户分类过，检查分类次数是否大于5，通过后以 用户名_星系名 为id保存于分类结果的table。
### url: /classify
### variable: body: ['username','galaxy_name','token','type1']
### error: 用户/星系不存在，鉴权错误，重复分类，分类次数大于5（暂定），权限不足