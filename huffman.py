__license__ = 'GolluM (c) EPITA'
__docformat__ = 'reStructuredText'
__revision__ = '$Id: huffman.py 2016-04-04'

from binaryTrees import *

def isPresent(e,L):   
    boo = False       
    for i in range (len(L)):
        if L[i] == e:
            boo = True
    return boo
            
def buildFrequencyList(outputList, dataIN):
   l = []
   for i in range(len(dataIN)):
       j = 0
       if isPresent(dataIN[i],l):
           (a,b) = outputList[j]
           while(b != dataIN[i]):
               j += 1
               (a,b) = outputList[j]
           outputList[j] = (a+1,b)     
       else:
           outputList.append((1,dataIN[i]))
           l.append(dataIN[i])
   return(outputList)


'display the tree use for test'

def printTree(B, s=""):  
    if B == None:
        print(s, '- ')
    elif B.left == None and B.right == None:
        print(s, '- ', B.key)
    else:
        print(s, '- ', B.key)
        printTree(B.left, s + "  |")
        printTree(B.right, s + "   ")

'return the two min of a list'

def mins(inputList):    
    ((min1,e1),(min2,e2)) = (inputList[0],inputList[1])
    for i in range(2,len(inputList)):
        (a,ea) = inputList[i]
        if (a < min2):
            ((min2,e2),(a,ea)) = ((a,ea),(min2,e2))
        if (a <= min1):
            ((min1,e1),(a,ea)) = ((a,ea),(min1,e1))
        if (min1 > min2):
            ((min1,e1),(min2,e2)) = ((min2,e2),(min1,e1))          
    return((min1,e1),(min2,e2))
    
def buildHuffmanTree(inputList):
    """Process the frequency list into an Huffman tree according to the algorithm.

        :param inputList: the frequencies list from :func:`buildFrequencyList`.
        :type inputList: tuple<int, str> list
        :return: returns an huffman tree containing all the datas from the list.
        :rtype: BinTree

        :Example:

    
    """
    l = []
    for i in range(len(inputList)):
        (a,b) = inputList[i]
        l.append((a , newBinTree(b,None,None)))
    while(len(l) > 1):        
        B = BinTree()       
        ((a,b),(c,d)) = mins(l)
        M = []
        for i in range(len(l)):
            if (l[i] != (a,b)) and (l[i] != (c,d)):
                M.append(l[i])
        l = M
        B.key= '.'
        B.left = d
        B.right = b
        l.append((a+c,B))
    (a,b)=l[0]
    return b

'search an element in a tree'

def reachCharTree(B,c,path):  
    if B == None:
        return stringPop(path)
    if B.key == c:
        return path
    path1 = reachCharTree(B.left,c,path + '0')
    path2 = reachCharTree(B.right,c,path + '1')
    if path1 == path2:
        return stringPop(path1)
    if len(path1) > len(path2):
        return path1
    else:
        return path2
        
def encodeData(huffmanTree, dataIN):
    """Encode the input string to its binary string representation.

        :param huffmanTree: the huffman tree from :func:`buildHuffmanTree`.
        :param dataIN: the data we want to encode.
        :type huffmanTree: BinTree
        :type dataIN: str
        :return: returns the binary string.
        :rtype: str

        :Example:
        
    """
    s = ""
    for i in range(len(dataIN)):
        s += reachCharTree(huffmanTree,dataIN[i],"")    
    return s
  
'depth parcours which return the binary value of the current string'

def recTree(H,s):   
    if H.left == None and H.right == None:        
        return s + '1' + int_to_bin(ord(H.key),8)
    if H.left != None:
        s =(recTree(H.left,s +'0'))
    if H.right != None:
        s =recTree(H.right,s)
    return s
   
    
def encodeTree(huffmanTree):
    """Encodes an huffman tree to its binary representation using a preOrder traversal:
        * each leaf key is encoded into its binary representation on 8 bits preceded by '1'
        * each time we go left we add a '0' to the result

        :param huffmanTree: the huffman tree to encode.
        :type huffmanTree: BinTree
        :return: returns a string corresponding to the binary representation of the huffman tree.
        :rtype: str

        :Example:

        
    """
    s = ""
    s=recTree(huffmanTree,s)
    return s

'convert a decimal to binary on p bits'

def int_to_bin(n,p): 
    r = ''
    while n>0:
        r = str(n%2) +r
        n = n//2
    r = (p-len(r))*'0'+r
    return r

'convert a binary on 8bits into a decimal'

def bin_to_int(s): 
    r = 0
    for i in s:
        r = int(i) + r*2
    return r

"pop the last element of s"
    
def stringPop(s):  
    t = ""
    for i in range(len(s)-1):
        t += s[i]
    return t

'delete every 0 at the end of s'
    
def del_zero(s):  
    sinter = s
    boo = True
    i = len(s)-1
    while boo and i > -1:
        if s[i] == '0':
            sinter = stringPop(sinter)
        else:
            boo = False
        i -= 1
    return sinter
    
def toBinary(dataIN):
    """Compress a string containing the binary representation to its real compressed string.

        :param dataIN: the data to compress.
        :type dataIN: str
        :return: returns a tuple: the compressed string corresponding to the input and the number of bits for the alignment.
        :rtype: tuple<str, int>

        :Example:

    
    

        .. warning:: some characters in the output string may not be visibles if you print it.
        s += chr(bin_to_int(inter,8))
    """
    s = ""
    inter = ""
    cpt = 0
    while (len(dataIN)%8 != 0):
        dataIN += '0'
        cpt +=1
    l = []
    for i in range (len(dataIN)):
        if i%8 == 0:
            l.append(inter)            
            inter = ""
        inter += dataIN[i]
    inter = ""
    for i in range (len(dataIN)-8,len(dataIN)):
        inter += dataIN[i]
    l.append(inter)
    l[len(l)-1] = del_zero(l[len(l)-1])    
    for i in range (len(l)):
        if l[i] != '':
           s += chr(bin_to_int(l[i]))
    return (s,cpt)

def compression(dataIN):
    """Compress a string using the Huffman algorithm.

        :param dataIN: the data to compress.
        :type dataIN: str
        :return: returns the compressed data (and its number of bits for the alignment) and the compressed tree (and its number of bits for the alignment).
        :rtype: tuple< tuple<str, int>, tuple<str, int> >

        :Example:

    
        
    """
    l = []
    B = buildHuffmanTree(buildFrequencyList(l,dataIN))
    (dataBIN,dataBINtree) = (encodeData(B,dataIN),encodeTree(B))
    (dataBIN,dataBINtree) = (toBinary(dataBIN),toBinary(dataBINtree))
    return (dataBIN,dataBINtree)


'DECOMPRESSION'

'return the correspondant tree of cpt in binary'

def decodeEnts(dataIN,cpt):      
    B = newBinTree("",None,None)
    B.key = '.'
    smid = ""
    if cpt == len(dataIN):
        return (B,cpt)
    if dataIN[cpt] == '0':
        (B.left,cpt) = decodeEnts(dataIN,cpt+1)
        (B.right,cpt) = decodeEnts(dataIN,cpt)
        return (B,cpt)
    if dataIN[cpt] == '1':
        smid = ""
        cpt += 1
        for i in range (8):        
            smid += dataIN[cpt+i]
        B.key = chr(bin_to_int(smid))
        cpt += 8
        return (B,cpt)
    if cpt == len(dataIN):
        return (B,cpt)
    return (B,cpt)
    
    
def decodeTree(dataIN, alignement):
    """Decodes an huffman tree from it binary representation:
        * a '0' means we add a new internal node and go to its left node
        * an '1' means the next 8 values are the encoded character of the current leaf.

        :param dataIN: the real binary string containing the encoded huffman tree.
        :param alignement: the number of bits to ignore at the end of the input.
        :type dataIN: str
        :type alignement: int
        :return: returns decoded huffman tree
        :rtype: BinTree

        :Example: 
    """
    s = ""
    sinter = ""
    i = 0
    while(i < len(dataIN)):
        if dataIN[i] == '\\' and dataIN[i+1] == 'x':
            n = 16*int(dataIN[i+2]) + int(dataIN[i+3])
            s += int_to_bin(n,8)
            i += 4
        else:
            s += int_to_bin(ord(dataIN[i]),8)
            i += 1
    i = len(s)-1 - (8-alignement)
    decal = 8 - alignement
    k = 0
    while(k <= decal):
        sinter += s[i+k]
        k += 1
    k = 0
    while(k <= 8):
        s = stringPop(s)
        k += 1
    s += sinter
    (a,b) = decodeEnts(s,0)   
    return a

'return the decode value of huffman tree'

def decodeString(H,s,res,cpt,refH): 
    if H.right==None and H.left == None: 
        res += H.key
        (res,cpt) = decodeString(refH,s,res,cpt,refH)
    if cpt == len(s):
        return (res,cpt)
    if s[cpt] == '0':
        (res,cpt) = decodeString(H.left,s,res,cpt+1,refH)
    if cpt == len(s):
        return (res,cpt)
    if s[cpt] == '1':
        (res,cpt) = decodeString(H.right,s,res,cpt+1,refH)
    return (res,cpt)
   
        
def decodeData(huffmanTree, dataIN, alignement):
    """Decode a binary string using the corresponding huffman tree into something more readable.

        :param huffmanTree: the huffman tree for decoding.
        :param dataIN: the input binary string we want to decode.
        :param alignement: the number of bits to ignore at the end of the input.
        :type huffmanTree: BinTree
        :type dataIN: str
        :type alignement: int
        :return: returns the decoded text
        :rtype: str

        :Example:

    
        
    """
    s = ""
    sinter = ""
    res = ""
    cpt = 0
    i = 0
    while(i < len(dataIN)):
        if dataIN[i] == '\\' and dataIN[i+1] == 'x':
            n = 16*int(dataIN[i+2]) + int(dataIN[i+3])
            s += int_to_bin(n,8)
            i += 4
        else:
            s += int_to_bin(ord(dataIN[i]),8)
            i += 1
    i = len(s)-1 - (8-alignement)
    decal = 8 - alignement
    k = 0
    while(k <= decal):
        sinter += s[i+k]
        k += 1
    k = 0
    while(k <= 8):
        s = stringPop(s)
        k += 1
    s += sinter
    (res,a) = decodeString(huffmanTree,s,res,cpt,huffmanTree)        
    return res

def decompression(dataIN):
    """Decompress the data compressed using the Huffman algorithm :func:`compression`

        :param dataIN: the compressed data and huffman tree, and their respectives alignment bits.
        :type dataIN: tuple< tuple<str, int>, tuple<str, int> >
        :return: returns the decompressed text.
        :rtype: str

        :Example:
        
    """
    ((a,b),(c,d)) = dataIN
    H = decodeTree(c,d)
    s = decodeData(H,a,b)
    return s

data = compression('Oh I am sorry did I break your concentration')
print(data)
print(decompression(data))
