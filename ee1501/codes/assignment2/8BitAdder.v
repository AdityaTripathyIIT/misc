/*
module EightBitAdder(input [7 : 0] a,
  input [7 : 0] b, 
  input cin, 
  output reg [7 : 0] sum, 
  output reg cout);

  reg rippleCarry;
  always @ (*) begin
  rippleCarry = cin;
    for (integer i = 0; i < 8; i = i + 1) begin
      sum[i] = a[i] ^ b[i] ^ rippleCarry;
      rippleCarry = ((a[i] ^ b[i]) & rippleCarry) | (a[i] & b[i]);
    end
    cout = rippleCarry;
  end
endmodule
*/
module full_adder_1bit(
    input a,
    input b,
    input cin,
    output sum,
    output cout
);
    assign sum = a ^ b ^ cin;
    assign cout = (a & b) | (a & cin) | (b & cin);
endmodule

module full_adder_8bit(
    input [7:0] a,
    input [7:0] b,
    input cin,
    output [7:0] sum,
    output cout
);
    reg [7:0] sum_temp;
    reg [8:0] carry;
    
    always @(*) begin
        carry[0] = cin;
        
        for (int i = 0; i < 8; i = i + 1) begin
            sum_temp[i] = a[i] ^ b[i] ^ carry[i];
            carry[i+1] = (a[i] & b[i]) | (a[i] & carry[i]) | (b[i] & carry[i]);
        end
    end
    
    assign sum = sum_temp;
    assign cout = carry[8];
endmodule
