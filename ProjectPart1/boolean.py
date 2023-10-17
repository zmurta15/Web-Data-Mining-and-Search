
def vargues(source, fields, qtxt, client, index_name):
        qtxt = qtxt
        query_bm25 = {
          'size': 5,
          '_source': source,
          'query': {
              'bool':{
                  "must":{
                    "term": {
                        "ingredients" : term
                    }
                  },
                  "should": 
                {
                    'multi_match': {
                      'query': qtxt,
                      'fields': fields
                    }
                }
              }
          }
        }
        response = client.search(
            body = query_bm25,
            index = index_name
        )
        return response