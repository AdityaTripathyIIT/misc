`timescale 1ns/1ps
module full_adder_8bit_tb;
    reg [7:0] a, b;
    reg cin;
    wire [7:0] sum;
    wire cout;
    
    full_adder_8bit dut(
        .a(a),
        .b(b),
        .cin(cin),
        .sum(sum),
        .cout(cout)
    );
    
    initial begin
        $dumpfile("wave2.vcd");
        $dumpvars(0, full_adder_8bit_tb);


        a = 8'd25; b = 8'd17; cin = 0;
        #10;
        $display("Test Case 1: a = %d, b = %d, cin = %d\n cout = %d, sum %d", 
                 a, b, cin, cout, sum);
        
        a = 8'd100; b = 8'd50; cin = 1;
        #10;
        $display("Test Case 2: a = %d, b = %d, cin = %d\n cout = %d, sum %d",
                 a, b, cin, cout, sum);
        
        a = 8'd200; b = 8'd100; cin = 0;
        #10;
        $display("Test Case 3: a = %d, b = %d, cin = %d\n cout = %d, sum %d", 
                 a, b, cin, cout, sum);
        
        $finish;
    end
endmodule
