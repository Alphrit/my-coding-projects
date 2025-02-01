#include<stdio.h>
#include<Windows.h>
#include<time.h>
#include<stdlib.h>
#include<conio.h>
#include<string.h>
#define _CRT_SECURE_NO_WARNINGS

#ifndef _INFOR_
#define _INFOR_

typedef struct INFOR {
    unsigned long Num;
    char ID[10];
    char Password[10];
    char Name[20];
    char Gender[2];
    char Age[3];
    char JobPosition[20];
    char Conpany[30];
    char Address[30];
    char ZipCode[7];
    char TelephoneNum[15];
    char PhoneNum[15];
}infor;



#endif

void printTitle(infor* pArr, infor* pArr2, infor* plus, int num);
void insert_member(infor* pArr, infor* pArr2, infor* plus, int num);
void modify_member(infor* pArr, infor* pArr2, infor* plus, int num);
void search_member(infor* pArr, infor* pArr2, infor* plus, int num);
void list_member(infor* pArr, infor* pArr2, infor* plus, int num);
void view_help(infor* pArr, infor* pArr2, infor* plus, int num);