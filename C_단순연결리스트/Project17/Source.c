#include "header.h"

void Rank(Infor* tem) { //1-1 과정. 등수 갱신
    NODE* a = A;
    while (NULL != a) {
        if (tem->total < a->data.total) { //추가될 노드의 총점(tem->total)이 현재 노드의 총점(a->data.total)보다 작다면
            tem->ranking++; //새로 추가될 점수의 등수를 증가시킴
        }
        else {             // 현재 노드의 총점(a->data.total)이 추가될 총점(tem->total)보다 작다면 
            a->data.ranking++;// 현재 노드의 등수를 증가시킴
        }
        a = a->link; // 다음 노드로 이동
    }
}

void AddNode(Infor* inf) {//1-1 과정.기존 노드에 새로운 노드를 추가
    if (NULL != A) {
        (B)->link = (NODE*)malloc(sizeof(NODE));  // 추가된 노드에 노드 메모리 할당
        B = (B)->link;  // 추가된 노드로 B를 옮긺
    }
    else {
        A = (NODE*)malloc(sizeof(NODE)); // 처음에 새 노드 메모리 할당
        B = A;  // 첫 노드기에 둘 다 새 노드를 가리킴
    }
    memcpy(&(B)->data, inf, sizeof(Infor)); //추가된 노드에 학생 정보 저장
    (B)->link = NULL;// 추가된 노드의 끝 정함

}

void Input(Infor* inf) { //1-1.각종 정보를 입력받음
    char *END = "end";
    char end[10];
    while (1) {
        printf("\n 입력을 마치려면 end 를 입력하세요");
        scanf_s("%s", end, sizeof(end));
        int com = strcmp(END, end); //end와 입력될 배열과 비교
        if (com == 0) { //end와 입력될 배열이 같다면
            break; //메인 화면으로 넘어감
        }
        printf("학번 : ");
        scanf_s("%d", &inf->id, sizeof(inf->id));
        printf("이름 : ");
        scanf_s("%s", &inf->name, 10);
        printf("국어 : ");
        scanf_s("%d", &inf->kor);
        printf("영어 : ");
        scanf_s("%d", &inf->eng);
        printf("수학 : ");
        scanf_s("%d", &inf->math);

        inf->ranking = 1; // 기본 랭킹 1등(하나 적었을 때)
        inf->total = inf->kor + inf->eng + inf->math; //총점
        inf->average = inf->total / 3.0f; //평균
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
        }                               //학점
        Rank(inf); //등수 갱신
        AddNode(inf); // 새로 입력한 성적을 연결 리스트에 추가
    }
    return;
}

void Delete() { //1-2.모든 노드 삭제, 메모리 또한 해제
    NODE* a = A, * next;

    while (NULL != a) {    // 시작 노드부터 마지막 노드까지 이동하도록 반복문을 구성
        next = a->link;    // a->link대신 a->link를 next에 저장(free함수 사용 시 대상을 찾지 못해 a->link 오류)
        free(a);   //a가 가리키는 모든 노드 삭제
        a = next;    // 다음 노드 주소로 이동(free함수 사용 시 대상을 찾지 못해 a->link 오류)
    }
    A = B = NULL;
}

void IDsearch() {   //2-1. 입력된 아이디와 같은 아이디를 찾아 그 노드의 정보를 표시
    NODE* a = A;
    int *idsearch;
    printf("\n\t검색할 학생 학번을 입력하세요 : ");
    scanf_s("%d", &idsearch, sizeof(idsearch));
    printf("\n\t==============================================================\n");
    printf("\t 학번    이름     국어  영어  수학  총점   평균   학점   등수\n");
    printf("\t--------------------------------------------------------------\n");
    while (NULL != a) {
        if (idsearch == a->data.id) {
            printf("\t %03d %8s %7d   %3d   %3d   %3d    %3.2f   %3c   %1d등\n",
            a->data.id, a->data.name, a->data.kor, a->data.eng, a->data.math,
            a->data.total, a->data.average, a->data.score, a->data.ranking);  //아이디를 찾을 시 정보 표시. 없으면 표시X
        }
        a = a->link;
    }
}
void NAMEsearch() { //2-2. 입력된 이름과 같은 이름을 찾아 그 노드의 정보를 표시
    NODE* a = A;
    int com = 0;
    char* namesearch[10];
    printf("\n\t검색할 학생 이름을 입력하세요 : ");
    scanf_s("%s", &namesearch, sizeof(namesearch));
    printf("\n\t==============================================================\n");
    printf("\t 학번    이름     국어  영어  수학  총점   평균   학점   등수\n");
    printf("\t--------------------------------------------------------------\n");
    while (NULL != a) {
        com = strcmp(namesearch, a->data.name);  //입력된 이름과 해당 노드의 이름을 비교
        if (com == 0) {
            printf("\t %03d %8s %7d   %3d   %3d   %3d    %3.2f   %3c   %1d등\n",
            a->data.id, a->data.name, a->data.kor, a->data.eng, a->data.math,
            a->data.total, a->data.average, a->data.score, a->data.ranking); //이름을 찾을 시 정보 표시. 없으면 표시X
        }
        a = a->link;
    }
}

NODE* IDsort(NODE* node) {   //3-1. 학번 기준으로 오름차순으로 정렬. IDsort 자체가 노드가 됨
    NODE* a1, * a2;
    a1 = node;

    while (a1->link != NULL) {
        if (a1->data.id > a1->link->data.id)   //현재 학번이 다음 학번보다 크다면
        {
            a2 = a1->link; // 앞으로 옮겨야할 노드를 저장
            a1->link = a1->link->link; // a2 제외 연결
            a2->link = node; // a2의 link는 가장 첫 자리를 가리킴
            node = a1 = a2; // a1와 node 모두 temp로 초기화 함으로 써 모두 가장 첫자리로 감
            printf("\n");
            continue; // 가장 첫 자리로 간 a1이 밑의 a1 = a1->link로 인해서 앞으로 가지 못하도록 막음
        }
        a1 = a1->link;  //다음 노드로 이동
    }
    return node;
}

NODE* NAMEsort(NODE* node) {   //3-2. 이름 기준으로 오름차순으로 정렬. NAMEsort 자체가 노드가 됨. IDsort와 원리 동일
    NODE* a1, * a2;
    a1 = node;
    int com;

    while (a1->link != NULL) {
        com = strcmp(a1->data.name, a1->link->data.name); //현재 노드의 이름(a1->data.name)과 다음 노드의 이름(a1->link->data.name) 비교
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

NODE* SCOREsort(NODE* node) {    //3-3. 점수 기준으로 내림차순으로 정렬. NAMEsort 자체가 노드가 됨. IDsort, NAMEsort와 원리 동일
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

void Output() { //4. 모든 정보 출력
    NODE* a = A;

    printf("\n\t==============================================================\n");
    printf("\t 학번    이름     국어  영어  수학  총점   평균   학점   등수\n");
    printf("\t--------------------------------------------------------------\n");
    while (NULL != a) {
        printf("\t %03d %8s %7d   %3d   %3d   %3d    %3.2f   %3c   %1d등\n",
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
        printf("\t\t학생 정보 관리 : 단순 연결 리스트\n");
        printf("\t====================================================\n");
        printf("\n\t 1. 학생 정보 관리(등록, 삭제)");
        printf("\n\t 2. 검          색(학번, 이름)");
        printf("\n\t 3. 정          렬(학번순, 이름순, 성적순)");
        printf("\n\t 4. 전체 학생 출력\n");
        printf("\n\t 5. 프로그램 종료\n\n");
        printf("\t---------------------------------------------------\n");
        printf("\n\t 선택할 번호는? ");

        scanf_s("%d", &num);
        char *Y = "Y";
        char y[10];

        switch (num) {
        case 1:
            printf("\n\t\t▶ 학생 정보 관리 ◀\n");
            printf("\n\t\t 1.학생 성적 등록");
            printf("\n\t\t 2.학생 성적 삭제");
            printf("\n\n\t     원하는 번호를 선택하세요 : ");
            scanf_s("%d", &num);
            switch (num) {
            case 1:
                Input(&temp); // 성적을 입력 받음
                system("pause");
                break;
            case 2:
                printf("\t정말 삭제하시겠습니까? 삭제하시길 원하시면 Y를 눌러주세요.");
                scanf_s("%s",y, sizeof(y));
                int com1 = strcmp(Y, y);
                if (com1 == 0) {
                    Delete(); //모든 정보 삭제
                    printf("\n\t정보를 삭제했습니다.\n");
                    system("pause");
                    break;
                }
                else {
                    printf("\n\t삭제를 취소했습니다.\n"); //다른 버튼을 누를 시 삭제 취소
                    system("pause");
                    break;
                }
            default:
                printf("\n\t다시 입력해주세요.\n");
                system("pause");
                break;
            }
            break;
        case 2:
            printf("\n\t\t▶ 학생 정보 관리 ◀\n");
            printf("\n\t\t 1. 학번으로 검색");
            printf("\n\t\t 2. 이름으로 검색");
            printf("\n\n\t\t 0. 검색 종료");
            printf("\n\n\t     원하는 번호를 선택하세요 : ");
            scanf_s("%d", &num);
            switch (num) {
            case 1:
                IDsearch(); //ID로 검색
                system("pause");
                break;
            case 2:
                NAMEsearch(); //이름으로 검색
                system("pause");
                break;
            case 0:
                printf("\n\t검색을 종료하고 메인 화면으로 돌아갑니다.\n");
                system("pause");
                break;
            default:
                printf("\n다시 입력해주세요.");
                system("pause");
                break;
            }
            break;
        case 3:
            printf("\n\t\t▶ 정렬 출력 ◀\n");
            printf("\n\t\t 1. 학번순으로 정렬");
            printf("\n\t\t 2. 이름순으로 정렬");
            printf("\n\t\t 3. 성적순으로 정렬");
            printf("\n\n\t     원하는 번호를 선택하세요 : ");
            scanf_s("%d", &num);
            switch (num) {
            case 1:
                A = IDsort(A); //ID 기준으로 오름차순으로 A를 재정렬
                printf("\n정렬이 완료되었습니다.\n");
                system("pause");
                break;
            case 2:
                A = NAMEsort(A);//이름 기준으로 오름차순으로 A를 재정렬
                printf("\n정렬이 완료되었습니다.\n");
                system("pause");
                break;
            case 3:
                A = SCOREsort(A); //점수 기준으로 내림차순으로 A를 재정렬
                printf("\n정렬이 완료되었습니다.\n");
                system("pause");
                break;
            default:
                printf("\n다시 입력해주세요.");
                system("pause");
                break;
            }
            break;
        case 4:
            Output(A); // 각 노드에 저장된 성적 정보를 출력
            system("pause");
            break;
        case 5:
            printf("\n프로그램을 종료합니다.");
            exit(100);
        default:
            printf("\n다시 입력해주세요.");
            system("pause");
            break;
        }
    }
        return 0;
}