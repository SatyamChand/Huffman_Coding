import huffmanCoding



text="I am here!!"


huff = huffmanCoding.Huffman()
huff.encode(text)

filename='demo.bin'
huff.writeToFile(filename)

print("\n\nNow decoding-------------------------------------------------------------------\n")

huff.decodeFromFile(filename)

