**- distinct untuk mengetahui semua macam value dan jumlah nya**

`GET index/_search
{
    "size": 0,
    "aggs": {
        "results": {
            "terms": {
                "size": 4000,
                "field": "id_laporan.keyword"
            }
        }
    }
}`

**- distinc untuk mengetahui semua macam value dan jumlh nya serta menampilkan field lain didalamnya**

`GET index/_search
{
    "size": 0,
    "aggs": {
        "results": {
            "terms": {
                "size": 4000,
                "field": "id_laporan.keyword"
            },
            "aggs": {
                "sources": {
                    "top_hits": {
                        "size": 100,
                        "sort": [
                            {"crawling_time": {"order": "asc"}}
                        ],
                        "_source": {
                            "includes": ["id_laporan", "crawling_time"]
                        }
                    }
                }
            }
        }
    }
}`

**- membuat index dan mapping didalamnya**

`PUT index-name
{
  "mappings": {
  "properties": {
    "dimension_code": {
      "properties": {
        "geometry": {
          "type": "geo_shape"
        },
        "location": {
          "type": "geo_point"
        }
      }
    }
  }
}
}`


**- menampilkan hanya bebrapa field saja**

`GET index/_search
{
  "_source": ["province_name", "logo_image", "results.sub_type", "results.analysis_result"],
  "query": {
    "match_all": {}
  }
}`


**- menggabungkan beberapa query (setara dengan AND di sql)**

`GET index/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "exists": {
            "field": "title"
          }
        },
        {
          "exists": {
            "field": "indo_global_impact_list.keyword"
          }
        }
      ]
    }
  },
  "sort": [
    {
      "date": {
        "order": "desc"
      }
    }
  ]
}`

**- aggregations 2 field**

`GET index/_search
{
  "size": 0,
  "aggs": {
    "regions": {
      "terms": {
        "field": "region.keyword",
        "size": 1000
      },
      "aggs": {
        "countries": {
          "terms": {
            "field": "countries.keyword",
            "size": 1000
          }
        }
      }
    }
  }
}`