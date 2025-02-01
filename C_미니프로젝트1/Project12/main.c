#include "infor.h"

int main(void) {
    printf("===========================================================================");
    printf("\nMMS(Membership Management System) 개발 1단계 Ver 0.9\n");
    printf("===========================================================================\n");
    struct INFOR arr[20], plus[2], arr2[20];
    memset(&arr, 0, sizeof(arr));
    memset(&plus, 0, sizeof(plus));
    memset(&arr2, 0, sizeof(arr2));
    int num = 0;
    printTitle(arr, arr2, plus, num);
    return 0;
}
void printTitle(infor* pArr, infor* pArr2, infor* plus, int num) {
    printf("\nI) 회원등록");
    printf("\nM) 회원정보 수정");
    printf("\nD) 회원정보 삭제");
    printf("\nS) 회원검색");
    printf("\nL) 회원목록");
    printf("\nN) 시스템초기화");
    printf("\nX) 자료정리");
    printf("\nH) 도움말");
    printf("\nQ) 종료");
    char Menu = _getch();
    switch (Menu) {
    case 'I':
    case 'i':
        system("cls");
        insert_member(&pArr, &pArr2, &plus, num);
        break;
    case 'M':
    case 'm':
        system("cls");
        modify_member(&pArr, &pArr2, &plus, num);
        break;
    case 'S':
    case 's':
        system("cls");
        search_member(pArr, pArr2, plus, num);
        break;
    case 'L':
    case 'l':
        system("cls");
        list_member(pArr, pArr2, plus, num);
        break;
    case 'H':
    case 'h':
        view_help(pArr, pArr2, plus, num);
        break;
    case 'Q':
    case 'q':
        exit(0);
    default:
        break;
    }

    return;
}
    
    