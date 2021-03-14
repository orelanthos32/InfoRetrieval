1.Set up elasticsearch on docker: docker run --name db1 -d -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.6.2
2. Set up nboost on docker: docker run -d -p8000:8000 --link db1 koursaros/nboost:latest-pt --uhost localhost --uport 9200 --search_route "/<index>/_search" --query_path url.query.q --topk_path url.query.size --default_topk 10 --choices_path body.hits.hits --cvalues_path _source.passage
3.launch index_dataV2py
4. wait for indexing to finish
5. launch api_nboost.py