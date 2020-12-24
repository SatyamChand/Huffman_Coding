class Node:                                                        # A node for huffman tree
    
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
    



    def showCodes(self):                                    #to help user identify codes for different symbols
        for k in self.codes:
            print(k,':',self.codes[k])




    def encodeFromFile(self,filename):                      #reading text from a file
        content=''
        self.encode(content)





    def encode(self,text):                                  #driver to encode text
        self.textInput(text)
        self.createHuffmanTree()
        #self.showCodes()
        entext=self.encodeText()
        self.padText()
        self.createHeader()
        self.completion()




    def textInput(self,inText):
        self.text=inText

        freq_count={}
        for ch in self.text:                                #count frequency of symbols
            if ch not in freq_count:
                freq_count[ch]=0
            freq_count[ch]+=1

        self.tree=[]                                        #creation of nodes to make Huffman tree
        for key in sorted(freq_count,key=freq_count.get):
            self.tree.append(Node(freq_count[key],key))
        



    def createHuffmanTree(self):                            #Creation of tree
        while(len(self.tree)>1):
            new_node = Node(self.tree[0].freq+self.tree[1].freq)
            new_node.createChild(self.tree[0],self.tree[1])
            self.tree=self.tree[2:]
            
            if(len(self.tree)==0):
                self.tree=new_node
                break
            notEndNode=False
            for i in range(len(self.tree)):
                if self.tree[i].freq>new_node.freq:
                    notEndNode=True
                    break
            if notEndNode:
                self.tree.insert(i,new_node)
            else:
                self.tree.append(new_node)
        
        self.createCodes(self.tree)
        



    def createCodes(self,node,string=''):                      #returns code for a text symbol
        if node.data:
            self.codes[string]=node.data
            return
        self.createCodes(node.left,string+'0')
        self.createCodes(node.right,string+'1')
        



    def encodeText(self):                                       #encodes text using dictionary codes, returns string
        e_code=''
        
        encoding_codes={}                                       #creating reverse dict since self.codes stores codes for decoding
        for key in self.codes:
            encoding_codes[self.codes[key]]=key
        
        for ch in self.text:
            e_code+=encoding_codes[ch]

        self.coded_text=e_code
        return self.coded_text
    



    def padText(self):                                          #to pad the text in counts of 8 since we need to create binary string and a byte can only hold 8 binaries
        self.padding=len(self.coded_text)%8
        if self.padding!=0:
            self.padding=8-self.padding
            self.coded_text+='0'*self.padding

        coded_str=bytearray()                                   
        for i in range(0,len(self.coded_text),8):               #conversion to bytes
            coded_str.append(int(self.coded_text[i:i+8],2))
        self.coded_bytestr=coded_str
        return coded_str
    



    def createHeader(self):                                     #returns header that stores relevent data for decoding the file (in byte form)
        header=bytearray()
        header.append(self.padding)
        header.append(len(self.codes))
        for code in self.codes:
            byte=map(ord,code)
            for x in byte:
                header.append(x)
            header.append(127)
            byte=int(ord(self.codes[code]))
            header.append(byte)
        self.header=header
        
            


    def completion(self):                                       
        b=self.header+self.coded_bytestr
        self.completebytestr=b                                  #content ready to be written
        
    def writeToFile(self,filename):                             #to write a binary file with specified name
        with open(filename,'wb') as file:
            file.write(self.completebytestr)
        print('Content written to file : ',self.text)
    '''    
    def writeToFile(self,file):
        file.write(self.completebytestr)
        print('Content written')
    '''


    #----------------------------------------decode section-----------------------------------------
    

    def decodeFromFile(self,filename):                          #read content for decoding
        with open(filename,'rb') as file:
            content=file.read()
            self.decode(content)



    
    def decode(self,content):                                   #driver to decode content
        self.completebytestr=content
        self.splitContents()
        self.decodeOutput()




    def splitContents(self):                                    #splits data to relevent components
        self.padding=int(self.completebytestr[0])
        count=int(self.completebytestr[1])

        i=0
        j=2
        codes={}
        while i<count:                                          #creation of dictionary for decoding
            code=''
            while self.completebytestr[j] != 127:               #value 127 represents end of string here, used here to let te program know the code sting for a symbol has ended
                code+=chr(self.completebytestr[j])
                j+=1
            codes[code]=chr(self.completebytestr[j+1])
            j+=2
            i+=1

        
        barray=bytearray(self.completebytestr[j:])
        b=''
        barray=map(bin,barray)
        
        for x in barray:
            b+=x[2:].rjust(8,'0')                               #conversion to a regular string for comprehesion and removing the padding
        self.codes=codes
        self.coded_text=b[:-self.padding]




    def decodeOutput(self):                                     #decode the string
        decodedtext=''
        s=''
        for ch in self.coded_text:
            s+=ch
            if s in self.codes:
                decodedtext+=self.codes[s]
                s=''
        print(decodedtext,'\n\n\n')
            

