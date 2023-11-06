start backend:
	$ uvicorn main:app --reload

start frontend:
	$ npm install
	$ npm run build
	
start docker:
	$ docker run -d -p 8000:8000 deep_learning_project_docker