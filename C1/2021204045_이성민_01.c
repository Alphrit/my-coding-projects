#include<stdio.h>
void PRINT(int num) {
	for (int i = 1; i < 10; i++) {
		printf("%d * %d = %d\n", num, i, num * i);
	}
	return;
}
int main() {
	printf("���ϴ� ������(1 ~ 9) : ");
	int num = 0;
	scanf_s("%d", &num);
	if (num >= 0 && num <= 9) {
		PRINT(num);
	}
	else {
		printf("1 ~ 9 ������ ������ �Է����ּ���.");
	}
	return 0;
}