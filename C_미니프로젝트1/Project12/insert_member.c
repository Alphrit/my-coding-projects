#include "infor.h"

void insert_member(infor* pArr, infor* pArr2, infor* plus, int num) {
	FILE* f = NULL;
	fopen_s(&f, "member.dat", "wb");
	if (f == NULL) {
		printf("파일 개방 실패!");
		fclose(f);
		exit(0);
	}
	printf("회원의 기본 정보를 입력하십시오...\n");

	printf("\n> 번 호 : ");
	scanf_s("%d", &plus[num].Num, sizeof(plus[num].Num));


	printf("\n> ID : ");
	scanf_s("%s", &plus[num].ID, sizeof(plus[num].ID));

	printf("\n> 비밀번호 : ");
	scanf_s("%s", &plus[num].Password, sizeof(plus[num].Password));

	printf("\n> 이 름 : ");
	scanf_s("%s", &plus[num].Name, sizeof(plus[num].Name));

	printf("\n> 성 별 : ");
	scanf_s("%s", &plus[num].Gender, sizeof(plus[num].Gender));

	printf("\n> 나 이 : ");
	scanf_s("%s", plus[num].Age, sizeof(plus[num].Age));

	printf("\n> 직 위 : ");
	scanf_s("%s", &plus[num].JobPosition, sizeof(plus[num].JobPosition));

	printf("\n> 회사명 : ");
	scanf_s("%s", &plus[num].Conpany, sizeof(plus[num].Conpany));

	printf("\n> 주 소 : ");
	scanf_s("%s", &plus[num].Address, sizeof(plus[num].Address));

	printf("\n> 우편번호 : ");
	scanf_s("%s", &plus[num].ZipCode, sizeof(plus[num].ZipCode));

	printf("\n> 전화번호 : ");
	scanf_s("%s", &plus[num].TelephoneNum, sizeof(plus[num].TelephoneNum));

	printf("\n> 휴대폰 : ");
	scanf_s("%s", &plus[num].PhoneNum, sizeof(plus[num].PhoneNum));
	
	printf("S)저장, M)메인, Q)종료 : ");
	char Menu = _getch();
	switch (Menu) {
	case 'S':
	case 's':
		fwrite(&plus, sizeof(plus), 1, f);
		num++;
		fclose(f);
		system("cls");
		printTitle(pArr, pArr2, plus, num);
		break;
	case 'M':
	case 'm':
		fclose(f);
		system("cls");
		printTitle(pArr, pArr2, plus, num);
	case 'Q':
	case 'q':
		exit(0);
	default:
		break;
	}
	return;
}