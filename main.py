import huffmanCoding



text="I am here!!"


huff = huffmanCoding.Huffman()
huff.textInput(text)
huff.createHuffmanTree()
#huff.showCodes()
entext=huff.encodeText()
huff.padText()
huff.createHeader()
huff.completion()



with open('text.text','wb') as file:
    huff.writeToFile(file)

print("\n\nNow decoding-------------------------------------------------------------------\n")

with open('text.text','rb') as file:
    huff.readFromFile(file)
huff.splitContents()
huff.decode()