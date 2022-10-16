#include <stdio.h>
#include <string.h>
#include <stdlib.h>

//==============================================================================
// 列挙：AnalyzeMode
// -----------------
// キー間隔を取得するタイミング(UP, DOWN)の指定
//==============================================================================
enum AnalyzeMode
{
 DOWN,
 UP
};

//==============================================================================
// グローバル：
//==============================================================================
const char*  ProgName = "getlog";  // プログラム名称
const char*  Pat[] = {             // 解析モードのパターン識別文字列
  "[D]", "[U]", NULL
};
const int  MaxItems = 500;         // １行分の最大打件数
const int  MaxTimes = 100;         // 文の最大入力回数

int  Mode = DOWN;                  // キー間隔の解析モード


char*  GUser = NULL;
char*  GCond = NULL;

//==============================================================================
// クラス：KeyItem
// ---------------
// １打鍵分の入力時刻と入力キーの名前を格納する
//==============================================================================
class  KeyItem
{
public:
  double  sec;  // キーの打鍵時刻(単位：秒)
  char*   key;  // キー名称
public:
  KeyItem()
  {
    sec = 0.0;
    key = NULL;
  }
  ~KeyItem()
  {
    if(key)
      delete []key;
  }
public:
  //------------------------------------------------------------
  // ログから入力時刻を取得して格納する
  //------------------------------------------------------------
  double GetTime(char* buf)
  {
    if(! buf || ! *buf)
      return  -1;
    char*  p = strstr(buf, " ");
    if(! p)
      return  -1;

    int     hh, mm;
    double  ss;
    sscanf(p+1, "%02d:%02d:%lf", &hh, &mm, &ss);
    return  (double)hh * 3600 + (double)mm * 60 + ss;
  }
  //------------------------------------------------------------
  // １打鍵分のキー情報を格納する
  //------------------------------------------------------------
  char*  Add(char* buf)
  {
    if(! buf || ! *buf)
      return  NULL;

    char*  p = strstr(buf, "ボタン");
    if(p)
      *p = 0;


    sec = GetTime(buf);

    p = strstr(buf, Pat[Mode]);
    if(! p)
      return  NULL;
    
    key = strdup(p + strlen(Pat[Mode]) + 1);
    return  key;
  }
  //------------------------------------------------------------
  // 格納されている情報を表示する
  //------------------------------------------------------------
  void  Show(double top)
  {
    printf("%s\t%.3f\n", key ? key : "null", sec - top);
  }
};


//==============================================================================
// クラス：Sentence
// ----------------
// １行分の打鍵情報を格納する
//==============================================================================
class  Sentence
{
public:
  enum {
	NOTFOUND = -1
  };
  int      Num;
  KeyItem  Item[MaxItems];
public:
  Sentence()
  {
    Num = 0;
  }
  ~Sentence()
  {
  }
public:
  //------------------------------------------------------------
  // １打鍵分のキー情報を格納する
  //------------------------------------------------------------
  char*  Add(char* buf)
  {
    if(! buf || ! *buf)
      return  NULL;

    if(! strstr(buf, Pat[Mode]))
      return  NULL;

    // if(strstr(buf, "Space") || strstr(buf, "Enter"))
    //   return  NULL;

    if(Num < MaxItems){
      char*  p = Item[Num].Add(buf);
      Num++;
    };
    return  buf;
  }
  //------------------------------------------------------------
  // １文中のキー情報を表示する
  //------------------------------------------------------------
  void  Show(int tim)
  {
    for(int i=0; i<Num; i++){
      printf("[%2d][%2d]\t", tim, i);
      Item[i].Show(i ? Item[i - 1].sec : Item[i].sec);
    }
  }
  //------------------------------------------------------------
  // キーフレーズを検索する
  //------------------------------------------------------------
  int  Search(const char* kw, int from=0)
  {
    if(! kw || ! *kw)
      return  NOTFOUND;

    int  n = strlen(kw);
    int  found = true;
    int  i;
    int  j;
    for(i=from; i<Num; i++){
      int  start = i;
      for(j=0; j<n && i < Num; j++){
	// printf("kw[%d]=%c\tItem[%d].kw[0]=%c\n", j, kw[j], i, Item[i].kw[0]);
	if(kw[j] && Item[i].key[0] != kw[j])
	  break;
	i++;
      }
      if(j == n)
	return  start;
    }
    return  NOTFOUND;
  }
  //------------------------------------------------------------
  // 指定したキーフレーズを入力した部分を探索する
  //------------------------------------------------------------
  void  Find(const char* kw, int from=0)
  {
    do {
      int  i = Search(kw, from);
      if(i == NOTFOUND)
	return;

      // printf("Num=[%d], kw=[%s], ret=%d\n", Num, kw, i);


      printf("%s\t%s\t", GUser, GCond);
      
      // key
      int  n = strlen(kw);
      for(int j=0; j<n && i+j < Num; j++){
	printf("%s", Item[i+j].key);
      }
      printf("\t");

      // time
      n = strlen(kw);
      for(int j=0; j<n && i+j < Num; j++){
	printf("%s%.3f", j ? "\t" : "", j ? Item[i+j].sec - Item[i+j-1].sec : 0);
      }
      printf("\n");

      from = i + n;
    } while(from < Num);
  }
};


//==============================================================================
// クラス：Log
// ----------------
// キーログから打鍵間隔を取得し格納する
//==============================================================================
class  Log
{
public:
  int       Tim;             // 入力した文数
  Sentence  Sen[MaxTimes];   // １文単位の打鍵情報
  char*     FName;           // ログファイル名
  char*     User;            // 実験協力者名
  char*     Cond;            // 計測条件名
public:
  Log(const char* fname)
  {
    Tim = 0;
    FName = User = Cond = NULL;

    if(fname)
      FName = strdup(fname);

    GetUserCond();
    GUser = User;
    GCond = Cond;
  }
  ~Log()
  {
    if(FName)
      delete []FName;
    if(User)
      delete []User;
    if(Cond)
      delete []Cond;
  }
public:
  //------------------------------------------------------------
  // １打鍵分のキー情報を格納する
  //------------------------------------------------------------
  void  GetUserCond()
  {
    if(! FName)
      return;

    char*  p = strstr(FName, "./");
    if(! p)
      return;
    p += 2;
    char*  q = strstr(p, "/");
    if(! q)
      return;
    *q = 0;
    User = strdup(p);
    *q = '/';
    p = q + 1;
    q = strstr(p, "/");
    if(! q)
      return;
    *q = 0;
    Cond = strdup(p);
    *q = '/';
  }
  //------------------------------------------------------------
  // １打鍵分のキー情報を格納する
  //------------------------------------------------------------
  void  Add(char* buf)
  {
    if(! buf || ! *buf)
      return;
    if(Tim < MaxTimes){
      
      if(strstr(buf, "OemPeriod") && Tim < MaxTimes){
	if(Sen[Tim].Num)
	  Tim++;
      }
      else {
	Sen[Tim].Add(buf);
      }
    }
  }
  //------------------------------------------------------------
  // キーログファイルから情報を読み込む
  //------------------------------------------------------------
  void  Load()
  {
    char  buf[1024];
    FILE*  fp = stdin;

    if(FName){
      fp = fopen(FName, "r");
      if(! fp){
	perror(ProgName);
	exit(-1);
      }
    }
    else
      fp = stdin;
    while(fgets(buf, sizeof(buf), fp)){
      char*  p = strtok(buf, "\r\n");
      if(! p || ! *p)
	continue;
      Add(p);
    }
    if(fp && fp != stdin)
      fclose(fp);
  }
  //------------------------------------------------------------
  // ログに記録されているすべてのキー情報を表示する
  //------------------------------------------------------------
  void  Show()
  {
    for(int i=0; i<Tim; i++){
      Sen[i].Show(i);
    }
  }
  //------------------------------------------------------------
  // 指定したキーフレーズを入力した部分を探索する
  //------------------------------------------------------------
  void  Find(const char* key)
  {
    for(int i=0; i<Tim; i++){
      printf("(%d)\n", i);
      Sen[i].Find(key);
      printf("\n");
    }
  }
  //------------------------------------------------------------
  // 指定したキーフレーズを取得する
  //------------------------------------------------------------
  void  Analyze()
  {
    const char*  phrase[] = {
       "orinpikku"
       , "orinnpikku"
       , "kikai"
       , "matatonai"
       , "taisou"
       , "sensyu"
       , "sennsyu"
       , "senshu"
       , "sennshu"
       , NULL
      };

    for(int i=0; phrase[i]; i++){
      Find(phrase[i]);
    }
  }
  //------------------------------------------------------------
  // キーログ解析を実行する
  //------------------------------------------------------------
  void  Run()
  {
    printf("User=[%s], Cond=[%s]\n", User, Cond);
    Load();
    Show();
    Analyze();
  }
};

//==============================================================================
// 関数：main
//==============================================================================
int  main(int argc, char** argv)
{
  Mode = DOWN;
  printf("Mode is %s\n"
	 "File is %s\n"
	 , Pat[Mode]
	 , argv[1] ? argv[1] : "(null)"
	 );

  Log(argc >= 2 ? argv[1] : NULL).Run();
  // printf("Terminated Completely\n");
  return  0;
}
