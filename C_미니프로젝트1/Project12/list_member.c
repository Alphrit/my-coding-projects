#include "infor.h"

void list_member(infor* pArr, infor* pArr2, infor* plus, int num) {
	FILE* fp = NULL;
	fopen_s(&fp, "member.dat", "rb");
	if (fp == NULL) {
		printf("���� ���� ����!");
		fclose(fp);
		exit(0);
	}

	fread(&pArr, sizeof(pArr), 1, fp);
	for (int i = 0; i < num; i++) {
		printf("\n> �� ȣ     : ");
		printf("%d", pArr[i].Num);
		printf("\n> ȸ��ID    : ");
		printf("%s", pArr[i].ID);
		printf("\n1. ��й�ȣ : ");
		printf("%s", pArr[i].Password);
		printf("\n2. �� ��    : ");
		printf("%s", pArr[i].Name);
		printf("\n3. �� ��    : ");
		printf("%s", pArr[i].Gender);
		printf("\n4. �� ��    : ");
		printf("%s", pArr[i].Age);
		printf("\n5. �� ��    : ");
		printf("%s", pArr[i].JobPosition);
		printf("\n6. ȸ���   : ");
		printf("%s", pArr[i].Conpany);
		printf("\n7. �� ��    : ");
		printf("%s", pArr[i].Address);
		printf("\n8. �����ȣ : ");
		printf("%s", pArr[i].ZipCode);
		printf("\n9. ��ȭ��ȣ : ");
		printf("%s", pArr[i].TelephoneNum);
		printf("\n10. �޴���  : ");
		printf("%s\n", pArr[i].PhoneNum);
	}
	printf("\nM)����, Q)���� : ");
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
	return;
}