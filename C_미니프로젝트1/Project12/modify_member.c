#include "infor.h"

void modify_member(infor* pArr, infor* pArr2, infor* plus, int num) {
	FILE* fp = NULL;
	fopen_s(&fp, "member.dat", "rb");
	if (fp == NULL) {
		printf("파일 개방 실패!");
		fclose(fp);
		exit(0);
	}

	fread(&pArr, sizeof(pArr), 1, fp);
	printf("검색할 사용자 ID를 입력하시오 : ");

	char id[10], ch;
	int index, op, n = 0;
	scanf_s("%s", &id, sizeof(id));
	for (index = 0; index < num; index++) {
		if (strcmp(id, pArr[index].ID) == 0) {
			printf("\n> 번 호     : ");
			printf("%d", pArr[index].Num);
			printf("\n> 회원ID    : ");
			printf("%s", pArr[index].ID);
			printf("\n1. 비밀번호 : ");
			printf("%s", pArr[index].Password);
			printf("\n2. 이 름    : ");
			printf("%s", pArr[index].Name);
			printf("\n3. 성 별    : ");
			printf("%s", pArr[index].Gender);
			printf("\n4. 나 이    : ");
			printf("%s", pArr[index].Age);
			printf("\n5. 직 위    : ");
			printf("%s", pArr[index].JobPosition);
			printf("\n6. 회사명   : ");
			printf("%s", pArr[index].Conpany);
			printf("\n7. 주 소    : ");
			printf("%s", pArr[index].Address);
			printf("\n8. 우편번호 : ");
			printf("%s", pArr[index].ZipCode);
			printf("\n9. 전화번호 : ");
			printf("%s", pArr[index].TelephoneNum);
			printf("\n10. 휴대폰  : ");
			printf("%s", pArr[index].PhoneNum);
			printf("\n수정할 항목을 선택하세요 : ");
			scanf_s("%d", &op, sizeof(op));

			FILE* pf = NULL;
			fopen_s(&pf, "member.dat", "wb");
			if (pf == NULL) {
				printf("파일 개방 실패!");
				fclose(pf);
				exit(0);
			}

			printf("데이터를 입력하세요 : ");
			
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
			printf("사용자를 찾을 수 없습니다...");
		}
		fclose(fp);
		printf("M)메인, Q)종료 : ");
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