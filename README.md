
# CDK on Pythonのサンプル

以下のページのTypeScriptをPythonに書き換え
https://dev.classmethod.jp/articles/cdk-practice-1-introduction/

## 構成の概要
### VPC
### SubnetはAZx2上に3つずつ配置
- Public ALB配置
- Appp EC2配置
- DB RDS配置
### RDSユーザ/パスワードはSecret Managerに配置
### Security Gourp,ネットワークACL,IAM Role等は適宜設定
   
