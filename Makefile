Build_and_start_Container_Salud_tech: 
	docker build . -f src/salud_tech/Dockerfile -t salud_tech/flask && docker compose --profile salud_tech up --build
Delete_Data_Folder:
	sudo rm -r data
Create_Data_Folder:
	mkdir -p data/bookkeeper && mkdir -p data/zookeeper && sudo chmod -R 777 ./data

clean_folder: 
	if [ -d "./data" ]; then echo "La carpeta data existe, eliminándola..."; rm -rf data; else echo "La carpeta data no existe, continuando..."; fi

start_pulsar_containers:
	docker compose --profile pulsar up --build -d

start_db_container:
	docker compose --profile db up --build -d

start_salud_tech_container:
	docker compose --profile salud_tech up --build -d

kill_all:
	docker compose --profile pulsar --profile db --profile salud_tech down -v

recreate_salud_tech_container:
	docker compose --profile salud_tech down -v && docker compose --profile salud_tech up --build --force-recreate 

recreate_anonimacion_container:
	docker compose --profile anonimacion down -v && docker compose --profile anonimacion up --build --force-recreate 