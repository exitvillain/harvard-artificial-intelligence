#include "types.h"
#include "stat.h"
#include "user.h"

//I think I need to import some sys library
//is it # <include <stdio.h>??

char buf[1024];
char prevBuf[1024] = "";
//int iteration = 1;
int n;

//char *text[1024];
char line[1024] = "";
char compareBuf[1024] = "";
char prevCompareBuf[1024] = "";

void uniq(int fd, char *name)
{
    while ((n = read(fd, buf, sizeof(buf))) > 0)
    {

        int i;
        int iteration = 1;
        int lengthOfLine = 0;
        for (i = 0; i < n; i++)
        {
            if (buf[i] != '\n')
            {
                line[lengthOfLine] = buf[i];
                if ((buf[i] >= 97) && (buf[i] <= 122))
                {
                    compareBuf[lengthOfLine] = buf[i] - 32;
                }
                else
                {
                    compareBuf[lengthOfLine] = buf[i];
                }
                lengthOfLine = lengthOfLine + 1;
            }
            else
            {
                if (iteration == 1)
                {
                    line[lengthOfLine] = '\0';
                    compareBuf[lengthOfLine] = '\0';
                    printf(1, "%s\n", line);
                    lengthOfLine = 0;
                    // write buf to prevBuf
                    strcpy(prevBuf, line);
                    strcpy(prevCompareBuf, compareBuf);
                    iteration = 2;
                }
                else
                {

                    if (strcmp(prevCompareBuf, compareBuf) != 0)
                    {
                        // write buf to prevBuf
                        line[lengthOfLine] = '\0';
                        compareBuf[lengthOfLine] = '\0';
                        lengthOfLine = 0;
                        strcpy(prevBuf, line);
                        strcpy(prevCompareBuf, compareBuf);
                        // print buf to screen
                        printf(1, "%s\n", prevBuf);
                    }
                    else
                    {
                        //compareBuf[lengthOfLine] = '\0';
                        lengthOfLine = 0;
                    }
                }
            }
        }
        //I will try to implement D
    }

    exit();
}

int main(int argc, char *argv[])
{
    int fd;

    if (argc <= 1)
    {
        uniq(0, "");
        exit();
    }
    if ((fd = open(argv[1], 0)) < 0)
    {
        printf(1, "uniq: cannot open %s\n", argv[1]);
        exit();
    }

    uniq(fd, argv[1]);

    close(fd);

    exit();
}