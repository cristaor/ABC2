# ABC

## Como correr el proyecto?
Para correr el projecto es necesario tener Docker instalado, se debe ejecutar el siguiente comando:´

 `` 
 docker compose up -d
 `` 
 
 Se deberan observar 3 microservicios desplegados y 2 servicios
 1. Redis
 2. Postgres
 3. Notification
 4. Authorizer
 5. API Gateway
 
 Despues de ver los servicios desplegados
 
 Se deben enviar las peticiones a los recursos

## Enviar petición login Usuario 1
```
curl --location --request POST 'localhost:5000/login' \
--header 'Content-Type: application/json' \
--data-raw '{
    "user": "1",
    "password":"1234"
}'
```

## Enviar petición botón de panico
```
curl --location --request POST 'localhost:5000/notificacion' \
--header 'Authorization: Bearer {{TOKEN_JWT}}' \
--header 'Content-Type: application/json' \
--data-raw '{"fecha_evento": "2200-01-01",
                    "uuid":"123123", 
                    "cliente": "1", 
                    "direccion": "calle 123", 
                    "sensor_type":"PANICO", 
                    "tipo_evento": "TYPE"
                    }'
```


## Enviar petición health check
```
curl --location --request GET 'localhost:5000/health' \
--header 'Authorization: Bearer {{TOKEN_JWT}}'
```
 
