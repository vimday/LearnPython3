
import java.util.LinkedList;

public class cardMove {
    public static LinkedList<Integer> findOriginOrder(int[] cur) {
        int sz = cur.length;
        LinkedList<Integer> res = new LinkedList<>();
        for (int i = sz - 1; i >= 0; i--) {
            if (!res.isEmpty()) {
                res.addFirst(res.pollLast());
            }
            res.addFirst(cur[i]);
        }
        return res;
    }

    public static void main(String[] args) {
        System.out.println(cardMove.findOriginOrder(new int[] { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13 }));
    }
}