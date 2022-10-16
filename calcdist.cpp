#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>

const char*  ProgName = "calcdist";  // プログラム名
const int    MaxDatas = 100;         // 最大キー打鍵数

class Distance
{
public:
  char*   User;
  char*   Cond;
  char*   key;
  int     Num;
  double  dat[MaxDatas];
public:
  enum {
	USER, COND, KEY, DAT
  };
  Distance()
  {
    User = Cond = key = NULL;
    Num = 0;
  }
  ~Distance()
  {
    if(User)
      delete []User;
    if(Cond)
      delete []Cond;
    if(key)
      delete []key;
  }
public:
  void  Add(const char* buf)
  {
    char*  tmp = strdup(buf);
    char*  p;

    if(p = strtok(tmp, ",\t\r\n")){
      int  n = 0;
      do {
	switch(n){
	case  USER:
	  User = strdup(p);
	  break;
	case  COND:
	  Cond = strdup(p);
	  break;
	case  KEY:
	  key = strdup(p);
	  break;
	default:
	  if(Num < MaxDatas){
	    dat[Num] = atof(p);
	    Num++;
	  }
	  else {
	    printf("Overflow !\n");
	    exit(-1);
	  }
	  break;
	}
	n++;
	// printf("[%s]", p);
      } while(p = strtok(NULL, ",\t\r\n"));
    }
    
    if(tmp)
      delete  []tmp;
  }
  void  Show()
  {
    printf("%s\t%s\t%s\t", User, Cond, key);
    for(int i=0; i<Num; i++){
      printf("%s%.3f", i ? "\t" : "", dat[i]);
    }
    printf("\n");
  }
};

const int  MaxDist = 1000;

class  CalcDistance
{
public:
  int       Num;
  Distance  Dist[MaxDist];
public:
  CalcDistance()
  {
    Num = 0;
  }
  ~CalcDistance()
  {
  }
public:
  void  Add(const char* buf)
  {
    if(Num < MaxDist){
      Dist[Num].Add(buf);
      Num++;
    }
  }
  void  Load(FILE* fp)
  {
    if(! fp)
      return;

    char  buf[1024];
    while(fgets(buf, sizeof(buf), fp)){
      if(! *buf)
	continue;
      Add(buf);
    }
  }
  void  Show()
  {
    for(int i=0; i<Num; i++){
      Dist[i].Show();
    }
  }
  void  Run(char* fname = NULL)
  {
    FILE*  fp = stdin;

    if(fname)
      fp = fopen(fname, "r");

    if(! fp){
      perror(ProgName);
      exit(-1);
    }
    Load(fp);
    Show();
    Calc("ando", "fast", "orinnpikku", 4);
  }
  void  Calc(const char* user, const char* cond, const char* key, int lnum);
};

void  CalcDistance::Calc(const char* user, const char* cond, const char* key, int lnum)
{
  if(! user || ! cond || ! key)
    return;

  double  avg[MaxDatas] = {0.0};
  int     n = 0;
  int     nn = 0;
  int     isdone = false;
  
  for(int i=0; i<Num; i++){
    if(strcmp(user, Dist[i].User) != 0 && strcmp(cond, Dist[i].Cond) != 0 && strcmp(key, Dist[i].key) != 0)
      continue;
    if(n < lnum){
      int  j;
      printf("[%d]\t", n);
      for(j=0; j<Dist[i].Num; j++){
	printf("%s%.3f", j ? "\t" : "", Dist[i].dat[j]);
	avg[j] += Dist[i].dat[j];
      }
      printf("\n");
      nn = j;
      n++;
    }
    else {
      // 平均値の計算
      if(! isdone){
	printf("%s\t%s\t%s\t[avg]\t", Dist[i].User, Dist[i].Cond, Dist[i].key);
	for(int j=0; j<nn; j++){
	  avg[j] /= n;
	  printf("%s%.3f", j ? "\t" : "", avg[j]);
	}
	printf("\n");
	isdone = true;
      }
      else {
	if(strcmp(cond, Dist[i].Cond) != 0 && strcmp(key, Dist[i].key) != 0)
	  continue;
	
	// ユークリッド距離（偏差自乗和）の計算
	double  std = 0.0;

	printf("%s\t%s\t%s\t[std]\t", Dist[i].User, Dist[i].Cond, Dist[i].key);
	for(int j=0; j<nn; j++){
	  std += (avg[j] - Dist[i].dat[j]) * (avg[j] - Dist[i].dat[j]);
	}
	std = sqrt(std);
	printf("%.3f\n", std);
      }
    }
  }
}


int  main(int argc, char** argv)
{
  CalcDistance().Run(argc == 1 ? NULL : argv[1]);

  return  0;
}
