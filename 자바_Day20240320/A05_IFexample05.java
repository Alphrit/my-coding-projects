package Day20240320;
import java.util.Scanner;

public class A05_IFexample05 {
	public static void main(String[] args) {
		Scanner scan = new Scanner(System.in);
		int Score = 0;
		System.out.print("점수를 입력하십시오: ");
		Score = scan.nextInt();
		
		if(Score <=100 && Score >= 95) {
			System.out.println("당신의 학점은 A+입니다. 매우 우수하군요!");
		}
		else if (Score <= 94 && Score >= 90) {
			System.out.println("당신의 학점은 A0입니다. 우수하군요!");
		}
		else if (Score <= 89 && Score >= 85) {
			System.out.println("당신의 학점은 B+입니다. 수고하셨습니다.");
		}
		else if (Score <= 84 && Score >= 80) {
			System.out.println("당신의 학점은 B0입니다. 평범하군요.");
		}
		else if (Score <= 79 && Score >= 75) {
			System.out.println("당신의 학점은 C+입니다. 분발하세요!");
		}
		else if (Score <= 74 && Score >= 70) {
			System.out.println("당신의 학점은 C0입니다. 분발하세요!");
		}
		else if (Score <= 69 && Score >= 65) {
			System.out.println("당신의 학점은 D+입니다. 분발하세요!");

		}
		else if (Score <= 64 && Score >= 60) {
			System.out.println("당신의 학점은 D0입니다. 분발하세요!");
		}
		else {
			System.out.println("당신의 학점은 F!");
		}
		scan.close();
	}
}
