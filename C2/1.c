#include <stdio.h>
#include <string.h>
typedef struct _score {
	char name[10], department[10], phone[20], address[20], num[20];
	char month, day;
	short year;
}SCORE;

int main() {
	printf("��    ��: ");
	gets_s(SCORE->num, sizeof(SCORE->num));
	printf("��    ��: ");
	gets_s(SCORE->department, sizeof(SCORE->department);
	printf("��    ��: ");
	gets_s(SCORE->name, sizeof(SCORE->name));
	printf("����ó: ");
	gets_s(SCORE->num, sizeof(SCORE->num));
	printf("��   ��: ");
	gets_s(SCORE->address, sizeof(SCORE->address));
	printf("�������: ");
	scanf_s("%d%*c%d%*c&d", &SCORE.year, &SCORE.month, &SCORE.day, sizeof(SCORE->year + SCORE->month + SCORE->day));


	printf("\n##### �л� ���� #####\n");
	printf("�й�: %s", SCORE.num);
	printf("��(��)��: %s", SCORE.department);
	printf("�̸�: %s", SCORE.name);
	printf("����ó: %s", SCORE.phone);
	printf("�ּ�: &s", SCORE.address);
	printf("%d-%d-%d", SCORE.year, SCORE.month, SCORE.day);
	return 0;
}