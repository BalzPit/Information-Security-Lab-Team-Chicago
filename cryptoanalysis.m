%Read the approx Matrices, which are the same as Task3
A = readmatrix("linear_key_output.txt");
A = logical(A(:,1:32)');
B = readmatrix("linear_text_output.txt");
B = logical(B(:,1:32)');


text = hexToBinaryVector('70518CE4', 32)';
chipher = hexToBinaryVector('A3F6BDB7', 32)';
% ######## COMMUNICATION TOOLBOX NEEDED #######
gf_A = gf(A);
inv_A = inv(gf_A);

key = inv_A * (xor(chipher,B*text));
Hex = binaryVectorToHex(logical(key.x'))


