package Day20240320;

import java.util.Scanner;

/**	중첩(nested) if 문
 */
public class A06_IFexample06 {
	public static void main(String[] args) {
		Scanner scan = new Scanner(System.in);
		System.out.print("1(+,-) 또는 0(*,/) 입력: ");
		int n = scan.nextInt();
		if(n == 1) {
			System.out.print("+, -: ");
			char op = scan.next().charAt(0);
			if (op =='+') {
				System.out.println("더하기 연산 문장");
			}
			else if (op == '-' ) {
				System.out.println("빼기 연산 문장");
			}
		}
		else if(n == 0) {
			System.out.print("*, /: ");
			char op = scan.next().charAt(0);
			if (op =='*') {
				System.out.println("곱하기 연산 문장");
			}
			else if (op == '/' ) {
				System.out.println("나누기 연산 문장");
			}
		}
		else {
			System.out.println("없는 번호입니다.");
		}
		scan.close();
	}
}
