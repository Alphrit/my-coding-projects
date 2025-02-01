#include<stdio.h>
void arrInput(int* pArr, int num) {
	for (int i = 0; i < num; i++) {
		printf("arr[%d] : ", i);
		scanf_s("%d", &pArr[i]);
	}
	return;
}
void arrOutput(const int* pArr, int num) {
	printf("\n arrIndex Value Histogram \n");
	for (int i = 0; i < num; i++) {
		printf("%6d", i);
		printf("%8d  ", pArr[i]);
		for (int a = 0; a < pArr[i]; a++) {
			printf("*");
		}
		printf("\n");
	}
	return;
}

void main() {
	printf("10개의 배열 원소를 입력하시오!!! \n");
	int pArr[10];
	arrInput(pArr, 10);
	arrOutput(pArr, 10);
	return;
}