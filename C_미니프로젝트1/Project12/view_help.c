#include "infor.h"

void view_help(infor* pArr, infor* pArr2, infor* plus, int num) {
	printf("\n\n----------------- HELP MESSAGE -------------------------------");
	printf("\n���α׷��� ó�� ����Ͻ� ���� ���� ����(menber.idx)��");
	printf("\n������ ����(member.dat)�� �������� �ʽ��ϴ�.");
	printf("\n����, 'N'�� ���� �ý��� �ʱ�ȭ�� ���� ����Ͻʽÿ�.");
	printf("\n��, ������ ������ ������ ��쿡 �� �۾��� �Ͻø� ������ �����͸�");
	printf("\n�Ҿ������ �ǹǷ� �����ؾ� �մϴ�.");
	printf("\n���� �����Ͱ� �������� 'X'�� ���� �ڷḦ �����Ͻʽÿ�.");
	printf("\n�ڷḦ �����Ͻø� ������ �˻��ӵ��� ���˴ϴ�.\n");
	printTitle(pArr, pArr2, plus, num);
	return;
}