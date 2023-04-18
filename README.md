# 📝 API Documentation

**Ebebul** is a cutting-edge project that revolutionizes healthcare communication by offering patients the ability to connect with their doctors at their convenience. With Ebebul, patients can chat with their doctors through the platform, make appointments, and locate nearby hospitals all in one place.

The platform offers a user-friendly interface that simplifies the process of scheduling appointments. Patients can search for doctors by specialty, location, and availability, making it easy to find a doctor that meets their specific needs. The platform also provides access to doctor profiles, where patients can view their credentials, specialties, and areas of expertise.

**Ebebul**'s chat feature allows patients to communicate directly with their doctors, eliminating the need for phone calls or emails. Patients can ask questions, receive advice, and discuss their health concerns in a secure, private environment. This feature allows for better communication and understanding between patients and doctors, leading to improved health outcomes.

## Getting Started

Before getting started, we strongly recommend you to install **Postman** app on your machine. Because, some type of requests are impossible to make from the browser. We also use, bash commands (mostly curl) for sending request to API

You can download Postman App for free by the link below:

[Download Postman | Get Started for Free](https://www.postman.com/downloads/)

## User Endpoints

`/auth/users/` → create new user | POST

`/auth/users/me/` → get current user | GET

`/auth/users/me/` → updates record | PATCH

`/auth/users/me/` → removes record from db | DELETE

`/auth/token/login/` → created new access and refresh token | POST

`/auth/token/refresh/` → get new access token by using refresh token | POST

## Hospital Endpoints

`/hospitals/` → get list of hospitals | GET

`/hospitals/<pk:int>/`→ get details of hospital by ID | GET

## Video Endpoints

`/videos/` → get list of videos | GET

`/videos/<pk:int>/`→ get details of video by ID | GET

## Notification Endpoints

`/notifications/` → get list of notifications | GET

`/notifications/<pk:int>/`→ get details of notification by ID | GET

## Content Endpoints

`/contents/` → get list of notifications | GET

`/contents/<pk:int>/`→ get details of content by ID | GET

`/contents/<pk:int>/file/`→ get content of file by ID | GET

## Visit Endpoints

`/visits/` → get list of notifications | GET

`/visits/<pk:int>/`→ get details of visit by ID | GET

## Sign Up

To access any data, first you (client) must create a user account. Without authentication, you cannot access to any data in database.

Endpoint to create new user record:

`/auth/users/`

Client must sent some required data which listed below

```json
// Request Body
{
    "password": "string", // max -> 128 chars
    "email": "string/email", // unique
    "name": "string", // max -> 100 chars
    "gender": "M",// only "F" or "M"
    "birth_date": "2000-12-09", // format YYYY-MM-DD
    "address": "Istanbul", //string
    "category": 1, // cat ID -> 1 for User, 2 for Nurse
    "longitude": 50.2, // double: 123.456789 | aaa.bbbbbb is valid data
    "latitude": 25.1, // double: 123.456789 | aaa.bbbbbb is valid data
    "marial_status": "S" // "S" -> single, "M" -> maried
}
```

When you send valid data, server responses the record which was created

```json
// Response
// Status: 201 Created
{
    "id": 6,
    "email": "hola2@gmail.com",
    "name": "Abdulaziz Abduvakhobov",
    "identity_number": null,
    "gender": "M",
    "birth_date": "2000-01-01",
    "weight": null,
    "height": null,
    "address": "Tashkent",
    "longitude": "50.200000",
    "latitude": "25.100000",
    "marial_status": "S",
    "last_login": "2023-03-05T22:10:48.240671+03:00",
    "category": 1
}
```

If you send invalid data or miss some fields, server will response which field is invalid

```json
// Response
// Status: 400 Bad Request
{
    "password": [
        "This field is required."
    ],
    "email": [
        "This field is required."
    ],
    "name": [
        "This field is required."
    ],
    "gender": [
        "This field is required."
    ],
    "birth_date": [
        "This field is required."
    ],
    "address": [
        "This field is required."
    ],
    "longitude": [
        "This field is required."
    ],
    "latitude": [
        "This field is required."
    ],
    "marial_status": [
        "This field is required."
    ],
    "category": [
        "This field is required."
    ]
}
```

Another example of invalid request

```json
// Request Body
{
    "password": "1234",
    "email": "hello@test.com",
    "first_name": "Abdulaziz",
    "last_name": "abduvakhobov",
    "gender": "M",
    "birth_date": "2000-12-09",
    "address": "Istanbul"
}
```

In this case, server checks validity of all fields, by default password value must be at least 8 characters

```json
// Response
// Status: 400 Bad Request
{
    "longitude": [
        "This field is required."
    ],
    "latitude": [
        "This field is required."
    ],
    "marial_status": [
        "This field is required."
    ],
    "category": [
        "This field is required."
    ]
}
```

## Authentication

After successfully creating of user record, client have to get access token in order to get access to data

**Token Endpoints:**

`/auth/token/login/` → creates new access and refresh **JWT (JSON Web Token)** token

`/auth/token/refresh/` → creates new access token by using refresh token

You must send **POST** request to get token. In the body of request client must enter **email** and **password** value

Example in Bash:

```bash
curl -X POST https://..../auth/token/login/
   -H 'Content-Type: application/json'
   -d '{"email":"my_mail","password":"my_password"}'
```

If data is valid, server will send access token

```json
// Response
// Status: 200 OK
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4NjY4Mzg2OSwianRpIjoiYTM1NDZmYmU2OTg1NDlkZTg4ODVhZTBhMzQ5ZDBiYzQiLCJ1c2VyX2lkIjo0fQ.EBeBY6JpX5TQaP_Ek__3xi-zxb887uWXQQqtDOC2q48",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjc4MTMwMjY5LCJqdGkiOiJmMWU0M2ZlZTgxYjc0MTFhODkwNDk2ZjUzMDViOTk1ZiIsInVzZXJfaWQiOjR9.hvH-uI0fX39Etug9rNYuOtRyNED8SbHtTlEA04FdODo"
}
```

Otherwise, it will send an error response

```json
// Response
// Status: 401 Unauthorized
{
    "detail": "invalid email or password",
    "access": null,
    "refresh": null
}
```

After few days access token will be **expired** and you (user) can’t access data anymore with current access token. For not bother user each time, you must send **POST** request to get new access token with **refresh** token. In the body of request client must enter just refresh token.

Example in Bash:

```bash
curl -X POST http://...../api/v1/auth/token/refresh/' \
--data '{
	"refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4NjY4ODg0NCwianRpIjoiYWE2ZTdiOGE3N2M5NDU3YTlkOGQ1ZDc3ZTgwNDFjNjIiLCJ1c2VyX2lkIjo1fQ.04NV9HkNNbQXFuD-_HCrHTVqAaMESBsVKQB1B2ZIlfk"
}'
```

If data is valid, server will send access token

```json
// Response
// Status: 200 OK
{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjc4MTMwMjY5LCJqdGkiOiJmMWU0M2ZlZTgxYjc0MTFhODkwNDk2ZjUzMDViOTk1ZiIsInVzZXJfaWQiOjR9.hvH-uI0fX39Etug9rNYuOtRyNED8SbHtTlEA04FdODo"
}
```

Otherwise, it will send an error response

```json
// Response
// Status: 401 Unauthorized
{
    "detail": "Token is invalid or expired",
    "code": "token_not_valid"
}
```

After getting `access` and `refresh` token client authenticated successfully and it can send almost every request. But keep in mind, you must set special header in order to access data.

### User Requests

**GET** **Request Example**

```bash
curl -X GET https://..../api/v1/auth/users/me/
   -H 'Content-Type: application/json'
   -H 'Authorization: Token ${TOKEN}'
```

Server’s response:

```json
// Response
// Status: 200 OK
{
    "id": 4,
    "name": "Abdulaziz Abduvakhobov",
    "email": "hello@gmail.com",
    "birth_date": "2000-01-01",
    "address": "Tashkent",
    "gender": "M",
    "identity_number": null,
    "weight": null,
    "height": null,
    "last_login": "2023-03-04T10:25:33.029392Z",
    "longitude": 50.2,
    "latitude": 25.1,
    "marial_status": "S",
    "category_name": "Nurse",
    "category_id": 2
}
```

**PATCH** **Request Example**

```bash
curl --location --request PATCH 'https://${BASE_URL}/api/v1/auth/users/me/' \
--header 'Authorization: Token ${TOKEN} \
--data '{
	"height": 170,
	"weight": 72,
	"identity_number": "12345678910"
}'
```

Server’s response:

```json
// Response
// Status: 200 OK
{
    "id": 4,
    "email": "hello@gmail.com",
    "name": "Abdulaziz Abduvakhobov",
    "identity_number": "123456789",
    "gender": "M",
    "birth_date": "2000-01-01",
    "weight": null,
    "height": null,
    "address": "Tashkent",
    "longitude": "50.200000",
    "latitude": "25.100000",
    "marial_status": "S",
    "last_login": "2023-03-05T22:27:59.738304+03:00",
    "category": 1
}
```

**DELETE** **Request Example**

```bash
curl --location --request DELETE 'https://${BASE_URL}/api/v1/auth/users/me/' \
     --header 'Authorization: Token ${TOKEN}'
```

Server’s response:

```json
// Response
// Status: 200 OK
{
    "message": "User successfully deleted."
}
```

### Content Requests

**GET** **Request Example**

```bash
curl -X GET https://..../api/v1/auth/contents/
   -H 'Content-Type: application/json'
   -H 'Authorization: Token ${TOKEN}'
```

Server’s response:

```json
// Response
// Status: 200 OK
[
    {
        "id": 1,
        "title": "Hello World",
        "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Faucibus et molestie ac feugiat sed lectus vestibulum mattis. Urna nec tincidunt praesent semper feugiat. Duis ultricies lacus sed turpis. Elementum integer enim neque volutpat ac tincidunt vitae semper quis.",
	"file": "https://ebebul.uc.r.appspot.com/files/documents/index.html"
        "date_created": "2023-04-18T22:04:48.290174+03:00",
        "date_updated": "2023-04-18T22:04:48.290199+03:00",
    },
    {
        "id": 2,
        "title": "Guten Abend!",
        "text": "Vestibulum lectus mauris ultrices eros in cursus turpis. Velit aliquet sagittis id consectetur purus ut faucibus. Dictum non consectetur a erat nam. Quam adipiscing vitae proin sagittis nisl rhoncus. Egestas integer eget aliquet nibh praesent tristique magna. Felis bibendum ut tristique et egestas. Cras pulvinar mattis nunc sed blandit libero volutpat sed. Magna fringilla urna porttitor rhoncus dolor purus non enim praesent. Dolor sit amet consectetur adipiscing elit pellentesque habitant morbi tristique. Et malesuada fames ac turpis.",
        "file": "https://ebebul.uc.r.appspot.com/files/documents/index.html"
	"date_created": "2023-04-18T22:04:48.290174+03:00",
        "date_updated": "2023-04-18T22:04:48.290199+03:00",
    }
]
```

**GET** **Request Example**

```bash
curl -X GET https://..../api/v1/auth/contents/1/ # ID of Content
   -H 'Content-Type: application/json'
   -H 'Authorization: Token ${TOKEN}'
```

Server’s response:

```json
// Response
// Status: 200 OK
{
    "id": 1,
    "title": "Hello World",
    "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Faucibus et molestie ac feugiat sed lectus vestibulum mattis. Urna nec tincidunt praesent semper feugiat. Duis ultricies lacus sed turpis. Elementum integer enim neque volutpat ac tincidunt vitae semper quis.",
    "file": "https://ebebul.uc.r.appspot.com/files/documents/index.html"
    "date_created": "2023-04-18T22:04:48.290174+03:00",
    "date_updated": "2023-04-18T22:04:48.290199+03:00",
}
```

**GET** **Request Example**

```bash
curl -X GET https://..../api/v1/auth/contents/1/file/ # ID of Content
   -H 'Content-Type: application/json'
   -H 'Authorization: Token ${TOKEN}'
```

Server’s response:

```html
<!-- Server returns content of uploaded file otherwise 404 error -->
<!doctype html>
<html lang="en">
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>Bootstrap demo</title>
	<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-KK94CHFLLe+nY2dmCWGMq91rCGa5gtU4mk92HdvYe+M/SXH301p5ILy+dN9+nJOZ" crossorigin="anonymous">
</head>
<body>
	<h1>Hello, world!</h1>
	<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ENjdO4Dr2bkBIFxQpeoTz1HIcje39Wm4jDKdf19U8gI4ddQ3GYNS7NTKfAdVQSZe" crossorigin="anonymous"></script>
</body>
</html>
```

### Video Requests

**GET** **Request Example**

```bash
curl -X GET https://..../api/v1/auth/videos/
   -H 'Content-Type: application/json'
   -H 'Authorization: Token ${TOKEN}'
```

Server’s response:

```json
// Response
// Status: 200 OK
[
    {
        "id": 1,
        "name": "New",
        "url": "https://www.youtube.com/watch?v=YxG7PhZ3fb4",
        "description": "Speed up your Rust code with Rayon",
	"date_created": "2023-04-18T22:04:48.290174+03:00",
    	"date_updated": "2023-04-18T22:04:48.290199+03:00",
    },
    {
        "id": 2,
        "name": "Low Level Learning",
        "url": "https://youtu.be/qWVRJsaUTIg",
        "description": "Nam at lectus urna duis convallis convallis. Nunc pulvinar sapien et ligula. Lorem ipsum dolor sit amet consectetur. Etiam non quam lacus suspendisse faucibus interdum posuere lorem. Sit amet commodo nulla facilisi nullam vehicula ipsum. Velit scelerisque in dictum non consectetur a. Cursus turpis massa tincidunt dui ut ornare lectus sit. Pellentesque sit amet porttitor eget.",
	"date_created": "2023-04-18T22:04:48.290174+03:00",
    	"date_updated": "2023-04-18T22:04:48.290199+03:00",
    }
]
```

**GET** **Request Example**

```bash
curl -X GET https://..../api/v1/auth/videos/2/ # ID of Video
   -H 'Content-Type: application/json'
   -H 'Authorization: Token ${TOKEN}'
```

Server’s response:

```json
// Response
// Status: 200 OK
{
    "id": 2,
    "name": "Low Level Learning",
    "url": "https://youtu.be/qWVRJsaUTIg",
    "description": "Nam at lectus urna duis convallis convallis. Nunc pulvinar sapien et ligula. Lorem ipsum dolor sit amet consectetur. Etiam non quam lacus suspendisse faucibus interdum posuere lorem. Sit amet commodo nulla facilisi nullam vehicula ipsum. Velit scelerisque in dictum non consectetur a. Cursus turpis massa tincidunt dui ut ornare lectus sit. Pellentesque sit amet porttitor eget.",
    "date_created": "2023-04-18T22:04:48.290174+03:00",
    "date_updated": "2023-04-18T22:04:48.290199+03:00",
}
```

### Hospital Requests

**GET** **Request Example**

```bash
curl -X GET https://..../api/v1/auth/hospitals/
   -H 'Content-Type: application/json'
   -H 'Authorization: Token ${TOKEN}'
```

Server’s response:

```json
// Response
// Status: 200 OK
[
    {
        "id": 1,
        "name": "Ümraniye Devlet Hastanesi",
        "location": "Umraniye",
	"date_created": "2023-04-18T22:04:48.290174+03:00",
	"date_updated": "2023-04-18T22:04:48.290199+03:00",
    },
    {
        "id": 2,
        "name": "Üsküdar Devlet Hastanesi",
        "location": "Üsküdar",
	"date_created": "2023-04-18T22:04:48.290174+03:00",
	"date_updated": "2023-04-18T22:04:48.290199+03:00",
    }
]
```

**GET** **Request Example**

```bash
curl -X GET https://..../api/v1/auth/hospitals/2/ # ID of Hospital
   -H 'Content-Type: application/json'
   -H 'Authorization: Token ${TOKEN}'
```

Server’s response:

```json
// Response
// Status: 200 OK
{
    "id": 2,
    "name": "Üsküdar Devlet Hastanesi",
    "location": "Üsküdar",
    "date_created": "2023-04-18T22:04:48.290174+03:00",
    "date_updated": "2023-04-18T22:04:48.290199+03:00",
}
```

### Appointments

**GET** **Request Example**

```bash
curl -X GET https://..../api/v1/auth/visits/
   -H 'Content-Type: application/json'
   -H 'Authorization: Token ${TOKEN}'
```

Server’s response:

```json
// Response
// Status: 200 OK
[
    {
        "id": 1,
        "datetime": "2023-03-04T13:14:20+03:00",
        "location": "Virtual Office",
        "visitor": 2, // ID of User
        "user": 1, // ID of User
	"date_created": "2023-04-18T22:04:48.290174+03:00",
	"date_updated": "2023-04-18T22:04:48.290199+03:00",
    },
    {
        "id": 2,
        "datetime": "2023-03-05T22:09:54+03:00",
        "location": "Tashkent",
        "visitor": 2, // ID of User
        "user": 5, // ID of User
	"date_created": "2023-04-18T22:04:48.290174+03:00",
	"date_updated": "2023-04-18T22:04:48.290199+03:00",
    }
]
```

**GET** **Request Example**

```bash
curl -X GET https://..../api/v1/auth/visits/2/ # ID of Visit
   -H 'Content-Type: application/json'
   -H 'Authorization: Token ${TOKEN}'
```

Server’s response:

```json
// Response
// Status: 200 OK
{
    "id": 2,
    "datetime": "2023-03-05T22:09:54+03:00",
    "location": "Tashkent",
    "visitor": 2, // ID of User
    "user": 5, // ID of User
    "date_created": "2023-04-18T22:04:48.290174+03:00",
    "date_updated": "2023-04-18T22:04:48.290199+03:00",
}
```
