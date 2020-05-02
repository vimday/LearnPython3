public class Zhengxushu {

    // 就是一个数组，里面的数比前面的都大叫正序数，问随机删除一个数，最大可以有多少个正序数 "
    // O(n)算法可行。从左往右遍历，维护前面两个最大的元素。 要删除的元素肯定是删掉之后，
    // 后面有原本不是正序数的变成了正序数。 那我们遍历过程中，就记录这个信息。记录哪些元素是可能被删除的。
    // 用一个map<Integer, Integer>来记录，key就是要被删除的元素，value是删除这个key之后后面变成正序数的个数。
    // 同时，用一个Set<Integer>来记录不删除的情况下，正序数的索引列表。
    // 后面在遍历一遍数组，那上面的set和map求最大值就可以了

    private static void updateTwoMax(int[] arr, int num) {
        if (num > arr[0]) {
            int oldMax = arr[0];
            arr[0] = num;
            arr[1] = oldMax;
        } else if (num == arr[0]) {
            arr[1] = num;
        } else {
            if (num > arr[1]) {
                arr[1] = num;
            }
        }
    }

    private static int solve(int[] arr) {
        int n = arr.length;
        int[] maxTwo = new int[] { arr[0], Integer.MIN_VALUE };
        Set<Integer> positiveOrderNumIndexSet = new HashSet<>();
        Map<Integer, Integer> map = new HashMap<>();
        for (int i = 1; i < n; i++) {
            if (arr[i] > maxTwo[0]) {
                positiveOrderNumIndexSet.add(i);
            } else {
                if (maxTwo[1] == Integer.MIN_VALUE) {
                    int preMax = maxTwo[0];
                    map.put(preMax, map.getOrDefault(preMax, 0) + 1);
                } else {
                    int secondMax = maxTwo[1];
                    if (arr[i] > secondMax) {
                        // 说明前面就一个比当前元素大的
                        int preMax = maxTwo[0];
                        map.put(preMax, map.getOrDefault(preMax, 0) + 1);
                    }
                }
            }

            updateTwoMax(maxTwo, arr[i]);
        }

        int count = positiveOrderNumIndexSet.size();
        int ansMax = count;
        for (int i = 0; i < n; i++) {
            if (!map.containsKey(arr[i])) {
                continue;
            }

            count += map.get(arr[i]);
            if (positiveOrderNumIndexSet.contains(i)) {
                count--;
            }
            ansMax = Math.max(ansMax, count);
            count = positiveOrderNumIndexSet.size();
        }

        return ansMax;
    }
}