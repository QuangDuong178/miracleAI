# AT.Miracle-BE

AT.Miracle-BE

### Setup env
```sh
$ cp .env.example .env
# pass value environment variables
```

### Basic Commands
- Run docker-compose
```bash
$ docker-compose -f local.yml up -d
```
- Interact container os
```bash
$ docker exec -it vietis_chatbot_api sh

# If new model was created run makemigrations
$ python manage.py makemigrations

```
- If environment crash...
```bash
$ docker-compose -f local.yml down -v && docker-compose -f local.yml up --build
```
