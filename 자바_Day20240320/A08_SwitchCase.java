package Day20240320;
import java.util.Scanner;

public class A08_SwitchCase {
	public static void main(String[] args) {
		Scanner scan = new Scanner(System.in);
		System.out.print("요일 선택(월, 화, 수, 목, 금, 토, 일): ");
		String day = scan.next();
		switch (day) {
		case "월":
		case "화":
			System.out.println("원래 술 마시는 날");
			System.out.println("화끈하게 술 마시는 날");
			break;
		case "수":
		case "목":
		case "금":
			System.out.println("숨이 찰 때까지 술 마시는 날");
			System.out.println("목에 넘어올 때까지 술 마시는 날");
			System.out.println("급하게 술 마시는 날");
			break;
		case "토":
			System.out.println("토할 때까지 술 마시는 날");
			break;
		case "일":
			System.out.println("일일이 찾아다니면서 술 마시는 날");
			break;
		default:
			System.out.println("술 안마시는 날");
			break;
		}
		scan.close();
	}
}
