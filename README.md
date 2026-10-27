# Simple Python API application with a frontend GUI serviced by nginx

Verificiation

`docker compose config -q` --> check compose file without running anything

`docker compose up -d --build` --> 
  - build docker compose up and the image is rebuilt
  - creates the network and volume
  -`--build` starts containers based on depends_on or health_checks otherwise starts all at the same time and connects to network
  - `-d` runs containers at the background. If not specified, at the foregound.
  
## Reaching the backend

To interact with the backend services, you need to specify the /api path on your URL request. Example below shows how to query for the backend health-check:

`http://localhost:8080/api/health`
