package Day20240320;

import java.util.Scanner;

public class A02_IFexample02 {
	public static void main(String[] args) {
		Scanner scan = new Scanner(System.in);
		int total = 0; //초기화
		System.out.print("입력할 성적점수(0 미만 또는 100 초과일 시 0으로 처리): ");
		total = scan.nextInt();
		
		if (total < 0 || total > 100) {
			total = 0;
		}
		System.out.println("당신이 입력한 점수는 "+total+"점입니다.");
		scan.close();
	
	}
	
}
