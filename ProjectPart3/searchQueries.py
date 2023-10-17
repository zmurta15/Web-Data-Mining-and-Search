def textBasedSearch(source, fields, qtxt, client, index_name):
        query_bm25 = {
            'size': 3,
            '_source': source,
            'query': {
                'multi_match': {
                'query': qtxt,
                'fields': fields,
                #'analyzer':'my_analyzer'
                }
            }
        }
        response = client.search(
        body = query_bm25,
        index = index_name
        )
        return response

def booleanTextSearch(source, fields, qtxt, term, client, index_name):
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
                  "should": {
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

def filterBooleanSearch(source, fields, qtxt, filter_, client, index_name):
        query_bm25 = {
          'size': 5,
          '_source': source,
          'query': {
              'bool':{
                  "should": {
                    'multi_match': {
                      'query': qtxt,
                      'fields': fields
                    }
                  },
                  "filter": {
                     "term": {
                       "ingredients": filter_,
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
    
def embeddingsSearch(source, embedding, queryEmb, client, index_name):
    # Compute the query embedding
    query_emb = queryEmb
    query_denc = {
      'size': 5,
      '_source': source,
       "query": {
            "knn": {
              embedding: {
                "vector": query_emb[0].numpy(),
                "k": 2
              }
            }
          }
    }
    response = client.search(
        body = query_denc,
        index = index_name
    )
    return response
