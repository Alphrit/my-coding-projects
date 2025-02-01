#include "infor.h"

void search_member(infor* pArr, infor* pArr2, infor* plus, int num) {
	FILE* fp = NULL;
	fopen_s(&fp, "member.dat", "rb");
	if (fp == NULL) {
		printf("파일 개방 실패!");
		fclose(fp);
		exit(0);
	}

	fread(&pArr, sizeof(pArr), 1, fp);
	printf("검색할 사용자 ID를 입력하십시오 : ");

	char id[10], ch;
	int op, n = 0;
	scanf_s("%s", &id, sizeof(id));
	for (int i = 0; i < num; i++) {
		if (strcmp(id, pArr[i].ID) == 0) {
			printf("\n> 번 호     : ");
			printf("%d", pArr[i].Num);
			printf("\n> 회원ID    : ");
			printf("%s", pArr[i].ID);
			printf("\n1. 비밀번호 : ");
			printf("%s", pArr[i].Password);
			printf("\n2. 이 름    : ");
			printf("%s", pArr[i].Name);
			printf("\n3. 성 별    : ");
			printf("%s", pArr[i].Gender);
			printf("\n4. 나 이    : ");
			printf("%s", pArr[i].Age);
			printf("\n5. 직 위    : ");
			printf("%s", pArr[i].JobPosition);
			printf("\n6. 회사명   : ");
			printf("%s", pArr[i].Conpany);
			printf("\n7. 주 소    : ");
			printf("%s", pArr[i].Address);
			printf("\n8. 우편번호 : ");
			printf("%s", pArr[i].ZipCode);
			printf("\n9. 전화번호 : ");
			printf("%s", pArr[i].TelephoneNum);
			printf("\n10. 휴대폰  : ");
			printf("%s", pArr[i].PhoneNum);
			n++;
		}
		if (!(n > 0)) {
			printf("사용자를 찾을 수 없습니다...");
		}
		fclose(fp);
		printf("\nM)메인, Q)종료 : ");
		char Menu = _getch();
		switch (Menu) {
		case 'M':
		case 'm':
			system("cls");
			printTitle(pArr, pArr2, plus, num);
		case 'Q':
		case 'q':
			exit(0);
		default:
			break;
		}
	}
	return;
}