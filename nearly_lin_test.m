%Read the approx Matrices, which are the same as Task3
A = readmatrix("linear_key_output.txt");
A = A(:,1:32)';
B = readmatrix("linear_text_output.txt");
B = B(:,1:32)';

save = readtable("output_hex.txt");
table = table2array(save);
tablelen = height(save);
match = zeros(tablelen,1);

for ii=1:tablelen
    key = hexToBinaryVector(table(ii,1),32)';
    text = hexToBinaryVector(table(11,2),32)';
    cipher = hexToBinaryVector(table(ii,3),32)';
    
    result = xor(A*key, B*text);
    % sum(xor(result, cipher))
    
    if sum(xor(result, cipher)) == 0
        match(ii) = 1;
    end
    
end

prob = sum(match)