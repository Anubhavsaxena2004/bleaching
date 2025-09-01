public class main
{
    public static void transposeSquare(int[][] m)
    {
        for (int i = 0; i < m.length; i++)
        {
            for (int j = i + 1; j < m.length; j++)
            {
                int t = m[i][j];
                m[i][j] = m[j][i];
                m[j][i] = t;
            }
        }
    }
    public static void printMatrix(int[][] m)
        { for(int[] row : m)
            {
                for(int val : row)
                    System.out.print(val + " ");
                System.out.println();
            }
        }
    public static void main(String[] args)
    {
        int[][] matrix = {
                {1, 2, 3},
                {4, 5, 6},
                {7, 8, 9}
        };
        System.out.println("Original Matrix:");
        printMatrix(matrix);
        transposeSquare(matrix);
        System.out.println("\nTransposed Matrix:");
        printMatrix(matrix);
        
    }
}