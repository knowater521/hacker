import requests

target_url = "http://wap.xiongti.cn/login.php"
data_dict = {"username":"holmes","password":"19980928","submit":"submit"}
response = requests.post(target_url, data=data_dict)
print(response.content)
