# Server-Client-Tic-Tac-Toe
A distributed implementation of a tic-tac-toe game using a server-client model

**Usage:**
This tic-tac-toe game can be run either on a single machine or on different machines over the internet.
To begin, start the server in a shell on a machine with an internet connection, and provide a single argument indicating a port to listen on( e.g. `python server.py 47003` )
Next, each of the two players should start their client in a shell, providing the IP address or DNS address of the server's machine, and the port that the server is listening on (e.g. `python client.py 72.171.30.187 47003`)

The first player to connect to the server will be assigned as player X, and must wait until the second player connects and is assigned as player O. After the second player connects, each player will be sent the blank game board, and then the updated board will be displayed again after each valid move is made. Each player can submit any moves to the server, but any moves made out of turn or where the space is already taken will be rejected and the player will be informed.

Recognized messages to the server:
R - resign. This ends the game and indicates to the non-resigning player that the other has resigned and that they have won.
? - help. This command displays the help prompt, outlining the valid move protocol and server messages.
M<R><C> - Make a move. This command submits a move to the server for validation, where R is the row (1, 2, or 3) and C is the column (A, B, or C), e.g. "MB1" will attempt to make a mark in the first row of column A.
