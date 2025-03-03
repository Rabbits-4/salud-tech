Build_Container_Salud_tech: 
	docker build . -f salud_tech.Dockerfile -t salud_tech/flask 
Delete_Data_Folder:
	sudo rm -r data
Create_Data_Folder:
	mkdir -p data/bookkeeper && mkdir -p data/zookeeper && sudo chmod -R 777 ./data

clean_folder: 
	if [ -d "./data" ]; then echo "La carpeta data existe, eliminándola..."; rm -rf data; else echo "La carpeta data no existe, continuando..."; fi