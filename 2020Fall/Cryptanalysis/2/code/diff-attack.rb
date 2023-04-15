$PERMUTATION =  [0,4,8,12,1,5,9,13,2,6,10,14,3,7,11,15]
$SBOXFORWARD =  [6,4,12,5,0,7,2,14,1,15,3,13,8,10,9,11]
$SBOXBACKWARD = [4,8,6,10,1,3,0,5,12,14,13,15,2,11,7,9]

$DELTA = [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0]
$OUTPUTDELTA1 = [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0] #
$OUTPUTDELTA2 = [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0]
$OUTPUTDELTA3 = [0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0]
$OUTPUTDELTA4 = [0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0]

class Xor
  def self.sum(block_one, block_two)
    block_one.zip(block_two).map {|x,y| x^y}
  end
end

class Fixnum
  def hex_to_binary_array
    sprintf("%04d", self.to_s(2)).split("").map(&:to_i)
  end
end

class Sbox
  # input: 16 bit array
  def self.sub(input, direction)
    raise "input not 16 bits" unless input.length == 16
    dir = direction == "forward" ? $SBOXFORWARD : $SBOXBACKWARD
    hexes = input.each_slice(4).map.inject([]) { |sum, s| sum << s.join.to_i(2)}
    hexes.inject([]) { |sum, h| sum += dir[h].hex_to_binary_array }
  end
end

class Permuter
  def self.permute(input)
    raise "input not 16 bits" unless input.length == 16
    16.times.map { |i| input[$PERMUTATION[i]] }
  end
end

class Round
  def self.forward(key, state, skip_permuter = false)
    raise "key not 16 bits" unless key.length == 16
    raise "state not 16 bits" unless state.length == 16
    state = Xor.sum(state, key)
    state = Sbox.sub(state, "forward")
    skip_permuter ? state : Permuter.permute(state)
  end

  def self.backward(key, state, skip_permuter = false)
    raise "key not 16 bits" unless key.length == 16
    raise "state not 16 bits" unless state.length == 16
    state = skip_permuter ? state : Permuter.permute(state)
    state = Sbox.sub(state, "backward")
    Xor.sum(state, key)
  end
end

class Cipher
  def self.encrypt(input, key)
    raise "input not 16 bits" unless input.length == 16
    raise "key not 96 bits" unless key.length == 96
    results = Round.forward(key[0,16], input)
    results = Round.forward(key[16,16], results)
    results = Round.forward(key[32,16], results)
    results = Round.forward(key[48,16], results)
    results = Round.forward(key[64,16], results , true)
    Xor.sum(results, key[80,16])
  end

  def self.decrypt(input, key)
    raise "input not 16 bits" unless input.length == 16
    raise "key not 96 bits" unless key.length == 96
    results = Xor.sum(input, key[80,16])
    results = Round.backward(key[64,16], results , true)
    results = Round.backward(key[48,16], results)
    results = Round.backward(key[32,16], results)
    results = Round.backward(key[16,16], results)
    Round.backward(key[0,16], results)
  end
end

class KnownPairGenerator
  def self.generate(key, pair_count)
    pairs = []
    pair_count.times do |i|
      #print "." if i % 100 == 0
      input1 = sprintf("%16d", i.to_s(2)).split("").map(&:to_i)
      input2 = Xor.sum(input1, $DELTA)
      output1 = Cipher.encrypt(input1, key)
      output2 = Cipher.encrypt(input2, key)
      output_delta = Xor.sum(output1, output2)
      pairs << {plain1: input1, plain2: input2, cipher1: output1, cipher2: output2} \
        if output_delta==$OUTPUTDELTA1 || output_delta==$OUTPUTDELTA2 \
          || output_delta==$OUTPUTDELTA3 || output_delta==$OUTPUTDELTA4
    end
    puts ""
    pairs
  end
end

class Analyzer
  def initialize(known_pairs)
    @known_pairs = known_pairs
  end

  def run_through_known_pairs
    @matches = {}
    @known_pairs.each_with_index do |known_pair, index|
      #print "#{index}." if index % 100 == 0
      cipher1 = known_pair[:cipher1]
      cipher2 = known_pair[:cipher2]
      16.times do |sbox53_key|
        @matches["#{sbox53_key}"] ||= 0
        xor53_1 = sbox53_key ^ cipher1[8,4].join.to_i(2)
        unsub53_1 = $SBOXBACKWARD[xor53_1].hex_to_binary_array
        xor53_2 = sbox53_key ^ cipher2[8,4].join.to_i(2)
        unsub53_2 = $SBOXBACKWARD[xor53_2].hex_to_binary_array
        @matches["#{sbox53_key}"] += 1 if Xor.sum(unsub53_1, unsub53_2) == [0,0,1,0]
      end
    end
    true
  end

  def sorted_matches
    @matches.sort { |x,y| (y[1]).abs <=> (x[1]).abs }
  end

end


unknown_key = 96.times.map { rand 2 }
puts "the generated 96-bit random key is"
puts "#{unknown_key[0,96]}"
puts "the key we want to recover is subkey 5 bits 8-11: #{unknown_key[88,4]}"
known_pairs = KnownPairGenerator.generate(unknown_key, 65536)

analyzer = Analyzer.new(known_pairs)
analyzer.run_through_known_pairs

puts "Here are the sorted best 10 results from analysis:"
analyzer.sorted_matches.first(10).each do |pair|
  puts "{#{pair[0]}} => #{(pair[1].to_f).abs / 65536}"
end
subkey5_part=0
print "Result:the most probable subkey 5 bits 8-11 is "
analyzer.sorted_matches.first(1).each do |pair|
  subkey5_part=pair[0]
  print "#{pair[0]} in decimal whose binary is "
end
puts "#{subkey5_part.to_i(10).hex_to_binary_array}"
if unknown_key[88,4]==subkey5_part.to_i(10).hex_to_binary_array 
	then puts "Attack successed!" 
end