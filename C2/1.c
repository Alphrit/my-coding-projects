#include <stdio.h>
#include <string.h>
typedef struct _score {
	char name[10], department[10], phone[20], address[20], num[20];
	char month, day;
	short year;
}SCORE;

int main() {
	printf("학    번: ");
	gets_s(SCORE->num, sizeof(SCORE->num));
	printf("학    과: ");
	gets_s(SCORE->department, sizeof(SCORE->department);
	printf("이    름: ");
	gets_s(SCORE->name, sizeof(SCORE->name));
	printf("연락처: ");
	gets_s(SCORE->num, sizeof(SCORE->num));
	printf("주   소: ");
	gets_s(SCORE->address, sizeof(SCORE->address));
	printf("생년월일: ");
	scanf_s("%d%*c%d%*c&d", &SCORE.year, &SCORE.month, &SCORE.day, sizeof(SCORE->year + SCORE->month + SCORE->day));


	printf("\n##### 학생 정보 #####\n");
	printf("학번: %s", SCORE.num);
	printf("학(부)과: %s", SCORE.department);
	printf("이름: %s", SCORE.name);
	printf("연락처: %s", SCORE.phone);
	printf("주소: &s", SCORE.address);
	printf("%d-%d-%d", SCORE.year, SCORE.month, SCORE.day);
	return 0;
}