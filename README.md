
## Request Token
```sh
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin"}' \
  http://localhost:8000/token/
```

## Request do file upload

```sh
curl -X POST \
  -H "Authorization: Token dbdb7e130963899f468f8255abf874484cf905b6" \
  -H "Content-Type: multipart/form-data" \
  -F "file_content=test.txt" \
  -F "name=test.txt" \
  http://localhost:8000/files/
```

## Request file download

```sh
curl -X GET -H "Authorization: Token dbdb7e130963899f468f8255abf874484cf905b6" http://localhost:8000/files/1/download/
```