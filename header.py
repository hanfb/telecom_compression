"""
Author: Kevin Lew
StudentID: 29677475
"""

import sys

class Tree:
    """Tree data structure
    """
    def __init__(self):
        """Constructor for tree
        """
        self.root = None
        self.nodes = []
    def add_node(self, node):
        """adds node to tree for popping later in huffman

        Args:
            node (Node): appends Node to list of nodes
        """
        self.nodes.append(node)
    def new_root(self, node):
        """Sets root of tree to node

        Args:
            node (Node): new root node
        """
        self.root = node
    def pop(self):
        """pops node from list of nodes

        Returns:
            Node: Node that is popped from list of nodes
        """
        return self.nodes.pop()
    def size(self):
        """returns the amount of nodes in tree

        Returns:
            Int: amount of nodes in tree
        """
        return len(self.nodes) 
    def sort_nodes(self):
        """sorts the nodes in tree by its frequency in descending order
        """
        self.nodes.sort(reverse=True, key=self.takeFreq)
    def traverse(self, node, code, pointer):
        """DFS traversal of tree and retrieves the code word for each symbol

        Args:
            node (Node): node being traversed
            code (Str): code word of symbol
            pointer (List): pointer for storing symbol and its respective code word
        """
        if not node.is_leaf():
            left_edge = node.left()
            self.traverse(left_edge.get_end(), code+left_edge.get_bit(), pointer)
            right_edge = node.right()
            self.traverse(right_edge.get_end(), code+right_edge.get_bit(), pointer)
        else:
            pointer.append((node.get_code(), code))
    @staticmethod
    def takeFreq(node):
        """Selects the frequency of occurrence used for sorting list of nodes
        Args:
            node (Node): node being sorted

        Returns:
            Int: frequency of occurence for symbol represented in node
        """
        return node.get_freq()

class Node:
    """Node data structure
    """
    def __init__(self, w, freq):
        """Constructor for Node

        Args:
            w (Str): symbol represented by node
            freq (Int): frequency of occurence of symbol in text
        """
        self.code = w
        self.edges = []
        self.freq = freq
    def add_edge(self, e):
        """adds edge to Node

        Args:
            e (Edge): edge to be added to node
        """
        self.edges.append(e)
    def get_code(self):
        """retrieves symbol represented by node

        Returns:
            Str: the symbol represented by node
        """
        return self.code
    def get_freq(self):
        """retrieves frequency of occurence of symbol

        Returns:
            Int: frequency of occurence of symbol in text
        """
        return self.freq
    def left(self):
        """Retrieves the left edge 

        Returns:
            Edge: the left edge whose start is this node
        """
        return self.edges[0]
    def right(self):
        """Retrieves the right edge

        Returns:
            Edge: the right edge whose start is this node
        """
        return self.edges[1]
    def is_leaf(self):
        """checks if node is leaf node

        Returns:
            Bool: True for leaf, False for internal node
        """
        if len(self.code) == 1:
            return True
        else:
            return False

class Edge:
    """Edge data structure
    """
    def __init__(self, bit, nodeS, nodeE):
        """Constructor for Edge

        Args:
            bit (Str): bit of edge
            nodeS (Node): origin node
            nodeE (Node): destination node
        """
        self.val = bit
        self.start = nodeS
        self.end = nodeE
    def get_bit(self):
        """Retrieves bit of edge

        Returns:
            Str: bit of edge
        """
        return self.val
    def get_end(self):
        """Retrives destination node of edge

        Returns:
            Node: destination node of edge
        """
        return self.end

def huffman(w):
    """Compression algorithm using huffman's encoding

    Args:
        w (Str): string within text file

    Returns:
        List: list of symbols and its respective code word
    """
    # find frequency of each symbol
    alphabet = []
    for _ in range(95):
        alphabet.append(0)
    for letter in w:
        alphabet[ord(letter)-32] += 1
    t = Tree()
    # add each unique symbol and its frequency to tree
    for i in range(len(alphabet)):
        if alphabet[i] > 0:
            t.add_node( Node(chr(i+32), alphabet[i]) )
    # create tree through grouping shown in huffman encoding
    while t.size() > 1:
        t.sort_nodes()
        node1 = t.pop()
        node2 = t.pop()
        temp = []
        # concatenate symbol of node1 and node2
        temp.append(node1.get_code())
        temp.append(node2.get_code())
        root = Node("".join(temp), node1.get_freq()+node2.get_freq())
        t.add_node(root)
        t.new_root(root)
        edge1 = Edge("0", root, node1)
        edge2 = Edge("1", root, node2)
        root.add_edge(edge1)
        root.add_edge(edge2)
    # get code word for each unique symbol
    p = [[]]
    t.traverse(t.root, "", p[0])
    codes = p[0]
    return codes

def to_binary(n):
    """Converts decimal to binary

    Args:
        n (Int): Decimal to be converted into binary

    Returns:
        List: each bit of binary representation stored as individual element in list
    """
    b_str = []
    temp = []
    # perform decimal to binary conversion
    while n > 0:
        temp.append(str(n%2))
        n //= 2
    # reverse order of bits 
    for i in range(len(temp)-1, -1, -1):
        b_str.append(temp[i])
    return b_str

def elias_omega(s):
    """Encoding for binary strings using elias omega algorithm

    Args:
        s (Str): Binary string

    Returns:
        Str: Encoded binary string after using elias omega encoding
    """
    l = len(s)
    #encoded = s
    encoded = [s]
    while l > 1:
        l_bin = to_binary(l-1) # previous length - 1 in binary representation
        l_bin[0] = "0" # flip first bit of length component
        encoded.append("".join(l_bin))
        l = len(l_bin) # update l value
    res = []
    # reverse encoded
    for i in range(len(encoded)-1, -1, -1):
        res.append(encoded[i])
    return "".join(res)
    
def header(w):
    """Creates header binary string using huffman and elias omega encoding

    Args:
        w (Str): String within text file

    Returns:
        Str: Binary string representing header 
    """
    header = []
    codes = huffman(w)
    codes.sort(key=takeFirst)
    header.append( elias_omega("".join(to_binary(len(codes)))) ) # number of unique symbols
    for code in codes:
        ascii_w = "".join( to_binary(ord(code[0])) ) # 1) ascii representation of symbol
        code_len = elias_omega( "".join(to_binary(len(code[1]))) ) # 2) elias omega encoding of length of huffman code word
        header.append(ascii_w + code_len + code[1]) # 1 + 2 + huffman code word for symbol
    header = "".join(header)
    output_file(header)
    return header

def takeFirst(n):
    """Takes first element to be sorted

    Args:
        n (List): sub list being sorted

    Returns:
        Any: first element in List
    """
    return n[0]

def output_file(n):
    """Writes header to output file

    Args:
        n (Str): Binary string represent header 
    """
    file = open("output_header.txt", "w")
    file.write(n)
    file.close()

def open_file(filename):
    """Reads string from text file

    Args:
        filename (Str): Name of file to be opened

    Returns:
        Str: String from text file
    """
    file = open(filename, "r")
    s = file.read()
    file.close()
    return s

def main():
    s = open_file(sys.argv[1])
    header(s)
    #print(huffman("gray and miserable"))
    #print(elias_omega("1"))
    #print(header("aacaacabcaba"))
    #print(header(s) == "011110000111110001001000110001101001")
    #print(len("1000000"))
    #print(len(elias_omega("1000000")))

if __name__ == "__main__":
    main()