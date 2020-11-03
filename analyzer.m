A = readmatrix("linear_key_output.txt");
A = A(:,1:32)';
B = readmatrix("linear_text_output.txt");
B = B(:,1:32)';

text = hexToBinaryVector('80000000', 32)';
key = hexToBinaryVector('80000000', 32)';

result = (xor(A*key, B*text))'
Hex = binaryVectorToHex(result)