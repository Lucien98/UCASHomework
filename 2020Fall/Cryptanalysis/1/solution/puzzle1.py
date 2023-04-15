F = [
0.0651738, 0.0124248, 0.0217339,
0.0349835, 0.1041442, 0.0197881,
0.0158610, 0.0492888, 0.0558094,
0.0009033, 0.0050529, 0.0331490,
0.0202124, 0.0564513, 0.0596302,
0.0137645, 0.0008606, 0.0497563,
0.0515760, 0.0729357, 0.0225134,
0.0082903, 0.0171272, 0.0013692,
0.0145984, 0.0007836
]       # 英文字符频率。
cipher = 'fcqfpifibqyiqaqgcjxjbdktirveprklolosjotbitpnjqcnqjomhdfziobqjktjnoyfvvkwwrkqlsydhkxlibtjadkchsbwjcsapimivmemfobbitarolbhmpbncdptjxykqptepzmmrvcltgksylyqdpbhifulvhkdvzxkfksuzfizhobqjvwmzrprpxwyjeugcfcoditzklxhvlcecluimpxjmtunpznwlxmnlfcznzxltoqadjxnjsesfweevganivbfwpljueclezufsttuedlthvxhspvfedltehddmbqlpiumdsimfdtevgfibtymdjkbkguihnyqvyqmngqtenkkjxajdadtelbhneskdhgnifzhllkpwdlpdqziardnjlxrohcrardnuflzlxrsxxgnvkbnesysjjcnmfwzstcqsttbexztshcbjmkscdkofvklmobnyjfqslhsxkanmblmhkozwpomkgudhmehircjcdscvkufqptepffibywlmrskmoywsxxfqpxuexflhoeztpxuejiqmlrfhxymnsuofxbzoatepkqrzvtzoarrktypdprnjaluedgnifkmtdqapifivsynqgqpnlfohijlpthumommrhjzoawujlavlcshwrvbuymjzqbifqoqzdumbvewgobziguszooffobnclmyfhgnnhanpimmcpzvxkgfnbllbqjsxbbuyhfibkahnxdnjkbtbokrvkskmqctpzwkffunhlkngstfoltuydrghkufsttbfxxszooflnynyykmfjtfwrwqnkuqilekqphbwdumecyncakmpgpvncgrtxwqmoyxhkolaxjnzfuoolknfktjaddnbmeiaxtxnpyfmlrffkcfsukmbsbqjeqbhxxrsorzqlbnvqpnnxbmxbbulfcjvkddmbquejirsorzqwdjdgmhbscixfqfnbwnsquhimqpiomhehzfvobuebiihvnlgreb'

def count_CI2(cipher, a, n):     # n 代表我们猜测的秘钥，也即偏移量
    N = [0.0 for i in range(26)]
    #cipher = c_alpha(cipher)
    L = len(cipher)
    for i in range(L):     #计算所有字母的频数，存在数组N当中
        if (cipher[i].islower()):
            N[a*(ord(cipher[i]) - ord('a') - n)%26] += 1
        else:
            N[(ord(cipher[i]) - ord('A') - n)%26] += 1  
    CI_2 = 0
    for i in range(26):
        CI_2 += ((N[i] / L) * F[i])
    return CI_2

def one_key(cipher_alpha,key_len):
    un_cip = ['' for i in range(key_len)]   
    #cipher_alpha = c_alpha(cipher)
    for i in range(len(cipher_alpha)):     # 完成分组工作
        z = i % key_len
        un_cip[z] += cipher_alpha[i]
    for i in range(key_len):
        print (i)
        pre_5_key(un_cip[i])     ####这里应该将5个分组的秘钥猜测全部打印出来

## 找出前5个最可能的单个秘钥
def pre_5_key(cipher):
    M = [(0, 0, 0.0) for i in range(12) for k in range(26)]
    coprime = (1,3,5,7,9,11,15,17,19,21,23,25) 
    for i in range(12):
        for k in range(26):
            #M[i*26 + k] = (chr(ord('a')+coprime[i]), chr(ord('a') + k), abs(0.065 - count_CI2(cipher, coprime[i], k)))
            M[i*26 + k] = (coprime[i], k, abs(0.065 - count_CI2(cipher, coprime[i], k)))
    #print(M)
    M = sorted(M,key = lambda x:x[2])   #按照数组第二个元素排序

    for i in range(10):
        print (M[i])
# for key_len in range(12, 13):
#     #key_len = 4   #输入猜测的秘钥长度
#     one_key(cipher,key_len)
#     print("\n\n\n\n")

a = [17, 21, 5]
m = [21, 23, 10, 25]

plaintext = ""
i = 0
while i < len(cipher):
    # for j in range(3):
    #     for k in range(4):
    plaintext += chr((a[i % 3] * (ord(cipher[i]) - ord('a') - m[i % 4]))%26 + ord('a') )
    i = i+1
print(plaintext)