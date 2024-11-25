import os
import json
from dotenv import load_dotenv
from example import load_json_example
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ecc.v20181213 import ecc_client, models

load_dotenv()
SecretId = os.getenv("SecretId")
SecretKey = os.getenv("SecretKey")

example = load_json_example("example01.json")

try:
    cred = credential.Credential("SecretId", "SecretKey")
    
    httpProfile = HttpProfile()
    httpProfile.endpoint = "ecc.tencentcloudapi.com"

    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    
    client = ecc_client.EccClient(cred, "", clientProfile)

    # 实例化一个请求对象,每个接口都会对应一个request对象
    req = models.ECCRequest()
    params = {
        "Content": example["Content"],
        "Title": example["Title"],
        "Grade": example["Grade"],
        "ModelContent": example["ModelContent"]
    }
    req.from_json_string(json.dumps(params))

    resp = client.ECC(req)
    print(resp.to_json_string())

except TencentCloudSDKException as err:
    print(err)