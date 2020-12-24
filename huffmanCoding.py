class Node:   
    
    def __init__(self,freq,data=None):
        self.data=data
        self.freq=freq
    
    def createChild(self,leftC,rightC):
        self.left=leftC
        self.right=rightC
    
    
    def sdisplay(self):
        print(self.data)
        
    def display(self):
        if self.data:
            print(self.data)
        print(self.freq)
        if hasattr(self,'right'):
            self.left.display()
            self.right.display()

            
    
    
class Huffman:
    def __init__(self):
        self.text=''
        self.codes={}
        self.coded_text=''
        self.tree=[]
        self.padding=0
        self.coded_bytestr=''
        self.header=''
        self.completebytestr=''
    
    def encode(self):
        
        return
        
    def showCodes(self):
        for k in self.codes:
            print(k,':',self.codes[k])
    
    def textInput(self,inText):
        self.text=inText
        print(inText)
        freq_count={}
        self.tree=[]
        for ch in self.text:
            if ch not in freq_count:
                freq_count[ch]=0
            freq_count[ch]+=1
        for key in sorted(freq_count,key=freq_count.get):
            self.tree.append(Node(freq_count[key],key))
        print('text=',self.text)
        
        
        
    def createHuffmanTree(self):
        while(len(self.tree)>1):
            new_node = Node(self.tree[0].freq+self.tree[1].freq)
            new_node.createChild(self.tree[0],self.tree[1])
            self.tree=self.tree[2:]
            
            if(len(self.tree)==0):
                self.tree=new_node
                break
            sm=False
            for i in range(len(self.tree)):
                if self.tree[i].freq>new_node.freq:
                    sm=True
                    break
                    
            if sm:
                self.tree.insert(i,new_node)
            else:
                self.tree.append(new_node)
        
        self.createCodes(self.tree)
        
    
    def createCodes(self,node,string=''):
        if node.data:
            self.codes[string]=node.data
            return
        self.createCodes(node.left,string+'0')
        self.createCodes(node.right,string+'1')
        
            
    def encodeText(self):
        e_code=''
        encoding_codes={}
        for key in self.codes:
            encoding_codes[self.codes[key]]=key
        print(encoding_codes)
        for ch in self.text:
            e_code+=encoding_codes[ch]
        print(self.text)
        print(e_code)
        self.coded_text=e_code
        print('coded text :',self.coded_text)
        #print(len(self.coded_text))
        return self.coded_text
    
    def padText(self):
        self.padding=len(self.coded_text)%8
        if self.padding!=0:
            self.padding=8-self.padding
            self.coded_text+='0'*self.padding
        #print(len(self.coded_text),self.coded_text)

        coded_str=bytearray()
        for i in range(0,len(self.coded_text),8):
            coded_str.append(int(self.coded_text[i:i+8],2))
        print(coded_str)
        self.coded_bytestr=coded_str
        return coded_str
    
    def createHeader(self):
        header=bytearray()
        #print(self.padding)
        #print(self.coded_text)
        #print(len(self.coded_text))
        header.append(self.padding)
        header.append(len(self.codes))
        for code in self.codes:
            #byte=int(code,2)
            byte=map(ord,code)
            #print(*byte)
            for x in byte:
                header.append(x)
            header.append(127)
            #print(ord(self.codes[code]))
            byte=int(ord(self.codes[code]))
            header.append(byte)
        self.header=header
        #print(header)
        
            
    def completion(self):
        b=self.header+self.coded_bytestr
        #print(b)
        self.completebytestr=b
        
    def writeToFile(self,file):
        file.write(self.completebytestr)
        print('Content written')
        

    #----------------------------------------
    
    def readFromFile(self,file):
        with open('text.text','rb') as file:
            byte=file.read()
            #print(byte)
            #print(int(byte[1]))
            #print(byte[2:])
            self.completebytestr=byte
    
    def splitContents(self):
        print(self.completebytestr)
        self.padding=int(self.completebytestr[0])
        count=int(self.completebytestr[1])
        i=0
        j=2
        codes={}
        while i<count:
            code=''
            #print(chr(self.completebytestr[j]))
            while self.completebytestr[j] != 127:
                #print('.',end=' ')
                code+=chr(self.completebytestr[j])
                j+=1
            #print(code)
            codes[code]=chr(self.completebytestr[j+1])
            j+=2
            i+=1
        print(codes)
        barray=bytearray(self.completebytestr[j:])
        print(barray)
        b=''
        barray=map(bin,barray)
        
        #some decoding error here---------------------------------------------
        #fixed
        for x in barray:
            b+=x[2:].rjust(8,'0')
        print(b)
        self.coded_text=b[:-self.padding]
    
    def decode(self):
        print(self.coded_text)
        decodedtext=''
        s=''
        for ch in self.coded_text:
            s+=ch
            if s in self.codes:
                decodedtext+=self.codes[s]
                s=''
        print(decodedtext)
            

