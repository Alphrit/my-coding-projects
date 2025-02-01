#include "infor.h"

void view_help(infor* pArr, infor* pArr2, infor* plus, int num) {
	printf("\n\n----------------- HELP MESSAGE -------------------------------");
	printf("\n프로그램을 처음 사용하실 때는 색인 파일(menber.idx)과");
	printf("\n데이터 파일(member.dat)이 존재하지 않습니다.");
	printf("\n따라서, 'N'을 눌러 시스템 초기화한 다음 사용하십시오.");
	printf("\n단, 데이터 파일이 존재할 경우에 이 작업을 하시면 기존의 데이터를");
	printf("\n잃어버리게 되므로 주의해야 합니다.");
	printf("\n저장 데이터가 많아지면 'X'를 눌러 자료를 정리하십시오.");
	printf("\n자료를 정리하시면 데이터 검색속도가 향상됩니다.\n");
	printTitle(pArr, pArr2, plus, num);
	return;
}