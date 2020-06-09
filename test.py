from injson import check
import json

sub = {"code": 200,
       "error": "hello, world",
       "name": "<name>",
       "phone": "<phone>",
       "level": [1],
       "address": "china",
       "result[0]": "<result01>",
        "result[0]['status']": "<status01>",
        "result[2]['status']": "no",   
       "result": [
           {"sweetest": "OK",
            "status": "<status>"
            },
           {"ages": [1, 2, 4],
            "status": "yes"
            },
           {"sonar": "OK",
            "status": "yes",
            "fruit": ["apple"]
            }
       ],
       "student":{"name": "Andy",
            "age": "<age>"
           }
       }

parent = {"code": 200,
          "error": "you are bad",
          "name": "Leo",
          "level": [2,1,"ONE"],
          "address": 86,
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
               "status": "yes",
               "fruit": ["branana",'apple']
               }
          ],
          "student":{"name": "Lily",
               "age": 19
              }
          }

result = check(sub, parent)
print(json.dumps(result, ensure_ascii=False, indent=4))
