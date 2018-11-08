![inJSON](https://github.com/tonglei100/injson/blob/master/logo.png?raw=true)

# inJSON

测试一个 JSON 是否在另一个 JSON 中，并返回不一致的键值对；同时可以以变量的形式提取对应路径上的字段值。

## 安装

```shell
pip install injson
```

## 使用

```python
from injson import check


sub = {"code": 200,
       "error": "hello, world",
       "name": "<name>",                # 以 <name> 扩起来的字符串视为变量 name \
       "phone": "<phone>",              # 该变量将从 parent 中对应位置提取值
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

result = check(sub, parent)
print(result)
```

## 打印结果

> 注: 下面的 json 格式是已美化后的结果

```python
{
    "code": 2,                          # 键值对不一致的个数，当值为 0 时，表示全部一致

    "result": {                         # 比较出不一致的键值对，并放在此 dict
        "/error": {                     # 键的路径，以 / 开头
            "code": 1,                  # 错误类型：1-值不一致，2-数据类型不一致，\
                                        # 3-键不存在, 4-预期键不存在，实际键存在
            "sv": "hello,word",         # sv 全拼为 sub_value, sub json 中对应键的值
            "pp": "/error",             # pp 全拼为 parent_path, parent json 中对应键的路径
            "pv": "you are bad"         # pv 全拼为 parent_value, parent json 中对应键的值
        },

        "/result[1].ages": {            # 如果是 list，则以 [i] 表示路径
            "code": 1,
            "sv": [1, 2, 4],
            "pp": "/result[2].ages",    # 对于 list，其下标不一定一致。
            "pv": [ 1, 2, 3]
        }
    },

    "var": {                            # 获取对应键位置上的值，并放在此 dict
        "name": "Leo",
        "_phone": None,                 # 如果某个键在 parent 中不存在，则键带上下划线（_）前缀，其值为 None
        "status": "NO"
    }
}
```

## 列表的比较逻辑

### 列表的元素假设
我们假设列表的所有元素都是同一个类型，比如都是字符串、数字、列表或都是字典。
程序处理时以预期数据的第一个元素做类型判断，如果类型不同，可能会出错。

### 列表的元素为字典
会继续对字典进行递归比较。

### 列表的元素是其他类型
仅判断预期的列表元素是否在实际结果的列表中。

> 注：如果列表的元素还是列表，子列表看做普通类型处理，不会逐层比较。


## 特殊匹配

|开头字符|匹配说明|示例    |示例说明    |
| ------ | -------- | -------- | ------------ |
| \*     | 包含     | *test    | 包含test     |
| ^      | 开头     | ^hello   | 以hello开头  |
| $      | 结尾     | $world   | 以world结尾  |
| \-     | 无此字段 | -        | 必须无此字段 |
| \+     | 有此字段 | +        | 必须有此字段 |
| \      | 转义     | \\*      | 匹配*        |
| #      | 不等于   | #test    | 不为test     |
