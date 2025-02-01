#include<stdio.h>
#include<stdlib.h>
#include<time.h>

void SWAP(int* pa, int* pb) {
	int temp;
	temp = *pa;
	*pa = *pb;
	*pb = temp;
	return;
}
void PRINT(int* pArr, int num) {
	for (int i = 0; i < num; i++) {
		printf("%d ", *(pArr + i));
	}
	printf("\n");
	return;
}


void insertionSort(int* pArr, int num) {
	int i, j, temp;
	for (i = 1; i < num; i++) {
		temp = pArr[i];
		for (j = i - 1; j >= 0 && pArr[j] > temp; j--) {
			pArr[j + 1] = pArr[j];
		}
		pArr[j + 1] = pArr[j];
	}
	return;
}

void main() {
	int pArr[10] = { 0 };
	srand((unsigned int)time(NULL));
	for (int i = 0; i < 10; i++) {
		pArr[i] = rand() / 300;
	}
	printf("정렬 전 배열 : ");
	PRINT(pArr, 10);
	insertionSort(pArr, 10);
	printf("정렬 후 배열 : ");
	PRINT(pArr, 10);
}