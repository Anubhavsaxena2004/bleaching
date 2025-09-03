import java.util.Scanner;
public class main {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
        Scanner sc = new Scanner(System.in);
        System.out.print("Enter your number: ");
        int num = sc.nextInt();
        for(int i=1; i<=10; i++){
            System.out.println(num + " x " + i + " = " + (num*i));
        }
    }
}



import java.util.Scanner;
public class main {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
        Scanner sc = new Scanner(System.in);
        int num = sc.nextInt();
       sum = 0;
       while(num>0){
           sum += num%10;
           num = num/10;
       }
       System.out.println(sum);
    }
}