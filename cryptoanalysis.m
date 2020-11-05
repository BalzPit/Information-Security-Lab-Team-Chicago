%Read the approx Matrices, which are the same as Task3
A = readmatrix("linear_key_output.txt");
A = logical(A(:,1:32)');
B = readmatrix("linear_text_output.txt");
B = logical(B(:,1:32)');


text = hexToBinaryVector('08D17555', 32)';
chipher = hexToBinaryVector('22C74406', 32)';

% ######## COMMUNICATION TOOLBOX NEEDED #######

gf_A = gf(A);
inv_A = inv(gf_A);

B_u  = mod(B*text,2);
key = inv_A * (xor(chipher,B_u));
Hex = binaryVectorToHex(logical(key.x'))


