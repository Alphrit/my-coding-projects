#include <stdio.h>             // printf �Լ�, scanf_s �Լ��� ����ϱ� ����!
#include <malloc.h>            // malloc �Լ��� ����ϱ� ����!
#include <memory.h>            // memcpy �Լ��� ����ϱ� ����!
#include <string.h>
#include<stdlib.h>
#include <stdbool.h>
#define _CRT_SECURE_NO_WARNINGS

#ifndef _INFOR_
#define _INFOR_

typedef struct infor
{
    char name[10];  // �̸��� ������ ����
    char score;
    int id, kor, eng, math;          // �й�, ����, ����, ���� ������ ������ ����
    int total;                   // ������ ������ ����
    int ranking;                 // ����� ������ ����
    float average;               // ����� ������ ����

} Infor;

typedef struct _node {
    Infor data;                     // �л� ������ ����� ����
    struct _node* link;         // ���� ��带 ����ų ������
} NODE;
NODE* A = NULL, * B = NULL;
Infor temp;
int fin = 0;

#endif
