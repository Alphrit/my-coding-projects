#include<stdio.h>
#include <stdlib.h>   
double my_atof(const char* pStr) {
	return atof(pStr);
}
void main() {
	char str[64];
	printf("�Ǽ��� ��ȯ�� ���ڿ� �Է� : ");
	scanf_s("%s", str, sizeof(str));
	printf("�Է� ���ڿ� : %s, ��ȯ�� ����(double): %1f", str, my_atof(str));
	return;
}
