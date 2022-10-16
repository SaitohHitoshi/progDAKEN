#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// int  fexist(const char* name)
// {
//   if(! name || ! *name)
//     return  false;

//   FILE*  fp = fopen(name, "r");
//   if(fp){
//     fclose(fp);
//     return  true;
//   }
//   return  false;
// }


void  Run(char* fname)
{
  FILE*  fp = fopen(fname, "r");
  if(! fp){
    perror("toutf8");
    exit(-1);
  }
  if(fp)
    fclose(fp);

  char*  p;
  
  p = strstr(fname, ".utf8.txt");
  if(p){
    printf("Already exist.\n");
    return;
  }
  p = strstr(fname, ".txt");
  if(p)
    *p = 0;
  
  char  cmd[1024];
  sprintf(cmd, "nkf %s.txt > %s.utf8.txt", fname, fname);
  system(cmd);
}

int  main(int argc, char** argv)
{
  if(argc > 1)
    Run(argv[1]);
  return  0;
}
