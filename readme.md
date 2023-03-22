# 构成


# users APP
## users APP 为用户注册和鉴权系统，有一个table用于存放用户数据
### describe：POST方法在request header传输注册信息，成功返回success 
### url: /register  
### variable: header:['username','password','email','confirmedPassword']
### error: 用户/邮箱已注册，密码不一致，字符空/过长

## 登录
### describe: POST方法在request header传输登录信息，成功则返回有期限的token
### url: /auth
### variable: header: ['username','password']
### error: 用户/密码错误

## 鉴权
### describe: POST方法在request header传输用户名和token，后端进行校验并返回请求
### url: /authenticate
### variable: header: ['username','token']
### error: 用户/token错误, token过期


# galaxy APP

## galaxy APP用于分配待分类星系给用户，并存储分类结果。有2个table，一个用于存储星系列表，一个用于存储分类结果。

## 请求图像
### describe: POST方法来请求待分类图像，鉴权后会返回特定或随机的，未被该用户分类过的，被分类次数少于5（暂时）的图像。
### url: /requry_image
### variable: header: ['username','token']
### error: 用户/token错误, token过期，鉴权错误，无此用户/galaxy，无未被分类galaxy

## 返回结果
### describe: POST方法来提交分类后的结果。先进行鉴权，随后结果先被检查是否在用户/galaxy列表中，检查是已经被该用户分类过，检查分类次数是否大于5，通过后以 用户名_星系名 为id保存于分类结果的table。
### url: /classify
### variable: header: ['username','galaxy_name','token','type1']