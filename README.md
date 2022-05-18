
# Backend for diploma

Technologies used:

- Python
- Django
- Django REST framework
## API Endpoints

#### Register user

```http
  POST /api/register
```

| Body Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `first_name` | `string` | First name |
| `second_name` | `string` | Last name |
| `position` | `string` | Position |
| `username` | `string` | Username |
| `email` | `string` | Email |
| `password` | `string` | Password |
| `password2` | `string` | Confirmation password |


```http
  POST /api/login
```

| Body Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username` | `string` | Username |
| `password` | `string` | Password |


#### Upload flows

```http
  POST /api/flows/upload
```

| Path Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `token[maybe]` | `string` | **Required**. Your token |

| Body Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `file` | `document` | Excel document |

#### Get available loads by subject

```http
  GET /api/load/available/by_subject
```

| Path Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `token[maybe]` | `string` | **Required**. Your token |


#### Get available loads by groups

```http
  GET /api/load/available/by_groups
```

| Path Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `token[maybe]` | `string` | **Required**. Your token |
