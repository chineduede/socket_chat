# Multi-user Chatroom Using Sockets

Inspired by https://beej.us/guide/bgnet0/html/split/project-multiuser-chat-client-and-server.html#project-multiuser-chat-client-and-server

### How to use

Run the server

`python server.py -p <port>`

Run the client

`python client.py -p <server_port> -n <username> --host <localhost>`

Commands

1. To send direct message to user, `/message <username> <message>`
2. To list available users, `/list-users`
3. To send emotes, `/emote <ex: sending love to everyone>`
4. To quit, `/q`
