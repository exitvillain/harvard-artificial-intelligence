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
                line[lengthOfLine++] = buf[i];
            }
            else
            {
                if (iteration == 1)
                {
                    line[lengthOfLine] = '\0';
                    printf(1, "%s\n", line);
                    lengthOfLine = 0;
                    // write buf to prevBuf
                    strcpy(prevBuf, line);
                    iteration = 2;
                }
                else
                {
                    if (strcmp(prevBuf, line) != 0)
                    {
                        // write buf to prevBuf
                        line[lengthOfLine] = '\0';
                        lengthOfLine = 0;
                        strcpy(prevBuf, line);
                        // print buf to screen
                        printf(1, "%s\n", prevBuf);
                    }
                    else
                    {
                        lengthOfLine = 0;
                    }
                }
            }
        }
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