package Day20240320;

import java.util.Scanner;

public class A04_IFexample04 {
	public static void main(String[] args) {
		int max = 0;
		Scanner scan = new Scanner(System.in);
		System.out.print("숫자를 입력하십시오: ");
		max = scan.nextInt();
		
		if(max == 100) {
			System.out.println(max+" == "+100);
		}
		else if(max > 100) {
			System.out.println(max+" > "+100);
		}
		
		else if (max < 100) {
			System.out.println(max+" < "+100);
		}
		
		/*else {
			System.out.println("오류? 오류?");
		}*/
		scan.close();
	}
}
