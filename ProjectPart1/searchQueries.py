def textBasedSearch(source, fields, qtxt, client, index_name):
        query = qtxt
        query_bm25 = {
            'size': 3,
            '_source': source,
            'query': {
                'multi_match': {
                'query': query,
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
