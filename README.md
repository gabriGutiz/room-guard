# RoomGuard

## Broker
As pastas necessárias para deploy e configuração do broker estão na pasta ./broker

## Servidor
O código do servidor, responsável por receber mensagens das salas e processar, está disponível na pasta ./server

O arquivo executado é ./server/server.py

A imagem do docker é construída com base no arquivo ./server/Dockerfile

## Dispositivo IoT
O código executado pelo dispositivo IoT está disponível na pasta ./iot/src/

No dispositivo, os dois scripts devem ser executados em paralelo: ./iot/src/send_state.py e ./iot/src/receive_action.py

## Frontend
O código do frontend está na pasta ./front

O frontend é composto pelo website e pelo backend.

O código da api para o frontend está na pasta ./front/back

O código do front está na pasta ./front/front

## Deploy
O deploy destes serviços é feito com o arquivo ./docker-compose.yml

## Utilidades
Na pasta ./utils existem diversos scripts com funcionalidades para testes locais.

