# easytestapi-flask

专供easytestapi接口自动化使用

# 安装启动
```shell
pip install -r requirement.txt

python manage.py
```

# 提供测试接口
```shell
# 查询tester列表
curl --location --request GET 'http://localhost:5000/testers'

# 新增tester
curl --location --request POST 'http://localhost:5000/testers' \
--header 'Content-Type: application/json' \
--data-raw '{
    "test_enum": "B",
    "test_str": "asdasdasdasd",
    "test_int": 123461231,
    "test_float": 3852504650.74,
    "test_phone": "13922113895",
    "test_dt": "2022-08-02 19:56:50"
}'

# 查询tester详情
curl --location --request GET 'http://localhost:5000/testers/1'

# 修改tester
curl --location --request PUT 'http://localhost:5000/tp/testers/9' \
--header 'Content-Type: application/json' \
--data-raw '{
    "test_str": "asdasdasdadasd",
    "test_phone": "13922771535"
}'

# 软删除tester
curl --location --request DELETE 'http://localhost:5000/tp/testers/9'

# 查询tester操作记录
curl --location --request GET 'http://localhost:5000/tp/tester_op_record'
```