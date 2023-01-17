# tic-tac-toe
## terraformを使って既存の環境を破壊します。
cd terraform
terraform destroy
## terraformをapplyします。
terraform apply
## 戻ります。
cd ..
## 認証トークンを取得し、レジストリに対して Docker クライアントを認証します。
aws ecr get-login-password --region ap-northeast-1 | docker login --username AWS --password-stdin 867926628156.dkr.ecr.ap-northeast-1.amazonaws.com
## 以下のコマンドを使用して、Docker イメージを構築します。一から Docker ファイルを構築する方法については、「こちらをクリック 」の手順を参照してください。既にイメージが構築されている場合は、このステップをスキップします。
docker build -t slack_bot .
## 構築が完了したら、このリポジトリにイメージをプッシュできるように、イメージにタグを付けます。
docker tag slack_bot:latest 867926628156.dkr.ecr.ap-northeast-1.amazonaws.com/slack_bot:latest
## 以下のコマンドを実行して、新しく作成した AWS リポジトリにこのイメージをプッシュします:
docker push 867926628156.dkr.ecr.ap-northeast-1.amazonaws.com/slack_bot:latest
## terraformをapplyします。
terraform apply
## urlを変更します
./frontend/MAIN.JSのapiUrlをhttps://dxscjo6mrh.execute-api.ap-northeast-1.amazonaws.com/testに