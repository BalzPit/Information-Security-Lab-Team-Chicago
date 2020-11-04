A = readmatrix("linear_key_output.txt");
A = A(:,1:32)';
Ainv = inv(A);
B = readmatrix("linear_text_output.txt");
B = B(:,1:32)';

text = hexToBinaryVector('08D17555', 32)';
cipher = hexToBinaryVector('22C74406', 32)';

k = Ainv*(xor(text, B*cipher))
Hex = binaryVectorToHex(result')
