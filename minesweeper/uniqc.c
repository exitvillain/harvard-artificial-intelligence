void uniqc(int fd, char *name)
{
    int z = 1;

    while ((n = read(fd, buf, sizeof(buf))) > 0)
    {
        int i;
        int iteration = 1;
        int lengthOfLine = 0;
        //flag can be 0,1, or 2
        //int flag = 0;
        //int z = 1 ;

        for (i = 0; i <= n; i++)
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
                    lengthOfLine = 0;
                    // write buf to prevBuf
                    strcpy(prevBuf, line);
                    iteration = 2;
                }
                else
                {
                    if (strcmp(prevBuf, line) == 0)
                    {
                        // write buf to prevBuf
                        line[lengthOfLine] = '\0';
                        strcpy(prevBuf, line);
                        //flag = flag + 1;
                        z = z + 1;
                        //if ((i+5)> n)
                        //{

                        //printf(1, "%d %s\n", z-1, prevBuf);
                        //}
                        lengthOfLine = 0;
                    }
                    else
                    {
                        if (z == 1)
                        {
                            //strcpy(prevBuf, line);
                            printf(1, "%d %s\n", z, prevBuf);
                            strcpy(prevBuf, line);
                        }
                        else
                        {
                            printf(1, "%d %s\n", z, prevBuf);
                            //printf(1, "%d %s\n", z, line);

                            //strcpy(prevBuf, line);
                            z = 1;
                            strcpy(prevBuf, line);
                        }
                        if (i + 5 > n)
                        {
                            prevBuf[lengthOfLine] = '\0';
                            printf(1, "%d %s", z, prevBuf);
                        }

                        line[lengthOfLine] = '\0';
                        lengthOfLine = 0;
                    }
                }
            }
        }
    }
    //WHAT I WANT TO DO TO Get that Last LIne, BUT THE FOLLOWING CODE DOESNT WORK
    printf(1, "%d %s", z, line);

    exit();
}