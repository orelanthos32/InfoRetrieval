# Instructions to run Website
1. Change drectory to this folder: stocksite folder
2. Install the required libraries: pip install -r requirements.txt 
3. Ensure that elasticsearch and nboost is running in docker:
*Set up elasticsearch on docker: docker run --name db1 -d -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.6.2
* Set up nboost on docker: docker run -d -p8000:8000 --link db1 koursaros/nboost:latest-pt --uhost localhost --uport 9200 --search_route "/<index>/_search" --query_path url.query.q --topk_path url.query.size --default_topk 10 --choices_path body.hits.hits --cvalues_path _source.passage
4. Index the date: py index_data.py
5. Run the server: py manage.py runserver
6. Wait for the server to be up
7. Open the web browser and search: http://127.0.0.1:8000/app/