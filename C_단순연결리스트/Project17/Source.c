#include "header.h"

void Rank(Infor* tem) { //1-1 ����. ��� ����
    NODE* a = A;
    while (NULL != a) {
        if (tem->total < a->data.total) { //�߰��� ����� ����(tem->total)�� ���� ����� ����(a->data.total)���� �۴ٸ�
            tem->ranking++; //���� �߰��� ������ ����� ������Ŵ
        }
        else {             // ���� ����� ����(a->data.total)�� �߰��� ����(tem->total)���� �۴ٸ� 
            a->data.ranking++;// ���� ����� ����� ������Ŵ
        }
        a = a->link; // ���� ���� �̵�
    }
}

void AddNode(Infor* inf) {//1-1 ����.���� ��忡 ���ο� ��带 �߰�
    if (NULL != A) {
        (B)->link = (NODE*)malloc(sizeof(NODE));  // �߰��� ��忡 ��� �޸� �Ҵ�
        B = (B)->link;  // �߰��� ���� B�� �ű�
    }
    else {
        A = (NODE*)malloc(sizeof(NODE)); // ó���� �� ��� �޸� �Ҵ�
        B = A;  // ù ���⿡ �� �� �� ��带 ����Ŵ
    }
    memcpy(&(B)->data, inf, sizeof(Infor)); //�߰��� ��忡 �л� ���� ����
    (B)->link = NULL;// �߰��� ����� �� ����

}

void Input(Infor* inf) { //1-1.���� ������ �Է¹���
    char *END = "end";
    char end[10];
    while (1) {
        printf("\n �Է��� ��ġ���� end �� �Է��ϼ���");
        scanf_s("%s", end, sizeof(end));
        int com = strcmp(END, end); //end�� �Էµ� �迭�� ��
        if (com == 0) { //end�� �Էµ� �迭�� ���ٸ�
            break; //���� ȭ������ �Ѿ
        }
        printf("�й� : ");
        scanf_s("%d", &inf->id, sizeof(inf->id));
        printf("�̸� : ");
        scanf_s("%s", &inf->name, 10);
        printf("���� : ");
        scanf_s("%d", &inf->kor);
        printf("���� : ");
        scanf_s("%d", &inf->eng);
        printf("���� : ");
        scanf_s("%d", &inf->math);

        inf->ranking = 1; // �⺻ ��ŷ 1��(�ϳ� ������ ��)
        inf->total = inf->kor + inf->eng + inf->math; //����
        inf->average = inf->total / 3.0f; //���
        if (inf->total >= 270) {    
            inf->score = 'A';
        }
        else if (inf->total >= 240) {
            inf->score = 'B';
        }
        else if (inf->total >= 210) {
            inf->score = 'C';
        }
        else if (inf->total >= 180) {
            inf->score = 'D';
        }
        else if (inf->total >= 150) {
            inf->score = 'E';
        }
        else {
            inf->score = 'F';
        }                               //����
        Rank(inf); //��� ����
        AddNode(inf); // ���� �Է��� ������ ���� ����Ʈ�� �߰�
    }
    return;
}

void Delete() { //1-2.��� ��� ����, �޸� ���� ����
    NODE* a = A, * next;

    while (NULL != a) {    // ���� ������ ������ ������ �̵��ϵ��� �ݺ����� ����
        next = a->link;    // a->link��� a->link�� next�� ����(free�Լ� ��� �� ����� ã�� ���� a->link ����)
        free(a);   //a�� ����Ű�� ��� ��� ����
        a = next;    // ���� ��� �ּҷ� �̵�(free�Լ� ��� �� ����� ã�� ���� a->link ����)
    }
    A = B = NULL;
}

void IDsearch() {   //2-1. �Էµ� ���̵�� ���� ���̵� ã�� �� ����� ������ ǥ��
    NODE* a = A;
    int *idsearch;
    printf("\n\t�˻��� �л� �й��� �Է��ϼ��� : ");
    scanf_s("%d", &idsearch, sizeof(idsearch));
    printf("\n\t==============================================================\n");
    printf("\t �й�    �̸�     ����  ����  ����  ����   ���   ����   ���\n");
    printf("\t--------------------------------------------------------------\n");
    while (NULL != a) {
        if (idsearch == a->data.id) {
            printf("\t %03d %8s %7d   %3d   %3d   %3d    %3.2f   %3c   %1d��\n",
            a->data.id, a->data.name, a->data.kor, a->data.eng, a->data.math,
            a->data.total, a->data.average, a->data.score, a->data.ranking);  //���̵� ã�� �� ���� ǥ��. ������ ǥ��X
        }
        a = a->link;
    }
}
void NAMEsearch() { //2-2. �Էµ� �̸��� ���� �̸��� ã�� �� ����� ������ ǥ��
    NODE* a = A;
    int com = 0;
    char* namesearch[10];
    printf("\n\t�˻��� �л� �̸��� �Է��ϼ��� : ");
    scanf_s("%s", &namesearch, sizeof(namesearch));
    printf("\n\t==============================================================\n");
    printf("\t �й�    �̸�     ����  ����  ����  ����   ���   ����   ���\n");
    printf("\t--------------------------------------------------------------\n");
    while (NULL != a) {
        com = strcmp(namesearch, a->data.name);  //�Էµ� �̸��� �ش� ����� �̸��� ��
        if (com == 0) {
            printf("\t %03d %8s %7d   %3d   %3d   %3d    %3.2f   %3c   %1d��\n",
            a->data.id, a->data.name, a->data.kor, a->data.eng, a->data.math,
            a->data.total, a->data.average, a->data.score, a->data.ranking); //�̸��� ã�� �� ���� ǥ��. ������ ǥ��X
        }
        a = a->link;
    }
}

NODE* IDsort(NODE* node) {   //3-1. �й� �������� ������������ ����. IDsort ��ü�� ��尡 ��
    NODE* a1, * a2;
    a1 = node;

    while (a1->link != NULL) {
        if (a1->data.id > a1->link->data.id)   //���� �й��� ���� �й����� ũ�ٸ�
        {
            a2 = a1->link; // ������ �Űܾ��� ��带 ����
            a1->link = a1->link->link; // a2 ���� ����
            a2->link = node; // a2�� link�� ���� ù �ڸ��� ����Ŵ
            node = a1 = a2; // a1�� node ��� temp�� �ʱ�ȭ ������ �� ��� ���� ù�ڸ��� ��
            printf("\n");
            continue; // ���� ù �ڸ��� �� a1�� ���� a1 = a1->link�� ���ؼ� ������ ���� ���ϵ��� ����
        }
        a1 = a1->link;  //���� ���� �̵�
    }
    return node;
}

NODE* NAMEsort(NODE* node) {   //3-2. �̸� �������� ������������ ����. NAMEsort ��ü�� ��尡 ��. IDsort�� ���� ����
    NODE* a1, * a2;
    a1 = node;
    int com;

    while (a1->link != NULL) {
        com = strcmp(a1->data.name, a1->link->data.name); //���� ����� �̸�(a1->data.name)�� ���� ����� �̸�(a1->link->data.name) ��
        if (com > 0)
        {
            a2 = a1->link;
            a1->link = a1->link->link;
            a2->link = node;
            node = a1 = a2;
            printf("\n");
            continue;
        }
        a1 = a1->link;
    }
    return node;
}

NODE* SCOREsort(NODE* node) {    //3-3. ���� �������� ������������ ����. NAMEsort ��ü�� ��尡 ��. IDsort, NAMEsort�� ���� ����
    NODE* a1, * a2;
    a1 = node;

    while (a1->link != NULL) {
        if (a1->data.total < a1->link->data.total)
        {
            a2 = a1->link;
            a1->link = a1->link->link;
            a2->link = node;
            node = a1 = a2;
            printf("\n");
            continue;
        }
        a1 = a1->link;
    }
    return node;
}

void Output() { //4. ��� ���� ���
    NODE* a = A;

    printf("\n\t==============================================================\n");
    printf("\t �й�    �̸�     ����  ����  ����  ����   ���   ����   ���\n");
    printf("\t--------------------------------------------------------------\n");
    while (NULL != a) {
        printf("\t %03d %8s %7d   %3d   %3d   %3d    %3.2f   %3c   %1d��\n",
            a->data.id, a->data.name, a->data.kor, a->data.eng, a->data.math,
            a->data.total, a->data.average, a->data.score, a->data.ranking);

        a = a->link;
    }
}

int main()
{
    int num, count = 0;

    while (1) {
        system("cls");
        printf("\t====================================================\n");
        printf("\t\t�л� ���� ���� : �ܼ� ���� ����Ʈ\n");
        printf("\t====================================================\n");
        printf("\n\t 1. �л� ���� ����(���, ����)");
        printf("\n\t 2. ��          ��(�й�, �̸�)");
        printf("\n\t 3. ��          ��(�й���, �̸���, ������)");
        printf("\n\t 4. ��ü �л� ���\n");
        printf("\n\t 5. ���α׷� ����\n\n");
        printf("\t---------------------------------------------------\n");
        printf("\n\t ������ ��ȣ��? ");

        scanf_s("%d", &num);
        char *Y = "Y";
        char y[10];

        switch (num) {
        case 1:
            printf("\n\t\t�� �л� ���� ���� ��\n");
            printf("\n\t\t 1.�л� ���� ���");
            printf("\n\t\t 2.�л� ���� ����");
            printf("\n\n\t     ���ϴ� ��ȣ�� �����ϼ��� : ");
            scanf_s("%d", &num);
            switch (num) {
            case 1:
                Input(&temp); // ������ �Է� ����
                system("pause");
                break;
            case 2:
                printf("\t���� �����Ͻðڽ��ϱ�? �����Ͻñ� ���Ͻø� Y�� �����ּ���.");
                scanf_s("%s",y, sizeof(y));
                int com1 = strcmp(Y, y);
                if (com1 == 0) {
                    Delete(); //��� ���� ����
                    printf("\n\t������ �����߽��ϴ�.\n");
                    system("pause");
                    break;
                }
                else {
                    printf("\n\t������ ����߽��ϴ�.\n"); //�ٸ� ��ư�� ���� �� ���� ���
                    system("pause");
                    break;
                }
            default:
                printf("\n\t�ٽ� �Է����ּ���.\n");
                system("pause");
                break;
            }
            break;
        case 2:
            printf("\n\t\t�� �л� ���� ���� ��\n");
            printf("\n\t\t 1. �й����� �˻�");
            printf("\n\t\t 2. �̸����� �˻�");
            printf("\n\n\t\t 0. �˻� ����");
            printf("\n\n\t     ���ϴ� ��ȣ�� �����ϼ��� : ");
            scanf_s("%d", &num);
            switch (num) {
            case 1:
                IDsearch(); //ID�� �˻�
                system("pause");
                break;
            case 2:
                NAMEsearch(); //�̸����� �˻�
                system("pause");
                break;
            case 0:
                printf("\n\t�˻��� �����ϰ� ���� ȭ������ ���ư��ϴ�.\n");
                system("pause");
                break;
            default:
                printf("\n�ٽ� �Է����ּ���.");
                system("pause");
                break;
            }
            break;
        case 3:
            printf("\n\t\t�� ���� ��� ��\n");
            printf("\n\t\t 1. �й������� ����");
            printf("\n\t\t 2. �̸������� ����");
            printf("\n\t\t 3. ���������� ����");
            printf("\n\n\t     ���ϴ� ��ȣ�� �����ϼ��� : ");
            scanf_s("%d", &num);
            switch (num) {
            case 1:
                A = IDsort(A); //ID �������� ������������ A�� ������
                printf("\n������ �Ϸ�Ǿ����ϴ�.\n");
                system("pause");
                break;
            case 2:
                A = NAMEsort(A);//�̸� �������� ������������ A�� ������
                printf("\n������ �Ϸ�Ǿ����ϴ�.\n");
                system("pause");
                break;
            case 3:
                A = SCOREsort(A); //���� �������� ������������ A�� ������
                printf("\n������ �Ϸ�Ǿ����ϴ�.\n");
                system("pause");
                break;
            default:
                printf("\n�ٽ� �Է����ּ���.");
                system("pause");
                break;
            }
            break;
        case 4:
            Output(A); // �� ��忡 ����� ���� ������ ���
            system("pause");
            break;
        case 5:
            printf("\n���α׷��� �����մϴ�.");
            exit(100);
        default:
            printf("\n�ٽ� �Է����ּ���.");
            system("pause");
            break;
        }
    }
        return 0;
}