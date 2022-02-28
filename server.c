#include<stdio.h>
#include<string.h>
#include<sys/socket.h>
#include<arpa/inet.h>
#include<unistd.h>
short SocketCreate(void)
{
    short hSocket;
    printf("Create the socket\n");
    hSocket = socket(AF_INET, SOCK_STREAM, 0);
    return hSocket;
}
int BindCreatedSocket(int hSocket)
{
    int iRetval=-1;
    int ClientPort = 90190;
    struct sockaddr_in  remote= {0};
    /* Internet address family */
    remote.sin_family = AF_INET;
    /* Any incoming interface */
    remote.sin_addr.s_addr = htonl(INADDR_ANY);
    remote.sin_port = htons(ClientPort); /* Local port */
    iRetval = bind(hSocket,(struct sockaddr *)&remote,sizeof(remote));
    return iRetval;
}
int main(int argc, char *argv[])
{
    int socket_desc, sock, clientLen, read_size;
    struct sockaddr_in server, client;
    char client_message[200]= {0};
    char message[100] = {0};
    const char *pMessage = "hello aticleworld.com";
    //Create socket
    socket_desc = SocketCreate();
    if (socket_desc == -1)
    {
        printf("Could not create socket");
        return 1;
    }
    printf("Socket created\n");
    //Bind
    if( BindCreatedSocket(socket_desc) < 0)
    {
        //print the error message
        perror("bind failed.");
        return 1;
    }
    printf("bind done\n");
    //Listen
    listen(socket_desc, 3);
    //Accept and incoming connection
    while(1)
    {
        printf("Waiting for incoming connections...\n");
        clientLen = sizeof(struct sockaddr_in);
        //accept connection from an incoming client
        sock = accept(socket_desc,(struct sockaddr *)&client,(socklen_t*)&clientLen);
        if (sock < 0)
        {
            perror("accept failed");
            return 1;
        }
        printf("Connection accepted\n");
        memset(client_message, '\0', sizeof client_message);
        memset(message, '\0', sizeof message);
        //Receive a reply from the client
        if( recv(sock, client_message, 200, 0) < 0)
        {
            printf("recv failed");
            break;
        }
        printf("Client reply : %s\n",client_message);
        if(strcmp(pMessage,client_message)==0)
        {
            strcpy(message,"Hi there !");
        }
        else
        {
            strcpy(message,"Invalid Message !");
        }
        // Send some data
        if( send(sock, message, strlen(message), 0) < 0)
        {
            printf("Send failed");
            return 1;
        }
        close(sock);
        sleep(1);
    }
    return 0;
}
