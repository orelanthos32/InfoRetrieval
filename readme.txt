1.Set up elasticsearch on docker: docker run -d -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.6.2
2.launch index_dataV2py
3. wait for indexing to finish
4. launch api_ES.py