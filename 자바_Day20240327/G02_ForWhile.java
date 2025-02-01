package Day20240327;

public class G02_ForWhile {
	public static void main(String[] args) {
		for(int n = 1; n<=100; n++) {
			System.out.print("*");
			
			if(n == 50) {

				System.out.println();
				System.out.println("별이 50개에 달하여 반복이 종료됨");
				break;
			}
		}
		int res = 2 * 100;
		System.out.println(res);
	}
}
