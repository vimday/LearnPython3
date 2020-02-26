__author__ = 'vimday'

import random
import functools
from tree_help import show_rb_tree, save_rb_tree


class RBNode:
    def __init__(self, val, color="R"):
        super().__init__()
        self.val = val
        self.color = color
        self.left = None
        self.right = None
        self.parent = None

    def is_black_node(self):
        return self.color == "B"

    def is_red_node(self):
        return self.color == "R"

    def set_black_node(self):
        self.color = "B"

    def set_red_node(self):
        self.color = "R"

    def print(self):
        if self.left:
            self.left.print()
        print(self.val)
        if self.right:
            self.right.print()


def tree_log(func):
    @functools.wraps(func)
    def function(a, b):
        save_rb_tree(a.root, "{}-{}".format(a.index, a.action))
        a.index += 1
        func(a, b)
        save_rb_tree(a.root, "{}-{}".format(a.index, a.action))
        a.index += 1
    return function


class RBTree:
    '''
    ************
    将红黑树的红节点提升至与其父节点同一高度后 红黑树就变成了4阶B树 ——（2，4）树
    B树为平衡树自然红黑树也为平衡树
    证明：
    包含n个内部节点的红黑树T，高度h=O(logn) //n+1个外部节点
    log2（n+1)<=h<=2*log2(n+1)
    若其黑高度为H，则h=H+R<=2H //红节点数目超不过黑节点
    若T对应的B树为TB，则H为TB的高度（TB的每个节点包含且仅包含一个黑节点）
    H<=log[4/2(向上取整)](n+1)/2+1<=log2(n+1)
    得证
    ************
    性质一：节点是红色或者是黑色；
    性质二：根节点是黑色；
    性质三：每个叶节点（NIL或空节点）是黑色；
    性质四：每个红色节点的两个子节点都是黑色的（也就是说不存在两个连续的红色节点）；
    性质五：从任一节点到其任意叶节点的所有路径都包含相同数目的黑色节点 //每个外部节点到根的路径所经过的黑节点相同
    -->
    1 对每个红色节点，子节点只有两种情况：要么都没有，要么都是黑色的。（不然会违反特征四）
                                                                2 对黑色节点，如果只有一个子节点，那么这个子节点，必定是红色节点。（不然会违反特征五）
    3 假设从根节点到叶子节点中，黑色节点的个数是H, 那么树的高度h范围 H<= h <= 2H（特征四五决定）。
    '''

    def __init__(self):
        self.root = None
        self.index = 1
        self.action = ""

    def left_rotate(self, node):
        print("left rotate", node.val)
        '''
         * 左旋时right 非空
         * 左旋示意图：对节点node进行左旋
         *     parent               parent
         *    /                       /
         *   node                   right
         *  / \                     / \
         * ln  right   ----->     node  ry
         *    / \                 / \
         *   ly ry               ln ly
         * 左旋做了三件事：
         * 1. 将right的左子节点ly赋给node的右子节点,(注意当ly非空时，把其父节点置为node)
         * 2. 将right的左子节点设为node，将node的父节点设为right
         * 3. 将node的父节点parent(非空时)赋给right的父节点，同时更新parent的子节点为right(左或右)
        :param node: 要左旋的节点
        :return:
        '''
        parent = node.parent
        right = node.right

        # 1:把右子节点的左子节点(ly) 赋给node的右节点
        node.right = right.left
        if node.right:
            node.right.parent = node
        # 2:将right的左子节点置为node
        right.left = node
        node.parent = right
        # 3:将right的父节点更新为parent
        right.parent = parent
        if not parent:
            self.root = right
        else:
            if parent.left == node:
                parent.left = right
            else:
                parent.right = right
        pass

    def right_rotate(self, node):
        print("right rotate", node.val)
        '''
         * 右旋时 node的左孩子非空
         * 右旋示意图：对节点node进行右旋
         *        parent           parent
         *       /                   /
         *      node                left
         *     /    \               / \
         *    left  ry   ----->   ln  node
         *   / \                     / \
         * ln  rn                   rn ry
         * 右旋做了三件事：
         * 1. 将left的右子节点rn赋给node的左子节点,并将node赋给rn右子节点的父节点(left右子节点非空时)
         * 2. 将left的右子节点设为node，将node的父节点设为left
         * 3. 将node的父节点parent(非空时)赋给left的父节点，同时更新parent的子节点为left(左或右)
        :param node:
        :return:
        '''
        parent = node.parent
        left = node.left

        # 处理步骤1
        node.left = left.right
        if node.left:
            node.left.parent = node

         # 处理步骤2
        left.right = node
        node.parent = left

        # 处理步骤3
        left.parent = parent
        if not parent:
            self.root = left
        else:
            if parent.left == node:
                parent.left = left
            else:
                parent.right = left
        pass

    def insert_node(self, node):
        '''
        红黑树中插入节点有可能造成双红缺陷
        :param node:
        :return:
        '''
        if not self.root:
            self.root = node
            self.root.set_black_node()
            return
        cur = self.root

        while cur:
            if cur.val < node.val:
                if not cur.right:
                    node.parent = cur
                    cur.right = node
                    break
                cur = cur.right
                continue
            if cur.val > node.val:
                if not cur.left:
                    node.parent = cur
                    cur.left = node
                    break
                cur = cur.left
            return False
        if node.parent.is_black_node():
            return
        # 出现双红缺陷
        solve_double_red(node)
        return "solved double red"

    @tree_log
    def solve_double_red(self, node):
        if self.root == node:
            self.root.set_black_node()
            return
        p = node.parent
        if p.is_black_node():
            return
        # 双红缺陷 node必有祖父节点
        g = p.parent
        if p == g.left:
            u = g.right
            # 1. 没有叔叔节点 若此节点为父节点的右子 则先左旋再右旋 否则直接右旋
            # 2. 有叔叔节点 叔叔节点颜色为黑色
            # 注: 1 2 情况可以合为一起讨论 父节点为祖父节点右子情况相同 只需要改指针指向即可
            #   1,2 情况相当于B树中在某个三叉节点插入红关键码，使得黑关键码不再居中 
            #   调整之后的结果相当于在新的四叉节点中 ,三个关键码的颜色改为RBR，注意此时B数的拓扑结构是不变的
            # 3. 有叔叔节点 叔叔节点颜色为红色 父节点颜色置黑 叔叔节点颜色置黑 祖父节点颜色置红 continue
            #  这种情况相当于B树中的超级节点发生上溢 此时可将p u转黑，g转红 
            #  等效于B树中的节点分裂，关键码g上升一层 再次solve_double_red(g)
            
            #case 3
            if u and u.is_red_node():
                p.set_black_node()
                u.set_black_node()
                g.set_red_node()
                self.solve_doble_red(g)
                return
            #case 1,2
            elif node==p.right:
                #左旋p
                self.left_rotate(p)
                node=node.left #此时为了将1，2情况合并需要将node变成原来的p，此时已然变成case 1
            p=node.parent #注意 才是可能已经将p进行过一次左旋，此时p在左旋后的node的位置
            g=p.parent
            p.set_black_node()
            g.set_red_node()
            self.right_rotate(g)
            return
        #对称情况
        elif p==g.right:
            u=g.left
            if u and u.is_red_node():
                g.set_red_node()
                p.set_black_node()
                u.set_black_node()
                self.solve_double_red(g)
                return
            elif node==p.left:
                self.right_rotate(p)
                node=node.right
            p=node.parent
            g=p.parent
            p.set_black_node()
            g.set_red_node()
            self.left_rotate(g)
            return
        def add_node(self,node):
            self.action='inser node {}'.format(node.val)
            self.insert(node)
            pass

        
        


