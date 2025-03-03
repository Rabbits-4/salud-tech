Build_and_start_Container_Salud_tech: 
	docker build . -f salud_tech.Dockerfile -t salud_tech/flask && docker compose --profile salud_tech up --build
Delete_Data_Folder:
	sudo rm -r data
Create_Data_Folder:
	mkdir -p data/bookkeeper && mkdir -p data/zookeeper && sudo chmod -R 777 ./data

clean_folder: 
	if [ -d "./data" ]; then echo "La carpeta data existe, eliminándola..."; rm -rf data; else echo "La carpeta data no existe, continuando..."; fi

start_pulsar_containers:
	docker compose --profile pulsar up --build

start_db_container:
	docker compose --profile db up --build -d

start_salud_tech_container:
	docker compose --profile salud_tech up --build

kill_all:
	docker compose --profile pulsar --profile db --profile salud_tech down -v