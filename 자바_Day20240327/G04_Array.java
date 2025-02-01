package Day20240327;

public class G04_Array {  //자바에서 배열은 객체보임...
	public static void main(String[] args) {
		int[] pAge = new int[500];
		//배여로가 for 문을 같이 쓰면 i 값은 index 를 지칭.
		
		
		for(int i=0; i<500; i++) {
			pAge[i] = i+1;
		}
		
		for(int i=0; i<=500; i++) {
			System.out.println("pAge[" + i+ "] = "+pAge[i]);
		}
		
	}
}
