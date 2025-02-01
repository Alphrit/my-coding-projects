package Day20240327;
public class G06_Array {
	public static void main(String[] args) {
		double[] dp = {1.1, 2.5, 3.3, 4.2, 4.5};
		
		System.out.println("배열 개수: "+dp.length);
		double avg = 0, sum = 0;
		for (int i = 0; i < dp.length; i++) {
			System.out.print(dp[i]+ " ");
			
			sum += dp[i];
		}
		System.out.println(" ");
		System.out.println("배열의 총합:"+sum);
		avg = sum/dp.length;
		System.out.println("배열의 평균:"+avg);
	}
}
