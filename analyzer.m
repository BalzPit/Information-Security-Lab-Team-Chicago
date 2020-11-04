A = readmatrix("linear_key_output.txt");
A = A(:,1:32)';
B = readmatrix("linear_text_output.txt");
B = B(:,1:32)';

text = double(hexToBinaryVector('12345678', 32)');
key = double(hexToBinaryVector('87654321', 32)');

A_k = mod(A*key,2);
B_u = mod(B*text,2);

result = xor(A_k,B_u);
Hex = binaryVectorToHex(result')
