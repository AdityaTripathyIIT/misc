`timescale 1ns/1ps

module Nand4BitAdder(sum, 
  cout, 
  a, 
  b, 
  cin);
    input [3:0] a, b;
    input cin;
    output [3:0] sum;
    output cout;

    wire [4:0] carry;
    assign carry[0] = cin;

    genvar i;
    generate
        for (i = 0; i < 4; i = i + 1) begin : adder_stage
            wire n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12;
            wire a_xor_b, ab, cin_a_xor_b;

            nand #1 (n1, a[i], b[i]);
            nand #1 (n2, a[i], n1);
            nand #1 (n3, b[i], n1);
            nand #1 (a_xor_b, n2, n3);

            nand #1 (n4, a_xor_b, carry[i]);
            nand #1 (n5, a_xor_b, n4);
            nand #1 (n6, carry[i], n4);
            nand #1 (sum[i], n5, n6);

            // nand #1 (n7, a[i], b[i]);
            // nand #1 (ab, n7, n7);

            nand #1 (ab, n1, n1);
            nand #1 (n8, carry[i], a_xor_b);
            nand #1 (cin_a_xor_b, n8, n8);

            nand #1 (n9, ab, ab);
            nand #1 (n10, cin_a_xor_b, cin_a_xor_b);
            nand #1 (carry[i+1], n9, n10);
        end
    endgenerate

    assign cout = carry[4];
endmodule

