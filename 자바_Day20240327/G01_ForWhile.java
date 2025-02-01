package Day20240327;
import java.util.Scanner;

public class G01_ForWhile {
	public static void main(String[] args) {
		// 무한반복: 특정 코드가 계속 실행상태(종료 조건이 있어야 함)
		Scanner scan = new Scanner(System.in);
		int total = 0;
		
		//while(true) {
		for(;;) {
			System.out.print("계속 더할 수(0을 입력할 시 종료): ");
			int number = scan.nextInt();
			if (number == 0) {
				break;
			}
			total = total + number;
		}
		scan.close();
		System.out.println("최종 합계: "+ total);
	}
}
