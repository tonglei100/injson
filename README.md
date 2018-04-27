# injson

测试一个 json 是否在另一个 json 中

## 安装

> pip install injson

## 使用

```python
import json
from injson import in_json


json1 = {"code":200,
        "error": "hello,word",
        "result": [
            {"sweetest":"OK",
             "status": "yes"
            },
            {"ages":[1,2,4],
             "status": "yes"
            },
            {"sonar":"OK",
             "status": "yes"
            }
        ],
       }

json2 = {"code":200,
        "error": "you are bad",
        "result": [
            {"sweetest":"Fail",
             "status": "NO"
            },
            {"sweetest":"OK",
             "status": "NO"
            },
            {"ages":[1,2,3],
             "status": "yes"
            },
            {"sonar":"OK",
             "status": "yes"
            }
        ],
       }

result = in_json(json1, json2)
print(json.dumps(result, ensure_ascii=False, indent=4))
```

## 打印结果

```json
{
    "code": 3,
    "result": {
        "/error": {
            "code": 1,
            "sv": "hello,word",
            "ppath": "/error",
            "pv": "you are bad"
        },
        "/result[0].status": {
            "code": 1,
            "sv": "yes",
            "ppath": "/result[1].status",
            "pv": "NO"
        },
        "/result[1].ages": {
            "code": 1,
            "sv": [1, 2, 4],
            "ppath": "/result[2].ages",
            "pv": [ 1, 2, 3]
        }
    }
}
```
