#coding:utf-8
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

    def rotateAt(self, v):
        '''
        :param v:为非空孙辈节点
        * BST节点旋转变换统一算法（3节点 + 4子树），返回调整之后局部子树根节点的位置
        * 注意：尽管子树根会正确指向上层节点（如果存在），但反向的联接须由上层函数完成
        '''
        if not v:
            print("Fail to rotate a null node")
            return
        p = v.parent
        g = p.parent
        # 视v、p和g相对位置分四种情况
        if g.left == p:  # zig
            if p.left == v:
                # case 1:zig-zig
                p.parent = g.parent  # 向上连接
                return self.connect34(v, p, g, v.left, v.right, p.right, g.right)
            else:
                # case 2:zig-zag
                v.parent = g.parent
                return self.connect34(p, v, g, p.left, v.left, v.right, g.right)
        else:  # zag
            if p.right == v:
                # case 3:zag-zag
                p.parent = g.parent
                return self.connect34(g, p, v, g.left, p.left, v.left, v.right)
            else:
                # case 4:zag-zig
                v.parent = g.parent
                return self.connect34(g, v, p, g.left, v.left, v.right, p.right)

    def connect34(self, lf, g, rf, s1, s2, s3, s4):
        lf.left = s1
        if s1:
            s1.parent = lf
        lf.right = s2
        if s2:
            s2.parent = lf
        rf.left = s3
        if s3:
            s3.parent = rf
        rf.right = s4
        if s4:
            s4.parent = rf
        g.left = lf
        lf.parent = g
        g.right = rf
        rf.parent = g
        return g

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
        self.solve_double_red(node)
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

            # case 3
            if u and u.is_red_node():
                p.set_black_node()
                u.set_black_node()
                g.set_red_node()
                self.solve_doble_red(g)
                return
            # case 1,2
            elif node == p.right:
                # 左旋p
                self.left_rotate(p)
                node = node.left  # 此时为了将1，2情况合并需要将node变成原来的p，此时已然变成case 1
            p = node.parent  # 注意 才是可能已经将p进行过一次左旋，此时p在左旋后的node的位置
            g = p.parent
            p.set_black_node()
            g.set_red_node()
            self.right_rotate(g)
            return
        # 对称情况
        elif p == g.right:
            u = g.left
            if u and u.is_red_node():
                g.set_red_node()
                p.set_black_node()
                u.set_black_node()
                self.solve_double_red(g)
                return
            elif node == p.left:
                self.right_rotate(p)
                node = node.right
            p = node.parent
            g = p.parent
            p.set_black_node()
            g.set_red_node()
            self.left_rotate(g)
            return

    def add_node(self, node):
        self.action = 'inser node {}'.format(node.val)
        self.insert_node(node)
        pass

    def real_delete_node(self, node):
        if node == self.root:
            self.root = None
            return
        if node.parent.left == node:
            node.parent.left = None
            return
        if node.parent.right == node:
            node.parent.right = None
            return
        return

    def search(self, val):
        if not self.root:
            return None
        cur = self.root
        while cur:
            if cur.val == val:
                return cur
            if cur.val < val:
                cur = cur.right
            else:
                cur = cur.left
        return None

    def findRightMin(self, node):
        """
        找到以 node 节点为根节点的树的最小值节点 并返回
        :param node: 以该节点为根节点的树
        :return: 最小值节点
        """
        temp_node = node.right
        if not temp_node:
            return None
        while temp_node.left:
            temp_node = temp_node.left
        return temp_node

    def findLeftMax(self, node):
        """
        找到以 node 节点为根节点的树的最大值节点 并返回
        :param node: 以该节点为根节点的树
        :return: 最大值节点
        """
        temp_node = node.left
        if not temp_node:
            return None
        while temp_node.right:
            temp_node = temp_node.right
        return temp_node

    def transplant(self, node_u, node_v):
        """
        用 v 替换 u
        :param tree: 树的根节点
        :param node_u: 将被替换的节点
        :param node_v: 替换后的节点
        :return: None
        """
        if not node_u.parent:
            self.root = node_v
        elif node_u == node_u.parent.left:
            node_u.parent.left = node_v
        elif node_u == node_u.parent.right:
            node_u.parent.right = node_v
        # 加一下为空的判断
        if node_v:
            node_v.parent = node_u.parent
    # 可以优化为交换node与后继节点的值

    def delete_node(self, node):
        node_color = node.color
        if not node.left:
            # 没有左子树 则直接用右子树代替该节点
            succ_node = node.right
            self.transplant(node, succ_node)
        elif not node.right:
            succ_node = node.left
            self.transplant(node, succ_node)
        else:
            # 既有左子又有右子，取右子中的最小者替代该节点
            new_node = self.findRightMin(node)

            node_color = new_node.color
            succ_node = new_node.right
            if new_node.parent != node:
                # 用new_node的后继取代newnode,并将newnode作为node右子树的根
                self.transplant(new_node, succ_node)
                new_node.right = node.right
                new_node.right.parent = new_node
            # 此时此时以newnode为根的右子树，已完全平衡，可以取代node且不影响平衡
            self.transplant(node, new_node)
            # 以下代码不能封装到transplant中 ，容易成环，transplant的取代是向上取代
            new_node.left = node.left
            new_node.left.parent = new_node
            new_node.color = node.color
        if not self.root:
            return
        if self.root == succ_node:
            self.root.set_black_node()
            return
        # 没有后继节点，x为底层节点
        # 若x为红色节点可直接删除，此时node_color为原x的颜色，若为黑色，则需调整
        if not succ_node:
            succ_node = node
        if node_color == "B":
            self.solve_doble_black(succ_node)

    def solve_doble_black(self, cur):
        if cur.is_red_node() or self.root == cur:
            cur.set_black_node()
            return
        # 此时 x,r(succ,x的后继者)均为黑色
        # 摘除 x(原new_node）后 黑深度不再统一，等效于B树中x所属节点发生下溢
        # 此时原x(现r)必非根
        p = cur.parent  # 原x的父亲
        if p.left == cur:
            s = p.right
        else:
            s = p.left
        # 双黑缺陷，必存在兄弟
        if s.is_black_node():
            # case1:s为黑,且有一红孩子 BB-1
            t = None
            if s.left and s.left.is_red_node():
                t = s.left
            if s.right and s.right.is_red_node():
                t = s.right
            if t:
                # 对应B树中的通过关键码的选择，消除超级节点的下溢
                # 若 s为p的左孩子，则需对p进行右旋，t，p染黑，s继承原来p的颜色
                # 也可以不区分 直接进行3+4重构
                p_old_color = p.color
                # 备份原子树根节点p颜色，并对t及其父亲、祖父
                # 以下，通过旋转重平衡，并将新子树的左、右孩子染黑
                new_root = self.rotateAt(t)
                if self.root == p:
                    self.root = p
                elif p.parent.left == p:
                    p.parent.left = new_root
                else:
                    p.parent.right = new_root
                new_root.left.set_black_node()
                new_root.right.set_black_node()
                new_root.color = p_old_color
            # 黑s无红孩子
            else:
                s.set_red_node()  # s转红
                # case 2:BB-2R p为红，p转黑，s转红即可
                # 等效于b树中下溢节点与兄弟合并，因p为红色，必有黑关键码，所以不会持续下溢
                if p.is_red_node():
                    p.set_black_node()
                else:
                    # case 3:BB-2B
                    # r,p保持黑 ，由于s已转红，故此子树黑高度平衡，但整树不平衡
                    # 相当于b树中下溢节点与兄弟合并，但合并之前p与s均为单关键码节点
                    # 因此下层下溢的修复引发上层下溢 最多O(logn）次
                    self.solve_double_black(p)
        else:
            # case 4:s为红 BB-3 此时隐藏条件为p必为黑
            # 则 将s转黑 p转红
            s.set_black_node()
            p.set_red_node()
            # 取t与其父s同侧
            if p.left == s:
                t = s.left
            else:
                t = s.right
            # 对t及其父亲、祖父做平衡调整
            new_root = rotateAt(t)
            if p == self.root:
                self.root = new_root
            elif p == p.parent.left:
                p.parent.left = new_root
            else:
                p.parent.right = new_root
            # 继续修正r处双黑——此时的p已转红，故后续只能是BB-1或BB-2R
            self.solve_double_black(cur)

    def delete_val(self,val):
        node=self.search(val)
        if not node:
            print("node error {}".format(val))
            return
        save_rb_tree(self.root, "{}_delete_pre".format(val))
        self.delete_node(node)
        save_rb_tree(self.root, "{}_delete_after".format(val))
        pass
if __name__ == '__main__':

    tree = RBTree()
    data = list(range(1, 20))
    random.shuffle(data)
    print(data)
    for i in data:
        tree.add_node(RBNode(i))

    random.shuffle(data)
    for i in data:
        print("delete ", i)
        tree.delete_val(i)


    pass