#include "infor.h"

void modify_member(infor* pArr, infor* pArr2, infor* plus, int num) {
	FILE* fp = NULL;
	fopen_s(&fp, "member.dat", "rb");
	if (fp == NULL) {
		printf("���� ���� ����!");
		fclose(fp);
		exit(0);
	}

	fread(&pArr, sizeof(pArr), 1, fp);
	printf("�˻��� ����� ID�� �Է��Ͻÿ� : ");

	char id[10], ch;
	int index, op, n = 0;
	scanf_s("%s", &id, sizeof(id));
	for (index = 0; index < num; index++) {
		if (strcmp(id, pArr[index].ID) == 0) {
			printf("\n> �� ȣ     : ");
			printf("%d", pArr[index].Num);
			printf("\n> ȸ��ID    : ");
			printf("%s", pArr[index].ID);
			printf("\n1. ��й�ȣ : ");
			printf("%s", pArr[index].Password);
			printf("\n2. �� ��    : ");
			printf("%s", pArr[index].Name);
			printf("\n3. �� ��    : ");
			printf("%s", pArr[index].Gender);
			printf("\n4. �� ��    : ");
			printf("%s", pArr[index].Age);
			printf("\n5. �� ��    : ");
			printf("%s", pArr[index].JobPosition);
			printf("\n6. ȸ���   : ");
			printf("%s", pArr[index].Conpany);
			printf("\n7. �� ��    : ");
			printf("%s", pArr[index].Address);
			printf("\n8. �����ȣ : ");
			printf("%s", pArr[index].ZipCode);
			printf("\n9. ��ȭ��ȣ : ");
			printf("%s", pArr[index].TelephoneNum);
			printf("\n10. �޴���  : ");
			printf("%s", pArr[index].PhoneNum);
			printf("\n������ �׸��� �����ϼ��� : ");
			scanf_s("%d", &op, sizeof(op));

			FILE* pf = NULL;
			fopen_s(&pf, "member.dat", "wb");
			if (pf == NULL) {
				printf("���� ���� ����!");
				fclose(pf);
				exit(0);
			}

			printf("�����͸� �Է��ϼ��� : ");
			
			switch (op) {
			case 1:
				pArr[index].Password == NULL;
				scanf_s("%s", &pArr[index].Password, sizeof(pArr[index].Password));
				fwrite(&pArr[index].Password, sizeof(pArr[index].Password), 1, pf);
				break;
			case 2:
				pArr[index].Name == NULL;
				scanf_s("%s", &pArr[index].Name, sizeof(pArr[index].Name));
				fwrite(&pArr[index].Name, sizeof(pArr[index].Name), 1, pf);
				break;
			case 3:
				pArr[index].Gender == NULL;
				scanf_s("%s", &pArr[index].Gender, sizeof(pArr[index].Gender));
				fwrite(&pArr[index].Gender, sizeof(pArr[index].Gender), 1, pf);
				break;
			case 4:
				pArr[index].Age == NULL;
				scanf_s("%s", &pArr[index].Age, sizeof(pArr[index].Age));
				fwrite(&pArr[index].Age, sizeof(pArr[index].Age), 1, pf);
				break;
			case 5:
				pArr[index].JobPosition == NULL;
				scanf_s("%s", &pArr[index].JobPosition, sizeof(pArr[index].JobPosition));
				fwrite(&pArr[index].JobPosition, sizeof(pArr[index].JobPosition), 1, pf);
				break;
			case 6:
				pArr[index].Conpany == NULL;
				scanf_s("%s", &pArr[index].Conpany, sizeof(pArr[index].Conpany));
				fwrite(&pArr[index].Conpany, sizeof(pArr[index].Conpany), 1, pf);
				break;
			case 7:
				pArr[index].Address == NULL;
				scanf_s("%s", &pArr[index].Address, sizeof(pArr[index].Address));
				fwrite(&pArr[index].Address, sizeof(pArr[index].Address), 1, pf);
				break;
			case 8:
				pArr[index].ZipCode == NULL;
				scanf_s("%s", &pArr[index].ZipCode, sizeof(pArr[index].ZipCode));
				fwrite(&pArr[index].ZipCode, sizeof(pArr[index].ZipCode), 1, pf);
				break;
			case 9:
				pArr[index].TelephoneNum == NULL;
				scanf_s("%s", &pArr[index].TelephoneNum, sizeof(pArr[index].TelephoneNum));
				fwrite(&pArr[index].TelephoneNum, sizeof(pArr[index].TelephoneNum), 1, pf);
				break;
			case 10:
				pArr[index].PhoneNum == NULL;
				scanf_s("%s", &pArr[index].PhoneNum, sizeof(pArr[index].PhoneNum));
				fwrite(&pArr[index].PhoneNum, sizeof(pArr[index].PhoneNum), 1, pf);
				break;
			}
				n++;
				fclose(pf);
		}
	}
		if (!(n > 0)) {
			printf("����ڸ� ã�� �� �����ϴ�...");
		}
		fclose(fp);
		printf("M)����, Q)���� : ");
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