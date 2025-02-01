#include<stdio.h>
#include <stdlib.h>   
double my_atof(const char* pStr) {
	return atof(pStr);
}
void main() {
	char str[64];
	printf("실수로 변환할 문자열 입력 : ");
	scanf_s("%s", str, sizeof(str));
	printf("입력 문자열 : %s, 변환된 숫자(double): %1f", str, my_atof(str));
	return;
}
