require "./AESSbox.rb"

def _init_
	#plaintext = ""
	plaintext_matrix = []
	key_matrix = []
	16.times do |i|
		#plaintext << "%02X" % i
		plaintext_matrix[i]=i
		key_matrix[i] = 1
	end
	return plaintext_matrix, key_matrix
end
class Array
	# the function that prints the matrix of a 16-byte array
	def print
		puts "%02X & %02X & %02X & %02X \\\\" % [self[0], self[4], self[8], self[12]]
		puts "%02X & %02X & %02X & %02X \\\\" % [self[1], self[5], self[9], self[13]]
		puts "%02X & %02X & %02X & %02X \\\\" % [self[2], self[6], self[10], self[14]]
		puts "%02X & %02X & %02X & %02X \\\\" % [self[3], self[7], self[11], self[15]]
	end
end

class Fixnum
	def add(addtion)
		self ^ addtion
	end
	def mult(multiplier)
		res=0
		if multiplier == 1
			res = self
		end
		
		if multiplier == 2
			
			if self >= 128
				res = self * 2 - 256
				res = res ^ 0X1B
			else 
				res = self * 2
			end
		end

		if multiplier==3
			res = self.mult(2).add(self)
		end
		res
	end
end


class XOR
	def self.sum(block_one, block_two)
		block_one.zip(block_two).map {|x,y| x^y}
	end
end

class AES
	def init
		@plaintext_matrix, @key_matrix = _init_()
		#@key_matrix.print
		@round = 0
		@rc = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36]
		@round_enc_result = @plaintext_matrix
	end

	def subByte(byte)
		i = byte / 16
		j = byte % 16
		AesBox[i][j]
	end
	def computeRoundKey
		i = @round * 16
		# cycle shift left 1 byte
		shift1B = [@key_matrix[i-3], @key_matrix[i-2], @key_matrix[i-1], @key_matrix[i-4]]
		#puts shift1B
		4.times do |i|
			puts "%02X" % ( shift1B[i] = subByte(shift1B[i]) )
		end
		#puts shift1B
		constant = [@rc[@round], 0, 0, 0]
		#puts constant
		# compute key_matrix的第四列,即key_matrix[16-19] 
		# w[i] = w[i-4] + constant + subbytes(shiftibyte(w[i-1])) ; w_{i-4} = key_matrix[i-16, 4]
		# the i in last line is the i of aes algorithm, 
		# not the index i of key_matrix array in the program 
		@key_matrix += XOR.sum( XOR.sum(shift1B, constant), @key_matrix[i-16,4] )
		#@key_matrix[4,16].print
		# compute w[i+1],w[i+2],w[i+3]
		3.times do
			i += 4
			# puts i
			# puts @key_matrix[i-4, 4]
			# puts @key_matrix[i-16, 4]
			@key_matrix += XOR.sum(@key_matrix[i-4, 4], @key_matrix[i-16, 4])
		end
		@key_matrix[16,16].print
	end

	def SubBytes
		# @round = 1
		16.times do |i|
			@round_enc_result[i] = subByte(@round_enc_result[i])

		end
	end

	def AddKey
		# key is in the @key_matrix
		@round_enc_result = XOR.sum(@key_matrix[@round * 16, 16], @round_enc_result)
		@round += 1
	end

	def ShiftRows
		round_enc_result = Array.new(@round_enc_result)
		#@round_enc_result.print
		# 循环移位写成列向量的形式
		# PC =[ 0, 4, 8,12,
		# 	  5, 9,13, 1,
		# 	 10,14, 2, 6,
		# 	 15, 3, 7,11
		# ]
		pc = [ 0,  5, 10, 15,
			   4,  9, 14,  3,
			   8, 13,  2,  7,
			  12,  1,  6, 11
		]
		16.times do |i|
			@round_enc_result[i] = round_enc_result[pc[i]]
		end
	end

	def MixColumn
		#@round_enc_result = 
		round_enc_result_matrix_2d = [
			[@round_enc_result[0],@round_enc_result[4],@round_enc_result[8],@round_enc_result[12]],
			[@round_enc_result[1],@round_enc_result[5],@round_enc_result[9],@round_enc_result[13]],
			[@round_enc_result[2],@round_enc_result[6],@round_enc_result[10],@round_enc_result[14]],
			[@round_enc_result[3],@round_enc_result[7],@round_enc_result[11],@round_enc_result[15]]
		]
		mix_matrix = [
			[2,3,1,1],
			[1,2,3,1],
			[1,1,2,3],
			[3,1,1,2]
		]
		mix_round_result_2dmatrx = Array.new(4) { Array.new(4) }
		4.times do |i|
			4.times do |j|
				mix_round_result_2dmatrx[i][j] = 0
				4.times do |k|
					mix_round_result_2dmatrx[i][j] ^= round_enc_result_matrix_2d[k][j].mult(mix_matrix[i][k])
				end
			end
		end
		pc_1 = [
			[0,0],[1,0],[2,0],[3,0],
			[0,1],[1,1],[2,1],[3,1],
			[0,2],[1,2],[2,2],[3,2],
			[0,3],[1,3],[2,3],[3,3]
		]
		16.times do |i|
			@round_enc_result[i] = mix_round_result_2dmatrx[pc_1[i][0]][pc_1[i][1]]
		end
	end

	def RoundFunction
		init
		self.AddKey
		puts "初始化轮密钥后的结果"
		@round_enc_result.print
		self.SubBytes
		puts "字节替换后的结果"
		@round_enc_result.print
		self.ShiftRows
		puts "行移位后的结果"
		@round_enc_result.print
		self.MixColumn
		puts "列混淆后的结果"
		@round_enc_result.print
		self.computeRoundKey
		puts "第一轮密钥："
		@key_matrix[16, 16].print
		self.AddKey
		#puts "第一轮加密的结果"
		#@round_enc_result.print
	end

end

plaintext_matrix, key_matrix = _init_()

puts plaintext_matrix.class
# plaintext_matrix.print()
key_matrix.print()
# AesBox[0].print
aes = AES.new
aes.init
#aes.computeRoundKey
aes.RoundFunction
#puts "%02X" % 0X6E.mult(3)