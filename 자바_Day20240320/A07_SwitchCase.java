package Day20240320;

import java.util.Scanner;

public class A07_SwitchCase {
	public static void main(String[] args) {
		Scanner scan = new Scanner(System.in);
		System.out.print("메뉴 선택(1, 2, 3, 4): ");
		int choice = scan.nextInt();
		
		switch (choice) {
		case 1:
			System.out.println("순대국입니다.");
			break;
		case 2:
			System.out.println("탕후루입니다.");
			break;
		case 3:
			System.out.println("돈까스입니다.");
			break;
		case 4:
			System.out.println("중국집입니다.");
			break;
		default:
			System.out.println("없는 메뉴입니다.");
			break;
		}
		scan.close();
	}
}
