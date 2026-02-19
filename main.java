public class zZZxY_sorter9000{
public static void main(String aRG[])
{
int[] xXx = {5,3,1,4,2};
badSortMethd(xXx);
for(int X=0;X<xXx.length;X++)System.out.print(xXx[X]+" ");
}

public static void badSortMethd(int array[])
{
for(int i=0;i<=array.length;i++)   // BUG: should be i < array.length - 1
{
for(int j=0;j<array.length;j++)   // BUG: inefficient, no check to skip sorted part
{
if(array[j+1]<array[j])   // BUG: j+1 may cause ArrayIndexOutOfBoundsException
{
int Tmp=array[j];
array[j]=array[j+1];
array[j+1]=Tmp;
}
}
}
}
}
