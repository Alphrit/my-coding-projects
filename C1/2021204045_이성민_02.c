#include<stdio.h>
void revPrint(const char* pStr) {
	int a = 0;
	while (pStr[a]) {
		a++;
	}
	for (a; a >= 0; a--) {
		printf("%c", pStr[a]);
	}

}

int main() {
	printf("문자열 입력 : ");
	char pStr[64];
	scanf_s("%[^\n]c", &pStr, sizeof(pStr));
	revPrint(pStr);
}