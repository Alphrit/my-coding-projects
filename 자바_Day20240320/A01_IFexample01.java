package Day20240320;

import java.util.Scanner;

/** 예제내용: 단독(단순) IF
 *  코드: 특정조건에서 조건이 참인 결과면 수행, 거짓이면 패스 
 */

public class A01_IFexample01 {
	public static void main(String[] args) {
		Scanner scan = new Scanner(System.in);
		int flag = 0;
		
		System.out.print("flag(1 이하면 0으로 처리함: ");
		flag = scan.nextInt();
		
		if (flag <= 0) {
			flag = 0;
		}
		
		System.out.println("이후 코드 진행.....");
		System.out.println("flag: "+flag);
		scan.close();
	}
}
