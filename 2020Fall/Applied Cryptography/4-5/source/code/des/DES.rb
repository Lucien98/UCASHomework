require "./init.rb"

class ConvertArray
	#convert array to binary string, delimited by a space
	def self.toBinary(input)
		input.each_slice(4) . map . inject("") {|sum, s| sum << (s . join . to_s + " ")}
	end
	#convert array to hex string, delimited by a space
	def self.toHex(input)
		x = input.each_slice(4) . map . inject("") {|sum, s| sum << s . join . to_s}
		"%08X" % x.to_i(2)
	end
end

class Bignum
	def hex_to_binary_arr
		bin_len = self.to_s(16) . length * 4
		format = "%#{bin_len}d"
		sprintf(format, self.to_s(2)) . split("") . map(&:to_i)
	end
end

class Fixnum
	def hex_to_binary_arr
		bin_len = self.to_s(16) . length * 4
		format = "%#{bin_len}d"
		sprintf(format, self.to_s(2)) . split("") . map(&:to_i)
	end
end

def printHex(input)
	puts "#{ConvertArray.toHex(input)}" 
end

def printBin(input)
	puts "#{ConvertArray.toBinary(input)}"
end

class DES
	def AddCheckBits(key)
		key_bits = key.hex_to_binary_arr 
		# key_bits = @key.hex_to_binary_arr
		i = 8
		# extend key to 64 bits
		until i < 1 do
			sum = 0
			j = 7
			until j < 1 do
				sum += key_bits[7*i-j]
				j = j - 1
			end
			key_bits[7*i, 0] = sum % 2
			i = i - 1
		end
		key_bits
	end

	def permutation(count, origin_arr, permute_arr)
		out_arr = []
		count.times do |i|
			out_arr[i] = origin_arr[permute_arr[i] - 1]
		end
		out_arr
	end

	def shift(c_in, d_in)
		if @round == 1 || @round == 2 || @round == 9 || @round == 16
			c_out = @c_in[1..27] + [@c_in[0]]
			d_out = @d_in[1..27] + [@d_in[0]]
		else
			c_out = @c_in[2..27] + @c_in[0..1]
			d_out = @d_in[2..27] + @d_in[0..1]
		end
		return c_out, d_out
	end

	def round_key(c_in, d_in)
		#@c_in, @d_in = shift()
		tmp = @c_in + @d_in
		roundkey = permutation(48, tmp, PC_2)
	end

	def getPlaintex_IP
		@plaintext
	end

	def getKey
		@key
	end

	def round_function
		@c_in, @d_in = shift(@c_in, @d_in) 
		roundkey = round_key(@c_in, @d_in)
		puts "input left and right halves:\n"
		printHex(@l)
		printHex(@r)
		puts "\n\n"
		l = @r
		r_e = permutation(48, @r, E)
		# puts "expansion permutation:"
		# printHex(r_e)
		puts "round key"
		printHex(roundkey)
		sbox_in_array = r_e.zip(roundkey).map { |x,y| x^y }
		sbox_8_in = sbox_in_array . each_slice(6) . map . inject([]) { |sum, s| sum << s.join.to_i(2) }
		sbox_outputs = []

		8.times do |i|
			tmp = sbox_8_in[i]
			j = tmp / 32 * 2 +  (tmp % 2)
			k = (tmp % 32) / 2
			sbox_outputs[i] = Sbox[i][j][k]
			# puts "sbox %d input: %0.6b " % [i+1 , tmp]
		end

		sb_out = sbox_outputs.each.map.inject([]) { |sum, s| sum << sprintf("%04d", s.to_s(2)).split("")}

		sb_out = sb_out.flatten.each.map(&:to_i)
		# puts "Sbox Output:\n"
		# printHex(sb_out)
		# puts "-----\n\n"
		sbox_outputs_P = permutation(32, sb_out, P)
		r = sbox_outputs_P.zip(@l).map { |x,y| x^y }
		# puts "output left and right halves:\n"
		# printHex(l)
		# printHex(r)
		# puts "\n\n"
		@l, @r = l, r
		@round = @round + 1
	end

	def sixteen_rounds
		15.times do |i|
			# puts "第%d轮的输出" % (i+2)
			round_function
		end
	end

	# def swap
	# 	@l, @r = r, l
	# end

	def fp
		merge_halves = @r + @l
		printHex(merge_halves) 
		@cipher = permutation(64, merge_halves, IIP)
	end

	def get_cipher
		fp()
		@cipher
	end

	def initialize(key, plaintext)
		if key.to_s(16) .length == 14
			@key = AddCheckBits(key)
			#puts "%s" % AddCheckBits(key)
			@key.length.times do |t|
				print "#{@key[t]}"
			end
			puts "\n"
		end
		if key.to_s(16) .length == 15
			@key = [0,0,0,0] + key.hex_to_binary_arr
			@key.length.times do |t|
				print "#{@key[t]}"
			end
			puts "\n"			
		else
			@key = key.hex_to_binary_arr
			@key.length.times do |t|
				print "#{@key[t]}"
			end
			puts "\n"
		end
		@key = permutation(56, @key, PC_1)
		origin_arr = Array.new(64)
		if plaintext.to_s(16).length == 15
			origin_arr = [0,0,0,0] + plaintext.hex_to_binary_arr
		else
			origin_arr = plaintext.hex_to_binary_arr
		end
		@plaintext = permutation(64, origin_arr, IP)
		@round = 1
		@c_in = @key[0..27]
		@d_in = @key[28..55]
		@l = @plaintext[0..31]
		@r = @plaintext[32..63]
	end
end

key = 0x5555555555555511
#key = 0x0123456789abcdef
plaintext = 0xFEFEFEFEFEFEFEFE

des = DES.new(key, plaintext)
puts "第1轮的输出"
des.round_function()

#des.sixteen_rounds()

#printHex(des.get_cipher())
