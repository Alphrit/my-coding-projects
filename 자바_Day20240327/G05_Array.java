package Day20240327;
public class G05_Array {
	public static void main(String[] args) {
		int[] aryNum = new int[1000];
		for (int i = 0; i < aryNum.length; i++) {
			aryNum[i] = i+1; //1000개의 변수공간에 (배열) 1~1000까지 초기화 코드
		}
		int sum = 0;
		for (int i = 0; i < aryNum.length; i++) {
			sum += aryNum[i];
		}
		System.out.println(sum);
		System.out.println(aryNum.length);
	}
}
