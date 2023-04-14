require "./init.rb"
puts " 第i个S盒 & 该随机变量等于0的次数 & 偏差 \\\\"
total = 64.0
8.times do |i|
	count = 0.0
	4.times do |j|
		16.times do |k|
			count_ones = (Sbox[i][j][k]*2 + k/8).to_s(2).scan("1").length
			if count_ones % 2 == 0
				count += 1
			end
		end
	end
	puts "%d & %d & %f \\\\" %[i, count, count/total - 0.5]
end