from injson import check
import json

sub = {"code": 200,
       "error": "hello, world",
       "name": "<name>",
       "phone": "<phone>",
       "level": 1,
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
       "student":{"name": "leo",
            "age": "<age>"
           }
       }

parent = {"code": 200,
          "error": "you are bad",
          "name": "Leo",
          "level": "ONE",
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
          "student":{"name": "leo",
               "age": 19
              }
          }

result = check(sub, parent)
print(json.dumps(result, ensure_ascii=False, indent=4))
