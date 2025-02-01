#include <stdio.h>             // printf 함수, scanf_s 함수를 사용하기 위해!
#include <malloc.h>            // malloc 함수를 사용하기 위해!
#include <memory.h>            // memcpy 함수를 사용하기 위해!
#include <string.h>
#include<stdlib.h>
#include <stdbool.h>
#define _CRT_SECURE_NO_WARNINGS

#ifndef _INFOR_
#define _INFOR_

typedef struct infor
{
    char name[10];  // 이름을 저장할 변수
    char score;
    int id, kor, eng, math;          // 학번, 국어, 영어, 수학 성적을 저장할 변수
    int total;                   // 총점을 저장할 변수
    int ranking;                 // 등수를 저장할 변수
    float average;               // 평균을 저장할 변수

} Infor;

typedef struct _node {
    Infor data;                     // 학생 정보를 기록할 변수
    struct _node* link;         // 다음 노드를 가리킬 포인터
} NODE;
NODE* A = NULL, * B = NULL;
Infor temp;
int fin = 0;

#endif
