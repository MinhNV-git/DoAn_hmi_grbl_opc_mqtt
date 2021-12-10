import func.HandlesString as func
import func.wrFile as hFile

# f= open('log.txt','r')
    
# for i in range(21):
#     data = f.readline()
#     print(data)
#     a = func.HandlesResponseGRBL_new(data)
#     print(a)

# f.close()

# (a,b,c,d) = func.HandlesGcodeLine('x10 y10 z10')
# print(a)
# print(b)
# print(c)
# print(d)

a = hFile.ReadLine_n('O1',10)
if a=='':
    print('rongs')
print(a)