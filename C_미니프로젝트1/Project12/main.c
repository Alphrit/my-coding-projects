#include "infor.h"

int main(void) {
    printf("===========================================================================");
    printf("\nMMS(Membership Management System) ���� 1�ܰ� Ver 0.9\n");
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
    printf("\nI) ȸ�����");
    printf("\nM) ȸ������ ����");
    printf("\nD) ȸ������ ����");
    printf("\nS) ȸ���˻�");
    printf("\nL) ȸ�����");
    printf("\nN) �ý����ʱ�ȭ");
    printf("\nX) �ڷ�����");
    printf("\nH) ����");
    printf("\nQ) ����");
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
    
    