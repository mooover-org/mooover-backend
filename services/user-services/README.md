# Mooover User Microservices

## About

Microservices for user related operations.

- URL prefix: `/api/v1/users`
- Documentation: `/api/v1/users/docs`

## Endpoints

- `GET /ping`: ping the service
- `GET /{id}`: get a user's data
- `GET /`: get all users data
- `POST /`: register a new user
- `PUT /{id}`: update user data
- `GET /{id}/steps`: get user's daily and weekly steps
- `GET /{id}/group`: get user's group data

For more info check the documentation.

## Contributing

You will need to import the `corelib` library to have access to basic data structures and functionalities.
