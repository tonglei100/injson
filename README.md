# injson

测试一个 json 是否在另一个 json 中，并返回不一致的值；同时可以返回对应路径上的字段值。

## 安装

> pip install injson

## 使用

```python
from injson import pick


sub = {"code": 200,
       "error": "hello,word",
       "name": "<name>", # 以 <> 扩起来的字符串，视为变量，从parent 中对应位置提取值
       "phone": "<phone>",
       "result": [
           {"sweetest": "OK",
            "status": "<status>"
            },
           {"ages": [1, 2, 4],
            "status": "yes"
            },
           {"sonar": "OK",
            "status": "yes"
            }
       ],
       }

parent = {"code": 200,
          "error": "you are bad",
          "name": "Leo",
          "result": [
              {"sweetest": "Fail",
               "status": "NO"
               },
              {"sweetest": "OK",
                  "status": "NO"
               },
              {"ages": [1, 2, 3],
                  "status": "yes"
               },
              {"sonar": "OK",
                  "status": "yes"
               }
          ],
          }

result = pick(sub, parent)
print(result)
```

## 打印结果

> 注: 下面的 json 格式是已美化后的结果

```python
{
    "code": 2,                      # 键值对不一致的个数
    # 比较出不一致的键值对，并放在如下列表
    "result": {
        "/error": {                 # 键的路径，以 / 开头
            "code": 1,              # 错误类型：1-值不一致，2-数据类型不一致，3-键不存在
            "sv": "hello,word",     # sub json中改键的值
            "ppath": "/error",      # parent json 中对应键的路径
            "pv": "you are bad"     # parent json 中对应键的值
        },
        "/result[1].ages": {        # 如果是 list，则以 [x] 表示路径
            "code": 1,
            "sv": [1, 2, 4],
            "ppath": "/result[2].ages", # 对于 list，去下标不一定一致。
            "pv": [ 1, 2, 3]
        }
    },
    # 获取对应键位置上的值，并放在如下列表中
    # 注意，如果某个键在 parent 中不存在，则其值为 None，但不会报错
    "var": {
        "name": "Leo",
        "phone": None,
        "status": "NO"
    }
}
```
