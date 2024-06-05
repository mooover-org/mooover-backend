# Mooover Group Microservices

## About

Microservices for group related operations.

- URL prefix: `/api/v1/groups`
- Documentation: `/api/v1/groups/docs`

## Endpoints

- `GET /ping`: ping the service
- `GET /{id}`: get a group's data
- `GET /`: get all groups data
- `POST /`: create a new group
- `PUT /{id}`: update group data
- `DELETE /{id}`: delete group
- `GET /{id}/members`: get group's members data
- `PUT /{id}/members`: add member to group
- `DELETE /{group_id}/members/{user_id}`: remove member from group

For more info check the documentation.

## Contributing

You will need to import the `corelib` library to have access to basic data structures and functionalities.
