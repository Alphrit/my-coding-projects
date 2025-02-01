package Day20240327;
public class G03__ForWhile {
	public static void main(String[] args) {
		for(int i = 1; i <= 100; i++) {
			
			if (i%3 == 0) {
				System.out.print(i + " ");
				continue; //아래 코드를 진행하지 않고, 다시 반복하러 올라감
			}
		}
		System.out.println();
		for(int a = 1; a<=100; a++) {
			if(a==3||a==6||a==9) {
				continue;
			}
			System.out.println(a);
		}
	}
}
