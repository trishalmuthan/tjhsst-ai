import pickle

bruh = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
length = len(bruh)

outfile = open('tester.pkl','wb')
pickle.dump(bruh,outfile)
pickle.dump(length,outfile)
outfile.close()

infile = open('tester.pkl', 'rb')
new_bruh = pickle.load(infile)
print(new_bruh)
new_length = pickle.load(infile)
print(new_length)
infile.close()