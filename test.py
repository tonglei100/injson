from injson import pick
import json

sub = {"code": 200,
       "error": "hello, world",
       "name": "<name>",
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
print(json.dumps(result, ensure_ascii=False, indent=4))
