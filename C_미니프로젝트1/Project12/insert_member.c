#include "infor.h"

void insert_member(infor* pArr, infor* pArr2, infor* plus, int num) {
	FILE* f = NULL;
	fopen_s(&f, "member.dat", "wb");
	if (f == NULL) {
		printf("���� ���� ����!");
		fclose(f);
		exit(0);
	}
	printf("ȸ���� �⺻ ������ �Է��Ͻʽÿ�...\n");

	printf("\n> �� ȣ : ");
	scanf_s("%d", &plus[num].Num, sizeof(plus[num].Num));


	printf("\n> ID : ");
	scanf_s("%s", &plus[num].ID, sizeof(plus[num].ID));

	printf("\n> ��й�ȣ : ");
	scanf_s("%s", &plus[num].Password, sizeof(plus[num].Password));

	printf("\n> �� �� : ");
	scanf_s("%s", &plus[num].Name, sizeof(plus[num].Name));

	printf("\n> �� �� : ");
	scanf_s("%s", &plus[num].Gender, sizeof(plus[num].Gender));

	printf("\n> �� �� : ");
	scanf_s("%s", plus[num].Age, sizeof(plus[num].Age));

	printf("\n> �� �� : ");
	scanf_s("%s", &plus[num].JobPosition, sizeof(plus[num].JobPosition));

	printf("\n> ȸ��� : ");
	scanf_s("%s", &plus[num].Conpany, sizeof(plus[num].Conpany));

	printf("\n> �� �� : ");
	scanf_s("%s", &plus[num].Address, sizeof(plus[num].Address));

	printf("\n> �����ȣ : ");
	scanf_s("%s", &plus[num].ZipCode, sizeof(plus[num].ZipCode));

	printf("\n> ��ȭ��ȣ : ");
	scanf_s("%s", &plus[num].TelephoneNum, sizeof(plus[num].TelephoneNum));

	printf("\n> �޴��� : ");
	scanf_s("%s", &plus[num].PhoneNum, sizeof(plus[num].PhoneNum));
	
	printf("S)����, M)����, Q)���� : ");
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